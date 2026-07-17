"""Image optimization validation checker"""
from __future__ import annotations
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import extract_images


def check_images(
    body: str,
    target_root: Path | None = None,
    post_path: str | None = None,
) -> Dict[str, Any]:
    """
    Check image optimization for SEO compliance.

    Args:
        body: Markdown body content
        target_root: cloned target repo root; enables D7 file-existence check
        post_path: post path relative to target_root (for resolving relative img src)

    Returns:
        {
            'passed': bool,
            'score': float,
            'checks': [...]
        }
    """
    checks = []
    images = extract_images(body)

    if not images:
        # No images is okay, not a failure
        return {
            'passed': True,
            'score': 1.0,
            'checks': [{
                'name': 'no_images',
                'passed': True,
                'severity': 'info',
                'message': 'No images found (optional)',
                'value': 0
            }],
            'summary': {
                'required': '0/0',
                'recommended': '0/0',
                'optional': '0/0'
            }
        }

    # 1. Alt text coverage (REQUIRED)
    images_with_alt = [img for img in images if img['alt'].strip()]
    alt_coverage = len(images_with_alt) / len(images) if images else 0

    checks.append({
        'name': 'alt_text_coverage',
        'passed': alt_coverage == 1.0,
        'severity': 'required',
        'message': f'Alt text coverage: {len(images_with_alt)}/{len(images)} images',
        'value': images_with_alt
    })

    # 2. Descriptive alt text (REQUIRED)
    # Alt should be >5 chars and not just filename
    descriptive_alts = []
    non_descriptive = []

    for img in images:
        alt = img['alt'].strip()
        src = img['src']
        filename = Path(src).stem if src else ''

        if alt and len(alt) > 5 and alt.lower() != filename.lower():
            descriptive_alts.append(img)
        elif alt:
            non_descriptive.append(img)

    descriptive_ratio = len(descriptive_alts) / len(images_with_alt) if images_with_alt else 0

    checks.append({
        'name': 'descriptive_alt_text',
        'passed': descriptive_ratio >= 0.8,
        'severity': 'required',
        'message': f'Descriptive alt text: {len(descriptive_alts)}/{len(images_with_alt)} (≥80% recommend)',
        'value': {'descriptive': descriptive_alts, 'non_descriptive': non_descriptive}
    })

    # 3. WebP format (OPTIONAL)
    webp_images = [img for img in images if '.webp' in img['src'].lower()]
    webp_ratio = len(webp_images) / len(images) if images else 0

    checks.append({
        'name': 'webp_format',
        'passed': webp_ratio >= 0.5,
        'severity': 'optional',
        'message': f'WebP format: {len(webp_images)}/{len(images)} images (≥50% recommend)',
        'value': webp_images
    })

    # 4. Lazy loading (OPTIONAL)
    # Check for loading="lazy" in HTML img tags
    lazy_count = body.count('loading="lazy"') + body.count("loading='lazy'")
    checks.append({
        'name': 'lazy_loading',
        'passed': lazy_count > 0,
        'severity': 'optional',
        'message': f'Lazy loading: {lazy_count} images (optional)',
        'value': lazy_count
    })

    # 5. Image files actually exist (D7, REQUIRED when target_root provided)
    if target_root is not None:
        local_imgs = [i for i in images if not i['src'].startswith(('http://', 'https://', 'data:'))]
        missing = []
        for img in local_imgs:
            src = img['src'].split('#')[0].split('?')[0]
            if src.startswith('/'):
                candidate = target_root / src.lstrip('/')
            else:
                base = (target_root / post_path).parent if post_path else target_root
                candidate = base / src
            if not candidate.exists():
                missing.append(img['src'])
        checks.append({
            'name': 'image_files_exist',
            'passed': not missing,
            'severity': 'required',
            'message': (
                f'All {len(local_imgs)} local image file(s) exist'
                if not missing else
                f'{len(missing)} image file(s) not found: {", ".join(missing[:3])}'
            ),
            'value': missing,
        })

    # Calculate score
    required_checks = [c for c in checks if c['severity'] == 'required']
    optional_checks = [c for c in checks if c['severity'] == 'optional']

    required_passed = sum(1 for c in required_checks if c['passed'])
    optional_passed = sum(1 for c in optional_checks if c['passed'])

    # Score: required 85%, optional 15%
    score = 0.0
    if required_checks:
        score += 0.85 * (required_passed / len(required_checks))
    if optional_checks:
        score += 0.15 * (optional_passed / len(optional_checks))

    passed = all(c['passed'] for c in required_checks)

    return {
        'passed': passed,
        'score': score,
        'checks': checks,
        'summary': {
            'required': f'{required_passed}/{len(required_checks)}',
            'optional': f'{optional_passed}/{len(optional_checks)}'
        }
    }
