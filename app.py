import streamlit as st
import pandas as pd

# Set the Streamlit page layout to wide to use full screen width
st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    # Load data from CSV
    df = pd.read_csv("fda_companion_diagnostics.csv")

    # Check for link-containing columns and format them with hidden URLs
    for column in df.columns:
        if df[column].dtype == object and df[column].str.contains("http").any():
            df[column] = df[column].apply(lambda x: f'<a href="{x}" target="_blank">Click here</a>'
                                          if isinstance(x, str) and "http" in x else x)
    
    return df

def main():
    st.title("Multi-Column Filter with One Result Table (Wide Layout)")

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

    # Apply filters to get a final DataFrame
    filtered_df = df.copy()

    for col_name, term in zip(selected_columns, search_terms):
        if col_name != "(None)" and term:
            filtered_df = filtered_df[
                filtered_df[col_name].str.contains(term, case=False, na=False)
            ]

    # Display one final table with rendered links
    st.markdown("---")
    st.subheader("Filtered Results")
    st.write(f"Showing {len(filtered_df)} records after all filters:")
    st.markdown(filtered_df.to_html(escape=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
