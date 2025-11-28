import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def plot_kingdom_distribution(df):
    if df.empty:
        return None
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='kingdom_grouped', order=df['kingdom_grouped'].value_counts().index)
    plt.title("Distribution of Observations by Kingdom")
    plt.xticks(rotation=30)
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_top_phyla(df, top_n=10):
    if df.empty:
        return None
    top_phyla = df['phylum'].value_counts().head(top_n)
    if top_phyla.empty:
        return None
    plt.figure(figsize=(8, 5))
    sns.barplot(x=top_phyla.values, y=top_phyla.index)
    plt.title(f"Top {top_n} Most Common Phyla")
    plt.xlabel("Count")
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_top_orders(df):
    if df.empty:
        return None
    top_orders = df['order'].value_counts().head(10)
    if top_orders.empty:
        return None
    plt.figure(figsize=(8, 5))
    sns.barplot(x=top_orders.values, y=top_orders.index)
    plt.title("Top 10 Orders")
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_species_richness(df):
    if df.empty or 'decimalLatitude' not in df.columns or 'species' not in df.columns:
        return None
    lat_richness = df.groupby('decimalLatitude')['species'].nunique()
    if lat_richness.empty:
        return None
    plt.figure(figsize=(10, 5))
    plt.scatter(lat_richness.index, lat_richness.values, alpha=0.6)
    plt.title("Species Richness Across Latitude")
    plt.xlabel("Latitude")
    plt.ylabel("Unique Species Count")
    plt.grid(True)
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_observations_per_year(df):
    if df.empty or 'event_year' not in df.columns:
        return None
    yearly_counts = df['event_year'].value_counts().sort_index()
    if yearly_counts.empty:
        return None
    plt.figure(figsize=(10, 5))
    plt.plot(yearly_counts.index, yearly_counts.values, marker='o')
    plt.title("Observations per Year")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.grid(True)
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_observations_per_month(df):
    if df.empty or 'event_month' not in df.columns:
        return None
    monthly_counts = df['event_month'].value_counts().sort_index()
    if monthly_counts.empty:
        return None
    plt.figure(figsize=(10, 5))
    sns.barplot(x=monthly_counts.index, y=monthly_counts.values)
    plt.title("Seasonality: Observations per Month")
    plt.xlabel("Month")
    plt.ylabel("Count")
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_top_countries(df):
    if df.empty or 'countryCode' not in df.columns:
        return None
    top_countries = df['countryCode'].value_counts().head(15)
    if top_countries.empty:
        return None
    plt.figure(figsize=(8, 6))
    sns.barplot(x=top_countries.values, y=top_countries.index)
    plt.title("Top 15 Countries by Observation Count")
    plt.xlabel("Count")
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_top_states(df):
    if df.empty or 'stateProvince' not in df.columns:
        return None
    top_states = df['stateProvince'].value_counts().head(15)
    if top_states.empty:
        return None
    plt.figure(figsize=(8, 6))
    sns.barplot(x=top_states.values, y=top_states.index)
    plt.title("Top 15 States/Provinces by Observation Count")
    plt.xlabel("Count")
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_correlation_heatmap(df):
    if df.empty:
        return None
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    if numeric_df.shape[1] < 2:
        return None
    plt.figure(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=False, cmap='coolwarm')
    plt.title("Correlation Heatmap for Numerical Variables")
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig


def plot_sunburst(df):
    if df.empty:
        return None
    # Hierarchy: Kingdom -> Phylum -> Class -> Order
    # Group by these columns and count
    cols = ['kingdom', 'phylum', 'class', 'order']
    # Ensure columns exist
    valid_cols = [c for c in cols if c in df.columns]
    if not valid_cols:
        return None
        
    # Limit data for performance if needed, but sunburst handles aggregation well.
    # However, too many nodes can be slow.
    # Let's aggregate first.
    df_grouped = df.groupby(valid_cols).size().reset_index(name='count')
    
    fig = px.sunburst(
        df_grouped,
        path=valid_cols,
        values='count',
        title="Taxonomic Hierarchy (Kingdom -> Order)",
        height=700
    )
    return fig

def plot_top_genera(df, top_n=10):
    if df.empty or 'genus' not in df.columns:
        return None
    top_genera = df['genus'].value_counts().head(top_n)
    if top_genera.empty:
        return None
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_genera.values, y=top_genera.index, palette="viridis")
    plt.title(f"Top {top_n} Genera")
    plt.xlabel("Count")
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_top_species(df, top_n=10):
    if df.empty or 'species' not in df.columns:
        return None
    top_species = df['species'].value_counts().head(top_n)
    if top_species.empty:
        return None
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_species.values, y=top_species.index, palette="magma")
    plt.title(f"Top {top_n} Species")
    plt.xlabel("Count")
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_taxonomy_pie(df, column='kingdom_grouped'):
    if df.empty or column not in df.columns:
        return None
    counts = df[column].value_counts()
    if counts.empty:
        return None
        
    fig = px.pie(
        values=counts.values,
        names=counts.index,
        title=f"Distribution by {column.replace('_', ' ').title()}"
    )
    return fig

import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium

def plot_folium_map(df, map_type="Cluster"):
    if df.empty or not {'decimalLatitude', 'decimalLongitude'}.issubset(df.columns):
        return None
    
    # Drop invalid coordinates
    mdf = df.dropna(subset=['decimalLatitude', 'decimalLongitude'])
    if mdf.empty:
        return None
        
    # Center map
    center_lat = mdf['decimalLatitude'].mean()
    center_lon = mdf['decimalLongitude'].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=2)
    
    # Limit points for performance if needed (Folium can be slow with > 1000 markers)
    # Heatmap handles many points well, Cluster handles moderate amount.
    # Let's cap at 2000 for markers to be safe, but allow more for heatmap.
    
    if map_type == "Heatmap":
        heat_data = mdf[['decimalLatitude', 'decimalLongitude']].values.tolist()
        HeatMap(heat_data).add_to(m)
        
    elif map_type == "Cluster":
        marker_cluster = MarkerCluster().add_to(m)
        # Cap at 1000 for performance in cluster mode if not filtered enough
        if len(mdf) > 1000:
            mdf_sampled = mdf.sample(1000)
        else:
            mdf_sampled = mdf
            
        # Optimize iteration
        locations = mdf_sampled[['decimalLatitude', 'decimalLongitude']].values.tolist()
        species_list = mdf_sampled['species'].fillna('Unknown').tolist() if 'species' in mdf_sampled.columns else ['Observation'] * len(mdf_sampled)
        dates_list = mdf_sampled['eventDate'].astype(str).tolist() if 'eventDate' in mdf_sampled.columns else [''] * len(mdf_sampled)
        
        for loc, species, date in zip(locations, species_list, dates_list):
            popup_text = f"{species}<br>{date}"
            folium.Marker(
                location=loc,
                popup=popup_text,
            ).add_to(marker_cluster)
            
    elif map_type == "Markers":
        # Cap strictly for markers without cluster
        if len(mdf) > 500:
            mdf_sampled = mdf.sample(500)
        else:
            mdf_sampled = mdf
            
        # Optimize iteration
        locations = mdf_sampled[['decimalLatitude', 'decimalLongitude']].values.tolist()
        species_list = mdf_sampled['species'].fillna('Unknown').tolist() if 'species' in mdf_sampled.columns else ['Observation'] * len(mdf_sampled)
        
        for loc, species in zip(locations, species_list):
            popup_text = f"{species}"
            folium.Marker(
                location=loc,
                popup=popup_text,
            ).add_to(m)
            
    return m

def plot_plotly_map(df):
    # Return a Plotly mapbox scatter if latitude/longitude present
    if df.empty or not {'decimalLatitude', 'decimalLongitude'}.issubset(df.columns):
        return None
    
    mdf = df.dropna(subset=['decimalLatitude', 'decimalLongitude'])
    if mdf.empty:
        return None
        
    # Limit points for performance if too many
    if len(mdf) > 5000:
        mdf = mdf.sample(5000)
        
    fig = px.scatter_geo(
        mdf,
        lat='decimalLatitude',
        lon='decimalLongitude',
        hover_name='species' if 'species' in mdf.columns else None,
        color='kingdom_grouped' if 'kingdom_grouped' in mdf.columns else None,
        projection="natural earth",
        title='Global Observations Distribution'
    )
    return fig

def plot_month_year_heatmap(df):
    if df.empty or 'event_year' not in df.columns or 'event_month' not in df.columns:
        return None
    
    # Pivot table for heatmap
    heatmap_data = df.pivot_table(index='event_month', columns='event_year', values='gbifID', aggfunc='count')
    
    if heatmap_data.empty:
        return None
        
    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False)
    plt.title("Observation Frequency: Month vs Year")
    plt.xlabel("Year")
    plt.ylabel("Month")
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_kingdom_over_time(df):
    if df.empty or 'event_year' not in df.columns or 'kingdom_grouped' not in df.columns:
        return None
        
    # Group by Year and Kingdom
    yearly_kingdom = df.groupby(['event_year', 'kingdom_grouped']).size().reset_index(name='count')
    
    if yearly_kingdom.empty:
        return None
        
    fig = px.line(
        yearly_kingdom, 
        x='event_year', 
        y='count', 
        color='kingdom_grouped',
        title="Kingdom Observations Over Time",
        markers=True
    )
    return fig

def plot_country_richness(df):
    if df.empty or 'countryCode' not in df.columns or 'species' not in df.columns:
        return None
        
    richness = df.groupby('countryCode')['species'].nunique().sort_values(ascending=False).head(15)
    
    if richness.empty:
        return None
        
    plt.figure(figsize=(10, 6))
    sns.barplot(x=richness.values, y=richness.index, palette="viridis")
    plt.title("Top 15 Countries by Species Richness")
    plt.xlabel("Unique Species Count")
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig

def plot_state_richness(df):
    if df.empty or 'stateProvince' not in df.columns or 'species' not in df.columns:
        return None
        
    richness = df.groupby('stateProvince')['species'].nunique().sort_values(ascending=False).head(15)
    
    if richness.empty:
        return None
        
    plt.figure(figsize=(10, 6))
    sns.barplot(x=richness.values, y=richness.index, palette="magma")
    plt.title("Top 15 States by Species Richness")
    plt.xlabel("Unique Species Count")
    plt.tight_layout()
    fig = plt.gcf()
    plt.close()
    return fig