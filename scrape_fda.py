# scrape_fda.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

FDA_URL = (
    "https://www.fda.gov/medical-devices/in-vitro-diagnostics/"
    "list-cleared-or-approved-companion-diagnostic-devices-in-vitro-"
    "and-imaging-tools#table"
)

def scrape_fda_table():
    # 1. Fetch the webpage
    response = requests.get(FDA_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve page. Status code: {response.status_code}")

    # 2. Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # 3. Locate the specific table
    #    If there's only one main table, soup.find("table") might suffice.
    #    Otherwise, refine with attributes like ID/class if needed.
    table = soup.find("table")

    # 4. Extract table headers
    headers = [th.get_text(strip=True) for th in table.find_all("th")]

    # 5. Extract rows (table body)
    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cols = tr.find_all(["td", "th"])
        row_data = [col.get_text(strip=True) for col in cols]
        rows.append(row_data)

    # 6. Create a pandas DataFrame
    df = pd.DataFrame(rows, columns=headers)

    return df

if __name__ == "__main__":
    df = scrape_fda_table()
    print(df.head())  # For debugging
    # Save to CSV or do additional processing
    df.to_csv("fda_companion_diagnostics.csv", index=False)
