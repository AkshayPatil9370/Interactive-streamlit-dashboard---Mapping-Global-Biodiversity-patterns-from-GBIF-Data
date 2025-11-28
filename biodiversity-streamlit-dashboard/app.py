import streamlit as st
from pathlib import Path
from src.data_loader import load_and_clean_data
from src.components.sidebar import sidebar
from src.components import tabs


def main():
    st.set_page_config(page_title="Biodiversity Dashboard", layout="wide")

    # Load Custom CSS
    css_path = Path(__file__).parent / "src" / "assets" / "style.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    data_path = Path(__file__).parent / "data" / "gbif_cleaned.csv"
    
    # Check if file exists
    if not data_path.exists():
        st.error(f"Data file not found at {data_path}. Please ensure the data is present.")
        return

    with st.spinner("Loading data..."):
        df = load_and_clean_data(str(data_path))

    # Sidebar returns the selected page name and filters
    selected, filters = sidebar(df)

    # Apply filters
    if filters["kingdom"] != "All":
        df = df[df["kingdom_grouped"] == filters["kingdom"]]
    
    if filters["phylum"] != "All":
        df = df[df["phylum"] == filters["phylum"]]

    if filters["country"] != "All":
        df = df[df["countryCode"] == filters["country"]]
    
    if filters["state"] != "All":
        df = df[df["stateProvince"] == filters["state"]]
        
    if filters["year_range"]:
        df = df[(df["event_year"] >= filters["year_range"][0]) & (df["event_year"] <= filters["year_range"][1])]
        
    if filters["has_image"]:
        # Assuming mediaType contains 'StillImage' for images
        df = df[df['mediaType'].str.contains('StillImage', na=False)]
        
    if filters["valid_coords"]:
        df = df.dropna(subset=['decimalLatitude', 'decimalLongitude'])

    # Display the selected tab, passing the dataframe
    tabs.main(selected, df)


if __name__ == "__main__":
    main()