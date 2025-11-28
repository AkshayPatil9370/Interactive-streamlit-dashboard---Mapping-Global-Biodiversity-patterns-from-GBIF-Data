import streamlit as st

import streamlit as st

def sidebar(df):
    st.sidebar.title("Biodiversity Dashboard")
    st.sidebar.markdown("## Navigation")
    
    pages = {
        "Overview": "1_overview",
        "Taxonomy": "2_taxonomy",
        "Temporal Analysis": "3_temporal",
        "Spatial Analysis": "4_spatial",
        "Species Insights": "5_species",
        "Distribution": "6_distribution",
        "Additional Analysis": "7_analysis",
        "Observations by Year": "8_yearly_observations",
        "Date Search": "9_date_search",
        "Raw Data": "10_raw_data"
    }
    
    selection = st.sidebar.selectbox("Select a page:", list(pages.keys()))
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Filters")
    
    # Kingdom Filter
    kingdoms = ["All"] + sorted(df['kingdom_grouped'].unique().tolist())
    selected_kingdom = st.sidebar.selectbox("Select Kingdom", kingdoms)

    # Phylum Filter
    if selected_kingdom != "All":
        phyla = ["All"] + sorted(df[df['kingdom_grouped'] == selected_kingdom]['phylum'].unique().tolist())
    else:
        phyla = ["All"] + sorted(df['phylum'].unique().tolist())
    selected_phylum = st.sidebar.selectbox("Select Phylum", phyla)

    # Country Filter
    countries = ["All"] + sorted(df['countryCode'].unique().tolist())
    selected_country = st.sidebar.selectbox("Select Country", countries)

    # State Filter
    if selected_country != "All":
        states = ["All"] + sorted(df[df['countryCode'] == selected_country]['stateProvince'].unique().tolist())
    else:
        states = ["All"] + sorted(df['stateProvince'].unique().tolist())
    selected_state = st.sidebar.selectbox("Select State/Province", states)
    
    # Year Filter
    if 'event_year' in df.columns:
        min_year = int(df['event_year'].min())
        max_year = int(df['event_year'].max())
        selected_year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))
    else:
        selected_year_range = None

    # Additional Filters
    st.sidebar.markdown("### Advanced Filters")
    has_image = st.sidebar.checkbox("Only records with images", value=False)
    valid_coords = st.sidebar.checkbox("Only valid coordinates", value=False)
    
    # Observation Count Threshold (for species)
    # This might be too heavy to filter the main dataframe by species count dynamically here, 
    # but we can pass it as a parameter.
    # Let's add a simple slider for "Minimum Observations per Species" if needed, 
    # but for now, let's stick to record-level filters to keep it fast.
    
    filters = {
        "kingdom": selected_kingdom,
        "phylum": selected_phylum,
        "country": selected_country,
        "state": selected_state,
        "year_range": selected_year_range,
        "has_image": has_image,
        "valid_coords": valid_coords
    }
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("Created by **Akshay Patil**")
    
    return selection, filters