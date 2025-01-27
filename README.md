# fda-companion-diagnostics
filter approved devices
Step-by-Step Guide to Create and Deploy Your Project Directly on GitHub
Step 1: Create a GitHub Repository
Go to GitHub.
Sign in or create an account.
Click on "New Repository" (or go to https://github.com/new).
Enter a repository name, e.g., fda-companion-diagnostics.
Choose Public or Private (Streamlit Cloud works with both).
Check "Add a README file" (optional, but useful).
Click "Create repository".
Step 2: Add scrape.py (Scraper Code)
In your newly created repository, click "Add file" > "Create new file".
Name the file scrape.py.
Copy and paste the following scraping code:
python
Copy
Edit
import requests
from bs4 import BeautifulSoup
import pandas as pd

FDA_URL = "https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-cleared-or-approved-companion-diagnostic-devices-in-vitro-and-imaging-tools#table"

def scrape_fda_table():
    # Fetch the webpage
    response = requests.get(FDA_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the relevant table
    table = soup.find("table")
    headers = [th.get_text(strip=True) for th in table.find_all("th")]

    rows = []
    for tr in table.find("tbody").find_all("tr"):
        cols = tr.find_all(["td", "th"])
        row_data = [col.get_text(strip=True) for col in cols]
        rows.append(row_data)

    df = pd.DataFrame(rows, columns=headers)

    # Save data to CSV for the Streamlit app to read
    df.to_csv("fda_companion_diagnostics.csv", index=False)
    print("Data scraped and saved successfully.")

if __name__ == "__main__":
    scrape_fda_table()
Scroll down, add a commit message like Added scrape.py, and click "Commit new file".
Step 3: Add app.py (Streamlit App Code)
Click "Add file" > "Create new file" again.
Name the file app.py.
Copy and paste the following Streamlit code:
python
Copy
Edit
import streamlit as st
import pandas as pd

# Configure wide layout
st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("fda_companion_diagnostics.csv")

def main():
    st.title("FDA Companion Diagnostics Explorer (Updated Daily)")

    df = load_data()

    # Show raw data option
    if st.checkbox("Show raw data"):
        st.dataframe(df, use_container_width=True)

    filter_cols = st.columns(5)
    selected_columns = []
    search_terms = []
    df_columns = df.columns.tolist()

    # Create 5 filter inputs horizontally
    for i in range(5):
        with filter_cols[i]:
            st.markdown(f"**Filter #{i+1}**")
            col = st.selectbox(f"Select column {i+1}", ["(None)"] + df_columns, key=f"col_select_{i}")
            query = st.text_input(f"Search {i+1}", key=f"query_{i}")
            selected_columns.append(col)
            search_terms.append(query)

    # Apply all 5 filters
    filtered_df = df.copy()
    for col_name, term in zip(selected_columns, search_terms):
        if col_name != "(None)" and term:
            filtered_df = filtered_df[filtered_df[col_name].str.contains(term, case=False, na=False)]

    # Display final filtered results
    st.markdown("---")
    st.subheader("Filtered Results")
    st.write(f"Showing {len(filtered_df)} records after all filters:")
    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
Scroll down, add a commit message like Added app.py, and click "Commit new file".
Step 4: Add requirements.txt (Dependencies File)
Click "Add file" > "Create new file".
Name it requirements.txt.
Add the following dependencies:
Copy
Edit
streamlit
pandas
beautifulsoup4
requests
Commit the file.
Step 5: Deploy the App on Streamlit Cloud
Go to Streamlit Cloud.
Sign in using GitHub.
Click "New App".
Select your newly created repository.
Choose the branch (main) and set app.py as the entry point.
Click "Deploy".
Your Streamlit app will be hosted, and a public URL will be provided (e.g., https://yourname-yourrepo.streamlit.app).

Step 6: Automate Scraping Using GitHub Actions
GitHub Actions can run scrape.py daily to fetch fresh data and push it to the repository.

In your repository, click "Add file" > "Create new file".
Name the file .github/workflows/scraper.yml.
Add the following code to run the scraper every day at midnight:
yaml
Copy
Edit
name: Daily Scraper

on:
  schedule:
    - cron: '0 0 * * *'  # Runs every day at midnight UTC
  workflow_dispatch:  # Allows manual triggering

jobs:
  run-scraper:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repo
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run scraper script
      run: python scrape.py

    - name: Commit and push CSV
      run: |
        git config --global user.name "github-actions[bot]"
        git config --global user.email "github-actions[bot]@users.noreply.github.com"
        git add fda_companion_diagnostics.csv
        git commit -m "Updated FDA data"
        git push
Commit the file.
Step 7: Confirm Deployment and Automation
Go to the "Actions" tab in your GitHub repository and ensure the scraper is running as scheduled.
Visit your Streamlit app link to confirm that it reflects the latest data.
Optionally, you can trigger the workflow manually from the "Actions" tab to test it.
Summary of What You've Done
Created all code files (scrape.py, app.py, requirements.txt) directly on GitHub.
Deployed your Streamlit app to Streamlit Cloud.
Set up GitHub Actions to scrape daily and update the CSV file.
Streamlit Cloud always serves the latest data whenever accessed.
Optional Enhancements
Add email notifications to the GitHub Action if scraping fails.
Use logging to track scraping success and failure.
Deploy to other platforms like Heroku, AWS, or Render if needed.
