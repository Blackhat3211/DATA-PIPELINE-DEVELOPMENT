import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def extract_data(file_path):
    """Stage 1: Extract data from a CSV source."""
    try:
        df = pd.read_csv(file_path)
        print(f"Successfully extracted {len(df)} rows.")
        return df
    except Exception as e:
        print(f"Error during extraction: {e}")
        return None

def transform_data(df):
    """Stage 2: Preprocessing and Transformation."""
    
    numeric_features = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = df.select_dtypes(include=['object']).columns

 
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    
    transformed_data = preprocessor.fit_transform(df)
    
    
    cat_names = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_features)
    new_columns = list(numeric_features) + list(cat_names)
    
    return pd.DataFrame(transformed_data, columns=new_columns)

def load_data(df, output_path):
    """Stage 3: Load the processed data into a destination."""
    try:
        df.to_csv(output_path, index=False)
        print(f"Successfully loaded data to {output_path}")
    except Exception as e:
        print(f"Error during loading: {e}")


if __name__ == "__main__":
    DATA_SOURCE = "raw_data.csv"
    OUTPUT_DESTINATION = "cleaned_data.csv"

    
    raw_df = extract_data(DATA_SOURCE)
    if raw_df is not None:
        processed_df = transform_data(raw_df)
        load_data(processed_df, OUTPUT_DESTINATION)