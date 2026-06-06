import sqlite3
import time
import random
from datetime import date
from playwright.sync_api import sync_playwright

print("🚀 script started")
print("scraper running")

URL = "https://www.merolagani.com/MarketSummary.aspx"


# 🟢 Human-like delay (prevents bot detection)
def human_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))


# 🟢 Create database if not exists
def init_db():
    conn = sqlite3.connect("nepse.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS market_leaders (
        date TEXT,
        symbol TEXT,
        category TEXT,
        rank INTEGER,
        value TEXT
    )
    """)
    conn.commit()
    conn.close()


def run_scraper():

    init_db()
    today = str(date.today())

    conn = sqlite3.connect("nepse.db")

    with sync_playwright() as p:

        # 🟢 stealth-style browser settings
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            viewport={"width": 1366, "height": 768}
        )

        page = context.new_page()

        page.goto(URL, wait_until="domcontentloaded")

        # 🟢 human delay after page load
        human_delay(2, 4)

        page.wait_for_timeout(3000)

        tables = page.locator("table")

        print("📊 Tables found:", tables.count())

        if tables.count() < 6:
            print("❌ Not enough tables found. Scraper might have failed.")
            browser.close()
            conn.close()
            return

        turnover = tables.nth(2)
        gainers = tables.nth(4)
        losers = tables.nth(5)

        # 🟢 TURNOVER
        for i, row in enumerate(turnover.locator("tr").all()[1:]):
            cols = row.locator("td").all_text_contents()

            if len(cols) >= 2:
                conn.execute(
                    "INSERT INTO market_leaders VALUES (?, ?, ?, ?, ?)",
                    (today, cols[0], "turnover", i + 1, cols[1])
                )

        human_delay(1, 2)

        # 🟢 GAINERS
        for i, row in enumerate(gainers.locator("tr").all()[1:]):
            cols = row.locator("td").all_text_contents()

            if len(cols) >= 3:
                conn.execute(
                    "INSERT INTO market_leaders VALUES (?, ?, ?, ?, ?)",
                    (today, cols[0], "gainer", i + 1, cols[2])
                )

        human_delay(1, 2)

        # 🟢 LOSERS
        for i, row in enumerate(losers.locator("tr").all()[1:]):
            cols = row.locator("td").all_text_contents()

            if len(cols) >= 3:
                conn.execute(
                    "INSERT INTO market_leaders VALUES (?, ?, ?, ?, ?)",
                    (today, cols[0], "loser", i + 1, cols[2])
                )

        conn.commit()
        conn.close()

        browser.close()

        print("✅ scraping completed successfully")


if __name__ == "__main__":
    run_scraper()