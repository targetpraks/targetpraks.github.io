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
    page.emulate_media(media="print")
    try:
        return page.pdf(prefer_css_page_size=True, print_background=True, tagged=True, outline=True)
    finally:
        page.emulate_media(media="screen")


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
        assert len(isolated) == 1 and title in isolated[0], f"Invalid sheet: {name}"
        if name in {"domestic", "gardener"}:
            assert "Signed:" in isolated[0] and "What we agreed" not in isolated[0]
        page.evaluate("window.dispatchEvent(new Event('afterprint'))")
        assert page.locator(".print-target").count() == 0
    return full


def check_screen(page):
    page.emulate_media(reduced_motion="reduce")
    for width in [320, 390, 768, 1280]:
        page.set_viewport_size({"width": width, "height": 850})
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Overflow at {width}px"
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for index, day in enumerate(days):
        choice = page.get_by_role("radio", name=day, exact=True)
        choice.focus()
        choice.press("Space")
        assert page.locator("#day-board h3").inner_text() == day
        school_run = page.locator("#day-roster tbody tr").nth(index).locator("td").nth(1)
        assert page.locator(".school-run").inner_text() == school_run.inner_text()
    page.set_viewport_size({"width": 320, "height": 800})
    page.get_by_role("link", name="Garden", exact=True).click()
    job = page.locator("#gardener .job-check input").first
    job.check()
    assert job.is_checked()
    job.uncheck()
    page.get_by_role("link", name="Notes", exact=True).click()
    page.get_by_label("From", exact=True).select_option("Lily")
    draft = "Review the second visit together."
    page.get_by_label("Suggested change").fill(draft)
    page.get_by_label("From", exact=True).select_option("Julie")
    assert page.get_by_label("Suggested change").input_value() == ""
    page.get_by_label("From", exact=True).select_option("Lily")
    page.add_init_script("Object.defineProperty(navigator, 'share', {value:data => window.sharedNote = data.text})")
    page.reload()
    assert page.get_by_label("Suggested change").input_value() == draft
    # Capture both platform paths without touching the OS clipboard or sending a message.
    page.evaluate("""Object.defineProperty(navigator, 'clipboard', {
        configurable:true, value:{writeText: text => window.copiedNote = text}
    })""")
    page.locator("#copy-note").click()
    assert page.evaluate("window.copiedNote") == "Maio household planner — Lily\n\n" + draft
    page.locator("#share-note").click()
    assert page.evaluate("window.sharedNote === window.copiedNote")
    page.evaluate("Object.defineProperty(navigator, 'clipboard', {value:undefined})")
    page.locator("#copy-note").click()
    assert page.locator("#note-ready").input_value().endswith(draft)
    assert all(draft not in text for text in page_texts(render(page))), "A private draft appeared in print"
    page.get_by_label("Suggested change").fill("")
    page.reload()
    assert page.get_by_label("Suggested change").input_value() == ""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-pdf", action="store_true")
    args = parser.parse_args()
    with sync_playwright() as driver:
        browser = driver.chromium.launch(channel="chrome")
        page = browser.new_page()
        page.goto(SOURCE.as_uri())
        data = check_print(page)
        check_screen(page)
        # The short public URL must preserve a direct link to a staff sheet.
        destination = "https://targetpraks.github.io/" + SOURCE.name
        page.route(destination, lambda route: route.fulfill(content_type="text/html", body=SOURCE.read_text()))
        page.goto((ROOT / "household.html").as_uri() + "#gardener")
        page.wait_for_url(destination + "#gardener")
        page.wait_for_function("document.querySelector('#gardener h2').getBoundingClientRect().top < 150")
        browser.close()
    if args.write_pdf:
        PDF.write_bytes(data)
    else:
        assert page_texts(PDF.read_bytes()) == page_texts(data), "Regenerate the published PDF"
    print("Verified all seven days, note sharing, the full A4 planner and individual print sheets.")


if __name__ == "__main__":
    main()
