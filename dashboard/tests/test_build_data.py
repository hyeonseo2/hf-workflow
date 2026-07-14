import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from dashboard.scripts.build_data import (
    compile_archive,
    parse_manifest,
    parse_report,
    write_snapshot,
)


MANIFEST_WITH_COLON_TITLE = """\
version: 1

run:
  id: sample-run
  created_at: 2026-07-11T03:41:07+00:00
  target_date: 2026-07-11

source:
  feed_url: https://huggingface.co/blog/feed.xml
  url: https://huggingface.co/blog/model-guide
  slug: model-guide
  title: \"Model: A practical guide\"
  published_date: 2026-07-10
  language: en

translation:
  target_repo: Hugging-Face-KREW/hugging-face-krew.github.io
  branch: translate/model-guide
  file_path: _posts/2026-07-11-model-guide.md
  pr_url: https://github.com/Hugging-Face-KREW/hugging-face-krew.github.io/pull/168
  locale: ko

handoff:
  seo:
    enabled: true
    primary_keyword: \"\"
    secondary_keywords: []
  quality:
    enabled: true
    checks:
      - fidelity
      - fluency
"""

QUALITY_REPORT = """\
# Quality Report

## Checks

- PASS: translation body is not empty
- PASS: no TODO marker remains

## Metrics

- body characters: 17410
- Korean letter ratio: 42.28%
"""

SEO_REPORT = """\
# SEO Report

## Checks

- PASS: frontmatter title exists

## Frontmatter

- title: Model: Korean practical guide
- categories: [Translation, HuggingFace]

## Heading Snapshot

- `# Model: Korean practical guide`
- `## Details`
"""

WARNING_REPORT = """\
# Quality Report

## Checks

- WARN: terminology needs review
- FAIL: source link is missing
"""

WARNING_ONLY_REPORT = """\
# Quality Report

## Checks

- WARN: terminology needs review
"""

SEO_WARNING_REPORT = """\
# SEO Report

## Checks

- WARN: title needs review
"""

SEO_FAIL_REPORT = """\
# SEO Report

## Checks

- PASS: frontmatter title exists
- WARN: description needs review
- FAIL: source URL is missing
"""


class CompileArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

    def make_archive(
        self,
        manifest=MANIFEST_WITH_COLON_TITLE,
        quality=None,
        seo=None,
        request=None,
        extra_manifests=None,
    ):
        archive = Path(self.temp_dir.name) / "workflow.zip"
        with ZipFile(archive, "w") as zip_file:
            zip_file.writestr("archive-root/reports/pr-168/manifest.yaml", manifest)
            if quality is not None:
                zip_file.writestr("archive-root/reports/pr-168/quality-report.md", quality)
            if seo is not None:
                zip_file.writestr("archive-root/reports/pr-168/seo-report.md", seo)
            if request is not None:
                zip_file.writestr("archive-root/reports/pr-168/request.md", request)
            for pr_number, extra_manifest in extra_manifests or []:
                zip_file.writestr(
                    f"nested-root/reports/pr-{pr_number}/manifest.yaml", extra_manifest
                )
        return archive

    def test_parse_manifest_supports_nested_scalars_and_lists(self):
        manifest = parse_manifest(MANIFEST_WITH_COLON_TITLE)

        self.assertEqual(manifest["version"], 1)
        self.assertTrue(manifest["handoff"]["seo"]["enabled"])
        self.assertEqual(manifest["handoff"]["seo"]["secondary_keywords"], [])
        self.assertEqual(manifest["handoff"]["quality"]["checks"], ["fidelity", "fluency"])
        self.assertEqual(manifest["source"]["title"], "Model: A practical guide")

    def test_parse_manifest_decodes_yaml_single_quote_escape(self):
        manifest = parse_manifest(
            MANIFEST_WITH_COLON_TITLE.replace(
                'title: "Model: A practical guide"', "title: 'Bob''s guide'"
            )
        )

        self.assertEqual(manifest["source"]["title"], "Bob's guide")

    def test_parse_report_derives_status_and_preserves_sections(self):
        parsed = parse_report(SEO_REPORT)

        self.assertEqual(parsed["status"], "pass")
        self.assertEqual(parsed["checks"], [{"status": "pass", "text": "frontmatter title exists"}])
        self.assertEqual(parsed["frontmatter"]["title"], "Model: Korean practical guide")
        self.assertEqual(parsed["frontmatter"]["categories"], "[Translation, HuggingFace]")
        self.assertEqual(parsed["headings"], ["# Model: Korean practical guide", "## Details"])

    def test_parse_report_marks_warning_only_report_as_warning(self):
        self.assertEqual(parse_report(WARNING_ONLY_REPORT)["status"], "warning")

    def test_compiles_reports_and_marks_missing_seo(self):
        archive = self.make_archive(
            manifest=MANIFEST_WITH_COLON_TITLE,
            quality=QUALITY_REPORT,
        )

        result = compile_archive(archive)

        self.assertEqual(result["repository"], "Hugging-Face-KREW/hugging-face-krew.github.io")
        self.assertEqual(result["reports"][0]["source"]["title"], "Model: A practical guide")
        self.assertEqual(result["reports"][0]["quality"]["status"], "pass")
        self.assertEqual(result["reports"][0]["quality"]["metrics"]["body characters"], "17410")
        self.assertEqual(result["reports"][0]["quality"]["fileName"], "quality-report.md")
        self.assertEqual(result["reports"][0]["quality"]["content"], QUALITY_REPORT)
        self.assertTrue(result["reports"][0]["quality"]["enabled"])
        self.assertTrue(result["reports"][0]["quality"]["available"])
        self.assertEqual(result["reports"][0]["seo"]["status"], "missing")
        self.assertEqual(result["reports"][0]["seo"]["fileName"], "seo-report.md")
        self.assertEqual(result["reports"][0]["seo"]["content"], "")
        self.assertTrue(result["reports"][0]["seo"]["enabled"])
        self.assertFalse(result["reports"][0]["requestAvailable"])

    def test_compiles_missing_quality_as_visible_status(self):
        result = compile_archive(self.make_archive(seo=SEO_REPORT))

        self.assertEqual(result["reports"][0]["quality"]["status"], "missing")
        self.assertFalse(result["reports"][0]["quality"]["available"])

    def test_compiles_seo_warning_and_fail_statuses(self):
        warning_result = compile_archive(self.make_archive(seo=SEO_WARNING_REPORT))
        fail_result = compile_archive(self.make_archive(seo=SEO_FAIL_REPORT))

        self.assertEqual(warning_result["reports"][0]["seo"]["status"], "warning")
        self.assertEqual(fail_result["reports"][0]["seo"]["status"], "fail")

    def test_compiles_warning_reports_request_and_descending_pr_order(self):
        older_manifest = MANIFEST_WITH_COLON_TITLE.replace(
            "sample-run", "older-run"
        ).replace("03:41:07", "02:00:00").replace("/168", "/167")
        archive = self.make_archive(
            quality=WARNING_REPORT,
            seo=SEO_REPORT,
            request="# Review Request\n",
            extra_manifests=[(167, older_manifest)],
        )

        result = compile_archive(archive)

        self.assertEqual([report["prNumber"] for report in result["reports"]], [168, 167])
        report = result["reports"][0]
        self.assertEqual(report["quality"]["status"], "fail")
        self.assertEqual(report["quality"]["checks"][0]["status"], "warning")
        self.assertTrue(report["seo"]["available"])
        self.assertEqual(report["seo"]["content"], SEO_REPORT)
        self.assertEqual(report["seo"]["headings"], ["# Model: Korean practical guide", "## Details"])
        self.assertTrue(report["requestAvailable"])
        self.assertEqual(result["reportSnapshotAt"], "2026-07-11T03:41:07+00:00")

    def test_existing_malformed_report_is_warning_and_repository_must_match(self):
        archive = self.make_archive(quality="# Quality Report\n\n## Metrics\n\n- body characters: 1\n")
        result = compile_archive(archive)
        self.assertEqual(result["reports"][0]["quality"]["status"], "warning")
        self.assertTrue(result["reports"][0]["quality"]["available"])

        foreign_manifest = MANIFEST_WITH_COLON_TITLE.replace(
            "Hugging-Face-KREW/hugging-face-krew.github.io", "another/repository"
        ).replace("/168", "/167")
        mixed_archive = self.make_archive(extra_manifests=[(167, foreign_manifest)])
        with self.assertRaisesRegex(ValueError, "target repository"):
            compile_archive(mixed_archive)

    def test_every_manifest_requires_a_non_empty_target_repository(self):
        missing_repository_manifest = MANIFEST_WITH_COLON_TITLE.replace(
            "  target_repo: Hugging-Face-KREW/hugging-face-krew.github.io\n", ""
        ).replace("/168", "/167")
        archive = self.make_archive(extra_manifests=[(167, missing_repository_manifest)])

        with self.assertRaisesRegex(ValueError, "non-empty translation.target_repo"):
            compile_archive(archive)

    def test_report_snapshot_uses_chronological_timestamp_across_offsets(self):
        latest_utc_manifest = MANIFEST_WITH_COLON_TITLE.replace(
            "03:41:07+00:00", "00:00:00+00:00"
        )
        earlier_plus_nine_manifest = MANIFEST_WITH_COLON_TITLE.replace(
            "03:41:07+00:00", "03:41:07+09:00"
        ).replace("/168", "/167")
        archive = self.make_archive(
            manifest=latest_utc_manifest,
            extra_manifests=[(167, earlier_plus_nine_manifest)],
        )

        result = compile_archive(archive)

        self.assertEqual(result["reportSnapshotAt"], "2026-07-11T00:00:00+00:00")

    def test_write_snapshot_is_byte_deterministic_with_sorted_keys_and_newline(self):
        archive = self.make_archive(quality=QUALITY_REPORT, seo=SEO_REPORT)
        first_output_path = Path(self.temp_dir.name) / "first-reports.json"
        second_output_path = Path(self.temp_dir.name) / "second-reports.json"

        write_snapshot(archive, first_output_path)
        write_snapshot(archive, second_output_path)

        first_bytes = first_output_path.read_bytes()
        expected_bytes = (
            json.dumps(
                compile_archive(archive), ensure_ascii=False, indent=2, sort_keys=True
            ).encode("utf-8")
            + b"\n"
        )
        self.assertEqual(first_bytes, second_output_path.read_bytes())
        self.assertEqual(first_bytes, expected_bytes)
        self.assertTrue(first_bytes.endswith(b"\n"))


if __name__ == "__main__":
    unittest.main()
