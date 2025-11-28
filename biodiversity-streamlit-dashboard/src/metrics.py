def species_count(df):
    return df['species'].nunique()

def genera_count(df):
    return df['genus'].nunique()

def families_count(df):
    return df['family'].nunique()

def kingdom_distribution(df):
    return df['kingdom_grouped'].value_counts()

def top_phyla(df, n=10):
    return df['phylum'].value_counts().head(n)

def top_orders(df, n=10):
    return df['order'].value_counts().head(n)

def top_genera(df, n=15):
    return df['genus'].value_counts().head(n)

def top_species(df, n=15):
    return df['species'].value_counts().head(n)

def observations_per_year(df):
    return df['event_year'].value_counts().sort_index()

def observations_per_month(df):
    return df['event_month'].value_counts().sort_index()

def country_counts(df, n=15):
    return df['countryCode'].value_counts().head(n)

def state_counts(df, n=15):
    return df['stateProvince'].value_counts().head(n)

def observers_count(df):
    if 'recordedBy' in df.columns:
        return df['recordedBy'].nunique()
    return 0

def images_count(df):
    if 'mediaType' in df.columns:
        return df['mediaType'].str.contains('StillImage', na=False).sum()
    return 0