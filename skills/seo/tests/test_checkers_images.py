"""Functional tests for the image checker (D6 alt, D7 file-existence)."""
from checkers import check_images


def _by_name(r):
    return {c["name"]: c for c in r["checks"]}


def test_no_images_is_ok():
    assert check_images("# T\n\ntext only")["passed"]


def test_alt_coverage_and_descriptive():
    body = '![검색 임베딩 벤치마크 다이어그램](/a.png)'
    c = _by_name(check_images(body))
    assert c["alt_text_coverage"]["passed"]
    assert c["descriptive_alt_text"]["passed"]


def test_missing_alt_fails_coverage():
    body = '<img src="/a.png" alt="">\n\n![](b.png)'
    assert not check_images(body)["passed"]


def test_d7_file_exists(sample_target_root):
    body = '![구조 다이어그램](/assets/images/sample/exists.png)'
    c = _by_name(check_images(body, sample_target_root, "_posts/2026-01-01-sample.md"))
    assert c["image_files_exist"]["passed"]


def test_d7_missing_file_fails(sample_target_root):
    body = '![없는 이미지 설명](/assets/images/sample/missing.png)'
    c = _by_name(check_images(body, sample_target_root, "_posts/2026-01-01-sample.md"))
    assert not c["image_files_exist"]["passed"]
    assert "/assets/images/sample/missing.png" in c["image_files_exist"]["value"]
