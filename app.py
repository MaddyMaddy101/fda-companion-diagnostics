import streamlit as st
import pandas as pd

# Set the Streamlit page layout to wide to use full screen width
st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    # Replace this with your actual data or CSV
    return pd.read_csv("fda_companion_diagnostics.csv")

def main():
    st.title("Multi-Column Filter with One Result Table (Wide Layout)")

    df = load_data()

    # Optional: Show the entire raw DataFrame if the user wants
    if st.checkbox("Show raw data"):
        st.dataframe(df, use_container_width=True)

    # We'll apply the filters sequentially, but only display one final table

    # Create a row of 5 columns for the filter widgets
    filter_cols = st.columns(5)

    # Step 1: Let each column pick which DataFrame column to filter on
    # Step 2: Let user enter a search term
    # We'll store these in lists so we can iterate and apply them
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

    # Now apply all 5 filters to get a final DataFrame
    filtered_df = df.copy()

    for col_name, term in zip(selected_columns, search_terms):
        if col_name != "(None)" and term:
            # Filter rows where 'col_name' contains 'term' (case-insensitive)
            filtered_df = filtered_df[
                filtered_df[col_name].str.contains(term, case=False, na=False)
            ]

    # Display one final table with the combined results
    st.markdown("---")
    st.subheader("Filtered Results")
    st.write(f"Showing {len(filtered_df)} records after all filters:")
    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
