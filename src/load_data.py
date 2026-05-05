import pandas as pd

def load_wine_data(path="data/wine_recommendation_dataset.csv"):
    """
    Carga el dataset de vinos desde un archivo CSV.
    """
    df = pd.read_csv(path)
    return df
