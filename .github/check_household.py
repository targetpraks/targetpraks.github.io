# /// script
# dependencies = ["playwright", "pymupdf"]
# ///
"""With Chrome installed, run: uv run .github/check_household.py [--write-pdf]."""

import argparse
from pathlib import Path

import pymupdf
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "2026-11-18-2026-11-16-maio-household.html"
PDF = ROOT / "2026-11-18-maio-household.pdf"


def render(page):
    return page.pdf(prefer_css_page_size=True, print_background=True, tagged=True, outline=True)


def page_texts(data):
    with pymupdf.open(stream=data, filetype="pdf") as document:
        return [page.get_text(sort=True) for page in document]


def check_print(page):
    full = render(page)
    texts = page_texts(full)
    starts = ["Week at a glance", "Daily routine", "Domestic cleaning", "Gardener checklist",
              "Lily", "Julie", "Ricardo", "Kids & Sofia", "The standard at 16:00",
              "Open questions", "Your notes"]
    assert len(texts) == len(starts), "Unexpected number of A4 pages"
    for title, text in zip(starts, texts):
        assert title in text, f"Missing {title} on the expected page"
    # Exercise the actual buttons and check which content reaches the print dialog.
    page.evaluate("window.print = () => {}")
    for button in page.locator("button[onclick^=printSheet]").all():
        button.click()
        section = page.locator("section.print-target")
        name = section.get_attribute("id")
        page.emulate_media(media="print")
        assert page.locator("section:visible").count() == 1, f"Another section is visible on {name}"
        title = section.locator("h2").inner_text().strip()
        isolated = page_texts(render(page))
        page.emulate_media(media="screen")
        assert len(isolated) == 1 and title in isolated[0], f"Invalid sheet: {name}"
        if name in {"domestic", "gardener"}:
            assert "Signed:" in isolated[0] and "What we agreed" not in isolated[0]
        page.evaluate("window.dispatchEvent(new Event('afterprint'))")
        assert page.locator(".print-target").count() == 0
    return full


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-pdf", action="store_true")
    args = parser.parse_args()
    with sync_playwright() as driver:
        browser = driver.chromium.launch(channel="chrome")
        page = browser.new_page()
        page.goto(SOURCE.as_uri())
        data = check_print(page)
        browser.close()
    if args.write_pdf:
        PDF.write_bytes(data)
    else:
        assert page_texts(PDF.read_bytes()) == page_texts(data), "Regenerate the published PDF"
    print("Verified the full planner and individual print sheets.")


if __name__ == "__main__":
    main()
