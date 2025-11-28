import streamlit as st
import pandas as pd

def display_date_search_tab(df):
    st.title("Date Search")
    st.write("Search for observations on a specific date.")
    
    if df.empty:
        st.warning("No data available.")
        return

    # Date Input Widgets
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get unique years from data if possible, else default range
        if 'event_year' in df.columns:
            years = sorted(df['event_year'].dropna().unique().astype(int).tolist(), reverse=True)
        else:
            years = list(range(2023, 1900, -1))
        selected_year = st.selectbox("Year", years)
        
    with col2:
        months = list(range(1, 13))
        selected_month = st.selectbox("Month", months)
        
    with col3:
        days = list(range(1, 32))
        selected_day = st.selectbox("Day", days)
        
    # Search Button
    if st.button("Search Observations"):
        # Filter Logic
        # Assuming columns: event_year, event_month, event_day exist and are numeric
        # If not, we might need to parse eventDate
        
        mask = (df['event_year'] == selected_year) & \
               (df['event_month'] == selected_month) & \
               (df['event_day'] == selected_day)
               
        results = df[mask]
        
        if not results.empty:
            st.success(f"Found {len(results)} observations on {selected_year}-{selected_month}-{selected_day}.")
            
            # Display Results Table
            # Select relevant columns
            cols_to_show = ['species', 'kingdom', 'countryCode', 'eventDate', 'occurrenceID']
            # Ensure columns exist
            cols_to_show = [c for c in cols_to_show if c in results.columns]
            
            display_df = results[cols_to_show].copy()
            
            # Make occurrenceID clickable
            # Streamlit dataframe with column config can handle links
            
            st.dataframe(
                display_df,
                column_config={
                    "occurrenceID": st.column_config.LinkColumn(
                        "Source Link",
                        help="Click to view observation on source website",
                        validate="^http",
                        display_text="View Observation"
                    )
                },
                hide_index=True,
                use_container_width=True
            )
            
        else:
            st.info(f"No observations found on {selected_year}-{selected_month}-{selected_day}.")
