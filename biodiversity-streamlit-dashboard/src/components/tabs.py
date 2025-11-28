import streamlit as st
from src import metrics
from src import visualizations
import matplotlib.pyplot as plt


def display_overview_tab(df):
    st.title("Biodiversity Dashboard Overview")
    
    st.markdown("""
    ### Dataset Description
    This dashboard provides an interactive exploration of biodiversity data from GBIF. 
    It includes observations of various species across different kingdoms, phyla, and locations.
    Use the sidebar filters to customize the view and explore specific segments of the data.
    """)
    
    st.markdown("---")
    st.subheader("Key Metrics")
    
    # Row 1
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Observations", f"{len(df):,}")
    with col2:
        st.metric("Total Species", f"{metrics.species_count(df):,}")
    with col3:
        st.metric("Total Genera", f"{metrics.genera_count(df):,}")
    with col4:
        st.metric("Total Families", f"{metrics.families_count(df):,}")
        
    # Row 2
    col5, col6, col7 = st.columns(3)
    with col5:
        if 'countryCode' in df.columns:
            st.metric("Countries Represented", f"{df['countryCode'].nunique():,}")
    with col6:
        st.metric("Unique Observers", f"{metrics.observers_count(df):,}")
    with col7:
        st.metric("Observations with Images", f"{metrics.images_count(df):,}")

    st.markdown("---")
    st.subheader("Quick Visualizations")
    
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Kingdom Distribution")
        fig = visualizations.plot_kingdom_distribution(df)
        if fig is not None:
            st.pyplot(fig)
            
    with c2:
        st.write("### Top Phyla")
        fig = visualizations.plot_top_phyla(df)
        if fig is not None:
            st.pyplot(fig)


def display_taxonomy_tab(df):
    st.title("Taxonomy Explorer")
    st.write("Explore the taxonomic hierarchy and distribution of species.")
    
    # Drill-down filters specific to this tab
    st.markdown("### Drill-Down Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        classes = ["All"] + sorted(df['class'].unique().tolist()) if 'class' in df.columns else []
        selected_class = st.selectbox("Select Class", classes)
    
    with col2:
        if selected_class != "All":
            orders = ["All"] + sorted(df[df['class'] == selected_class]['order'].unique().tolist())
        else:
            orders = ["All"] + sorted(df['order'].unique().tolist()) if 'order' in df.columns else []
        selected_order = st.selectbox("Select Order", orders)
        
    with col3:
        if selected_order != "All":
            families = ["All"] + sorted(df[df['order'] == selected_order]['family'].unique().tolist())
        elif selected_class != "All":
            families = ["All"] + sorted(df[df['class'] == selected_class]['family'].unique().tolist())
        else:
            families = ["All"] + sorted(df['family'].unique().tolist()) if 'family' in df.columns else []
        selected_family = st.selectbox("Select Family", families)

    # Apply local filters
    filtered_df = df.copy()
    if selected_class != "All":
        filtered_df = filtered_df[filtered_df['class'] == selected_class]
    if selected_order != "All":
        filtered_df = filtered_df[filtered_df['order'] == selected_order]
    if selected_family != "All":
        filtered_df = filtered_df[filtered_df['family'] == selected_family]
        
    st.markdown(f"**Showing {len(filtered_df)} observations**")
    st.markdown("---")

    # Visualizations
    st.subheader("Taxonomic Hierarchy")
    st.write("Interactive Sunburst Chart (Click to expand)")
    fig_sunburst = visualizations.plot_sunburst(filtered_df)
    if fig_sunburst:
        st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.info("Not enough data for Sunburst chart.")

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top 10 Genera")
        fig_genera = visualizations.plot_top_genera(filtered_df)
        if fig_genera:
            st.pyplot(fig_genera)
            
    with c2:
        st.subheader("Top 10 Species")
        fig_species = visualizations.plot_top_species(filtered_df)
        if fig_species:
            st.pyplot(fig_species)
            
    st.markdown("---")
    st.subheader("Distribution by Kingdom")
    fig_pie = visualizations.plot_taxonomy_pie(filtered_df, 'kingdom_grouped')
    if fig_pie:
        st.plotly_chart(fig_pie, use_container_width=True)


def display_temporal_tab(df):
    st.title("Temporal Analysis")
    st.write("Analyze temporal trends and seasonal patterns.")
    
    st.subheader("Yearly Trends")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Observations per Year")
        fig_year = visualizations.plot_observations_per_year(df)
        if fig_year:
            st.pyplot(fig_year)
            
    with col2:
        st.write("### Kingdom Trends Over Time")
        fig_kingdom = visualizations.plot_kingdom_over_time(df)
        if fig_kingdom:
            st.plotly_chart(fig_kingdom, use_container_width=True)
            
    st.markdown("---")
    st.subheader("Seasonal Patterns")
    col3, col4 = st.columns(2)
    with col3:
        st.write("### Observations per Month")
        fig_month = visualizations.plot_observations_per_month(df)
        if fig_month:
            st.pyplot(fig_month)
            
    with col4:
        st.write("### Month vs Year Heatmap")
        fig_heatmap = visualizations.plot_month_year_heatmap(df)
        if fig_heatmap:
            st.pyplot(fig_heatmap)


from streamlit_folium import st_folium

def display_spatial_tab(df):
    st.title("Geographic Mapping")
    st.write("Explore the spatial distribution of observations.")
    
    # Map Type Selection
    map_provider = st.radio("Select Map Provider", ["Folium (Interactive)", "Plotly (Global View)"], horizontal=True)
    
    if map_provider == "Folium (Interactive)":
        map_style = st.selectbox("Select Map Style", ["Cluster", "Heatmap", "Markers"])
        st.write(f"Displaying {map_style} Map. (Note: Markers are capped for performance)")
        
        folium_map = visualizations.plot_folium_map(df, map_type=map_style)
        if folium_map:
            st_folium(folium_map, width=None, height=500, returned_objects=[])
        else:
            st.warning("No valid coordinates found for the current selection.")
            
    else:
        st.write("Displaying Global Scatter Map.")
        plotly_map = visualizations.plot_plotly_map(df)
        if plotly_map:
            st.plotly_chart(plotly_map, use_container_width=True)
        else:
            st.warning("No valid coordinates found for the current selection.")

    st.markdown("---")
    st.subheader("Species Richness by Latitude")
    fig_lat = visualizations.plot_species_richness(df)
    if fig_lat:
        st.pyplot(fig_lat)


def display_distribution_tab(df):
    st.title("Distribution Metrics")
    st.write("This tab displays distribution metrics by country and state.")
    fig = visualizations.plot_top_countries(df)
    if fig is not None:
        st.pyplot(fig)
    fig = visualizations.plot_top_states(df)
    if fig is not None:
        st.pyplot(fig)


def display_analysis_tab(df):
    st.title("Advanced Analysis")
    st.write("Deep dive into correlations and biodiversity patterns.")
    
    st.subheader("Correlation Matrix")
    fig_corr = visualizations.plot_correlation_heatmap(df)
    if fig_corr:
        st.pyplot(fig_corr)
    else:
        st.info("Not enough numerical data for correlation analysis.")
        
    st.markdown("---")
    st.subheader("Biodiversity Patterns")
    
    st.write("### Species Richness vs Latitude")
    fig_lat = visualizations.plot_species_richness(df)
    if fig_lat:
        st.pyplot(fig_lat)
        
    st.markdown("---")
    st.subheader("Regional Richness")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Species Richness by Country")
        fig_country = visualizations.plot_country_richness(df)
        if fig_country:
            st.pyplot(fig_country)
            
    with col2:
        st.write("### Species Richness by State")
        fig_state = visualizations.plot_state_richness(df)
        if fig_state:
            st.pyplot(fig_state)



def display_yearly_observations_tab(df):
    st.title("Observations by Year")
    st.write("Total number of observations for each year.")

    if 'event_year' not in df.columns:
        st.error("Year data not available.")
        return

    # Group by year and count
    yearly_counts = df['event_year'].value_counts().sort_index().reset_index()
    yearly_counts.columns = ['Year', 'Observations']
    
    # Ensure Year is integer for display
    yearly_counts['Year'] = yearly_counts['Year'].astype(int)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Graph")
        # Using matplotlib for consistency with other tabs, or st.line_chart for simplicity
        # Let's use st.line_chart for a quick interactive chart
        st.line_chart(yearly_counts.set_index('Year'))
    
    with col2:
        st.subheader("Table")
        st.dataframe(yearly_counts, hide_index=True)


def display_raw_data_tab(df):
    st.title("Raw Data")
    st.write("This tab displays the raw data based on current filters.")
    st.write(f"Total records: {len(df)}")
    st.dataframe(df)





from src.components import species_panel
from src.components import date_search

def main(selected, df):
    tabs = {
        "Overview": display_overview_tab,
        "Taxonomy": display_taxonomy_tab,
        "Temporal Analysis": display_temporal_tab,
        "Spatial Analysis": display_spatial_tab,
        "Species Insights": species_panel.display_species_panel,
        "Distribution": display_distribution_tab,
        "Additional Analysis": display_analysis_tab,
        "Observations by Year": display_yearly_observations_tab,
        "Date Search": date_search.display_date_search_tab,
        "Raw Data": display_raw_data_tab
    }

    # Fallback to Overview
    if selected not in tabs:
        selected = "Overview"

    tabs[selected](df)


if __name__ == "__main__":
    # simple local run for development
    import pandas as pd
    # Mock data for testing
    df = pd.DataFrame({'species': ['A', 'B'], 'gbifID': [1, 2]})
    main('Overview', df)