import streamlit as st
import pandas as pd
from src import visualizations
from streamlit_folium import st_folium

def display_species_panel(df):
    st.title("Species Insights Panel")
    st.write("Deep dive into specific species.")
    
    # Species Selector
    if df.empty:
        st.warning("No data available for the current filters.")
        return

    # Hierarchical Selection to group similar species
    st.markdown("### Select Species")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Kingdom
        kingdoms = ["All"] + sorted(df['kingdom_grouped'].unique().tolist())
        selected_kingdom = st.selectbox("Kingdom", kingdoms, key="species_kingdom")
        
    with col2:
        # Family (filtered by Kingdom)
        if selected_kingdom != "All":
            families = ["All"] + sorted(df[df['kingdom_grouped'] == selected_kingdom]['family'].unique().tolist())
        else:
            families = ["All"] + sorted(df['family'].unique().tolist()) if 'family' in df.columns else []
        selected_family = st.selectbox("Family", families, key="species_family")
        
    with col3:
        # Genus (filtered by Family)
        if selected_family != "All":
            genera = ["All"] + sorted(df[df['family'] == selected_family]['genus'].unique().tolist())
        elif selected_kingdom != "All":
            genera = ["All"] + sorted(df[df['kingdom_grouped'] == selected_kingdom]['genus'].unique().tolist())
        else:
            genera = ["All"] + sorted(df['genus'].unique().tolist())
        selected_genus = st.selectbox("Genus", genera, key="species_genus")
        
    # Species (filtered by Genus)
    filtered_df = df.copy()
    if selected_kingdom != "All":
        filtered_df = filtered_df[filtered_df['kingdom_grouped'] == selected_kingdom]
    if selected_family != "All":
        filtered_df = filtered_df[filtered_df['family'] == selected_family]
    if selected_genus != "All":
        filtered_df = filtered_df[filtered_df['genus'] == selected_genus]
        
    species_list = sorted(filtered_df['species'].unique().tolist())
    selected_species = st.selectbox("Species", species_list, key="species_selector")
    
    if not selected_species:
        return
        
    # Filter data for selected species
    species_df = df[df['species'] == selected_species]
    
    # 1. Taxonomy Info
    st.subheader("Taxonomic Classification")
    first_row = species_df.iloc[0]
    taxonomy_cols = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    taxonomy_info = {col: first_row[col] for col in taxonomy_cols if col in species_df.columns}
    
    cols = st.columns(len(taxonomy_info))
    for i, (rank, name) in enumerate(taxonomy_info.items()):
        with cols[i]:
            st.metric(rank.capitalize(), name)
            
    st.markdown("---")
    
    # 2. Key Metrics for Species
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Observations", len(species_df))
    with col2:
        if 'countryCode' in species_df.columns:
            st.metric("Countries Found In", species_df['countryCode'].nunique())
    with col3:
        if 'event_year' in species_df.columns:
            min_year = int(species_df['event_year'].min())
            max_year = int(species_df['event_year'].max())
            st.metric("Year Range", f"{min_year} - {max_year}")

    # 3. Map
    st.subheader(f"Distribution of {selected_species}")
    map_type = st.radio("Map Type", ["Folium (Markers)", "Plotly (Scatter)"], horizontal=True, key="species_map_type")
    
    if map_type == "Folium (Markers)":
        m = visualizations.plot_folium_map(species_df, map_type="Markers")
        if m:
            st_folium(m, width=None, height=500)
        else:
            st.warning("No coordinates available.")
    else:
        fig = visualizations.plot_plotly_map(species_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No coordinates available.")

    # 4. Timeline
    st.subheader("Observation Timeline")
    fig_timeline = visualizations.plot_observations_per_year(species_df)
    if fig_timeline:
        st.pyplot(fig_timeline)
        
    # 5. Image Panel / Observation Links
    st.subheader("Observation Gallery")
    st.write("Browse individual observations. If 'mediaType' indicates an image, it might be viewable on the source site.")
    
    # Filter for records with images if possible, or just show all
    with_images = species_df[species_df['mediaType'].str.contains('StillImage', na=False)] if 'mediaType' in species_df.columns else pd.DataFrame()
    
    if not with_images.empty:
        st.write(f"Found {len(with_images)} observations with images reported.")
        display_df = with_images
    else:
        st.write("No observations explicitly marked as having images. Showing all records.")
        display_df = species_df
        
    # Pagination for gallery
    page_size = 6
    if len(display_df) > page_size:
        page = st.number_input("Page", min_value=1, max_value=(len(display_df) // page_size) + 1, value=1)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        subset = display_df.iloc[start_idx:end_idx]
    else:
        subset = display_df
        
    # Display cards
    cols = st.columns(3)
    for i, (index, row) in enumerate(subset.iterrows()):
        with cols[i % 3]:
            with st.container(border=True):
                st.write(f"**Date:** {row.get('eventDate', 'Unknown')}")
                st.write(f"**Location:** {row.get('countryCode', 'Unknown')}, {row.get('stateProvince', 'Unknown')}")
                
                if 'occurrenceID' in row and pd.notna(row['occurrenceID']):
                    link = row['occurrenceID']
                    st.link_button("View Observation", link)
                    
                    # Optional: Try to embed if it's a direct image link (unlikely for occurrenceID, usually a page)
                    # If we had a direct image URL column, we would use st.image(row['imageUrl'])
                    # Since occurrenceID is a page, we can try iframe but many sites block it.
                    # Let's just provide the link for safety and better UX than a broken iframe.
                else:
                    st.write("No Link Available")
