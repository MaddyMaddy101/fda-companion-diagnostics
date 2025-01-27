import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

FDA_URL = (
    "https://www.fda.gov/medical-devices/in-vitro-diagnostics/"
    "list-cleared-or-approved-companion-diagnostic-devices-in-vitro-"
    "and-imaging-tools#table"
)

def scrape_fda_table():
    response = requests.get(FDA_URL)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve page. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    headers = [th.get_text(strip=True) for th in table.find_all("th")]

    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cols = tr.find_all(["td", "th"])
        row_data = []
        for col in cols:
            link = col.find("a")
            if link and link.get("href"):
                cell_content = f'{col.get_text(strip=True)} ({link["href"]})'
            else:
                cell_content = col.get_text(strip=True)
            row_data.append(cell_content)
        rows.append(row_data)

    df = pd.DataFrame(rows, columns=headers)

    return df

def detect_changes(new_file, old_file="fda_companion_diagnostics.csv"):
    if not os.path.exists(old_file):
        return True  # No old file, treat as a change

    old_data = pd.read_csv(old_file)
    if not old_data.equals(new_file):
        return True  # Changes detected

    return False  # No changes detected

if __name__ == "__main__":
    df = scrape_fda_table()

    if detect_changes(df):
        print("Changes detected! Updating the CSV file.")
        df.to_csv("fda_companion_diagnostics.csv", index=False)
    else:
        print("No changes detected.")
