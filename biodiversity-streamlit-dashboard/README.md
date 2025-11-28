# Biodiversity Streamlit Dashboard

This project is an interactive dashboard built using Streamlit to visualize and analyze biodiversity data. It provides various features and insights into the dataset, allowing users to explore taxonomic distributions, temporal trends, spatial distributions, and more.

## Project Structure

```
biodiversity-streamlit-dashboard
├── app.py                     # Main entry point for the Streamlit application
├── requirements.txt           # List of dependencies for the project
├── README.md                  # Documentation for the project
├── .gitignore                 # Files and directories to ignore by Git
├── .streamlit
│   └── config.toml           # Streamlit app configuration settings
├── data
│   └── gbif_cleaned.csv     # Sample dataset for testing and demonstration
├── notebooks
│   └── biodiversity.ipynb     # Jupyter notebook with analysis and data processing
├── src
│   ├── __init__.py           # Marks the src directory as a Python package
│   ├── data_loader.py         # Functions for loading and processing the dataset
│   ├── preprocessing.py        # Functions for data preprocessing
│   ├── metrics.py             # Functions to calculate key metrics
│   ├── visualizations.py       # Functions for creating visualizations
│   └── components
│       ├── sidebar.py         # Sidebar layout and navigation
│       └── tabs.py            # Manages the tabbed interface
├── pages
│   ├── 1_overview.py          # Overview of the dataset
│   ├── 2_taxonomy.py          # Taxonomic distribution of species
│   ├── 3_temporal.py          # Temporal analysis of observations
│   ├── 4_spatial.py           # Spatial analysis of geographical distribution
│   ├── 5_distribution.py       # Distribution metrics by country and state
│   └── 6_analysis.py          # Additional analysis features
└── tests
    └── test_data_loader.py    # Unit tests for data loading functions
```

## Features

- **Overview Page**: Provides key statistics and general information about the dataset.
- **Taxonomy Page**: Displays visualizations and metrics related to the taxonomic distribution of species.
- **Temporal Analysis**: Shows trends over time in the dataset, including observations per year and month.
- **Spatial Analysis**: Visualizes the geographical distribution of observations using maps and heatmaps.
- **Distribution Metrics**: Displays country and state-level counts of observations.
- **Additional Analysis**: Includes correlation analysis and biodiversity richness metrics.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd biodiversity-streamlit-dashboard
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

4. Open your web browser and navigate to `http://localhost:8501` to view the dashboard.

## Usage Guidelines

- Use the sidebar to navigate between different sections of the dashboard.
- Explore the various tabs to gain insights into the biodiversity dataset.
- Visualizations and metrics are interactive, allowing for a deeper understanding of the data.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.