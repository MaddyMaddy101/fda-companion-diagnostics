import streamlit as st
import pandas as pd
import re

# Set the Streamlit page layout to wide to use full screen width
st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    # Load data from CSV
    df = pd.read_csv("fda_companion_diagnostics.csv")

    # Function to extract short name and format links
    def format_link(cell_value):
        if isinstance(cell_value, str) and '(' in cell_value and 'http' in cell_value:
            match = re.match(r'(.+?)\s?\((http[s]?://[^\)]+)\)', cell_value)
            if match:
                short_name, url = match.groups()
                return f'<a href="{url}" target="_blank">{short_name}</a>'
        return cell_value

    # Apply formatting to all cells that may contain links
    df = df.applymap(format_link)

    return df

def main():
    st.title("Multi-Column Filter with Sorting (Wide Layout)")

    df = load_data()

    # Optional: Show the entire raw DataFrame if the user wants
    if st.checkbox("Show raw data"):
        st.markdown(df.to_html(escape=False), unsafe_allow_html=True)

    # Create a row of 5 columns for the filter widgets
    filter_cols = st.columns(5)

    # Step 1: Let each column pick which DataFrame column to filter on
    # Step 2: Let user enter a search term
    selected_columns = []
    search_terms = []

    df_columns = df.columns.tolist()

    # Create 5 filter inputs horizontally
    for i in range(5):
        with filter_cols[i]:
            st.markdown(f"**Filter #{i+1}**")
            col = st.selectbox(
                f"Select column {i+1}", 
                ["(None)"] + df_columns,  # "(None)" means skip this filter
                key=f"col_select_{i}"
            )
            query = st.text_input(
                f"Search {i+1}", 
                key=f"query_{i}"
            )
            selected_columns.append(col)
            search_terms.append(query)

    # Apply filters to get a filtered DataFrame
    filtered_df = df.copy()
    for col_name, term in zip(selected_columns, search_terms):
        if col_name != "(None)" and term:
            filtered_df = filtered_df[
                filtered_df[col_name].str.contains(term, case=False, na=False)
            ]

    # Sorting Dropdowns
    st.markdown("---")
    st.subheader("Sorting Options")
    sort_column = st.selectbox("Select a column to sort by:", df_columns, key="sort_column")
    sort_order = st.radio("Select sort order:", ("Ascending", "Descending"), key="sort_order")

    # Apply sorting
    if sort_column:
        filtered_df = filtered_df.sort_values(
            by=sort_column,
            ascending=(sort_order == "Ascending"),
            ignore_index=True
        )

    # Display the final table with rendered links
    st.markdown("---")
    st.subheader("Filtered and Sorted Results")
    st.write(f"Showing {len(filtered_df)} records after all filters:")
    st.markdown(filtered_df.to_html(escape=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
