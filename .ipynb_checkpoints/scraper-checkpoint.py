

import sqlite3
from datetime import date
from playwright.sync_api import sync_playwright

print("🚀 script started")
print("scraper running")

URL = "https://www.merolagani.com/MarketSummary.aspx"

import sqlite3

print("🌐 starting scraping")

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
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        tables = page.locator("table")

        print(tables.nth(2).inner_text()[:200])

        print("📊 Tables found:", tables.count())

        turnover = tables.nth(2)
        gainers = tables.nth(4)
        losers = tables.nth(5)

        # TURNOVER
        for i, row in enumerate(turnover.locator("tr").all()[1:]):
            cols = row.locator("td").all_text_contents()
            if len(cols) >= 2:
                conn.execute(
                    "INSERT INTO market_leaders VALUES (?, ?, ?, ?, ?)",
                    (today, cols[0], "turnover", i+1, cols[1])
                )

        # GAINERS
        for i, row in enumerate(gainers.locator("tr").all()[1:]):
            cols = row.locator("td").all_text_contents()
            if len(cols) >= 3:
                conn.execute(
                    "INSERT INTO market_leaders VALUES (?, ?, ?, ?, ?)",
                    (today, cols[0], "gainer", i+1, cols[2])
                )

        # LOSERS
        for i, row in enumerate(losers.locator("tr").all()[1:]):
            cols = row.locator("td").all_text_contents()
            if len(cols) >= 3:
                conn.execute(
                    "INSERT INTO market_leaders VALUES (?, ?, ?, ?, ?)",
                    (today, cols[0], "loser", i+1, cols[2])
                )

        conn.commit()
        conn.close()

        browser.close()

if __name__ == "__main__":
    run_scraper()