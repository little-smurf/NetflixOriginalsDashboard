# data_preprocessing.py

import pandas as pd


def load_data(file_path):
    # Load your CSV data
    data = pd.read_csv(file_path, encoding='ISO-8859-1')
    return data

def preprocess_data(data):
    # Explore the data and perform necessary preprocessing steps

    # Display basic information about the data
    print("Data Overview:")
    print(data.head())

    # Check for missing values
    print("\nMissing Values:")
    print(data.isnull().sum())

    # Handle missing values (replace NaN values with mean, median, or specific values)
    data.fillna(value=0, inplace=True)  # Replace NaN with 0 for demonstration

    # Perform other preprocessing steps as needed

    return data

def save_processed_data(data, output_path):
    # Save the preprocessed data to a new CSV file
    data.to_csv(output_path, index=False)
    print(f"\nPreprocessed data saved to {output_path}")

if __name__ == "__main__":
    # Specify the path to your CSV file
    input_file_path = "NetflixOriginals.csv"

    # Specify the path to save the preprocessed data
    output_file_path = "preprocessed_data.csv"

    # Load the data
    original_data = load_data(input_file_path)

    # Perform data preprocessing
    preprocessed_data = preprocess_data(original_data)

    # Save the preprocessed data
    save_processed_data(preprocessed_data, output_file_path)