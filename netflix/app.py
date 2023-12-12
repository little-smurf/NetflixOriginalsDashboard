import streamlit as st
import pandas as pd
import plotly.express as px
import re

def load_data():
    # Load your preprocessed CSV data
    data = pd.read_csv("preprocessed_data.csv", encoding="ISO-8859-1")  # Update with your actual file path
    return data

def preprocess_data(data):


    # Create a new column 'genres_list' with a list of genres for each title
    genre_columns = data.columns[data.columns.str.startswith('Genre')]
    data['genres_list'] = data[genre_columns].apply(
        lambda row: [genre.strip().lower() for genres in row.dropna() for genre in re.split('/| |-', genres) if genre.lower() not in ['variety show', 'one man show', 'coming of age'] or print(genre)],
        axis=1
    )



    # Create a new column 'languages_list' with a list of languages for each title
    data['languages_list'] = data['Language'].apply(lambda x: [lang.strip() for lang in re.split('/| |-', x)] if pd.notna(x) else [])

    return data

def main():
    # Load preprocessed data
    data = load_data()

    # Preprocess data
    data = preprocess_data(data)

    # Add interactive filters
    st.sidebar.subheader("Interactive Filters")

    # Genre filter
    unique_genres = data['genres_list'].explode().unique()
    selected_genres = st.sidebar.multiselect("Select Genres", unique_genres)

    # List of genres to exclude (exceptions)
    genre_exceptions = ['Variety Show', 'One Man Show', 'Coming of Age']

    if selected_genres:
        # Filter data, excluding genres in the exception list
        data = data[data['genres_list'].apply(lambda x: any(item in selected_genres for item in x) and not any(exception.lower() in x for exception in genre_exceptions))]


    # IMDB Score filter
    imdb_score_range = st.sidebar.slider("Select IMDB Score Range", float(data['IMDB Score'].min()), float(data['IMDB Score'].max()), (float(data['IMDB Score'].min()), float(data['IMDB Score'].max())))
    data = data[(data['IMDB Score'] >= imdb_score_range[0]) & (data['IMDB Score'] <= imdb_score_range[1])]

    # Language filter
    unique_languages = data['languages_list'].explode().unique()
    # Remove 'All' and 'English' from the unique_languages list
    unique_languages = [lang for lang in unique_languages if lang not in ['All', 'English']]
    selected_language = st.sidebar.selectbox("Select Language", unique_languages)
    if selected_language:
        data = data[data['languages_list'].apply(lambda x: selected_language in x)]



    # Custom HTML and CSS for styling
    custom_html_css = """
    <div id="body">
        <div id="custom-container">
            <h1>Netflix Originals Dashboard</h1>
            <div class="chart-container">
            </div>
        </div>
    </div>
    """

    custom_css = """
    <style>
    body {
        background-color: #fbe0e0; /* Primary background color */
        color: #000000; /* Text color */
        font-family: serif; /* Font family */

        /* Custom Streamlit theme colors */
        --primary-color: #560319;
        --background-color: #fbe0e0;
        --secondary-background-color: #f7e6e6;
        --text-color: #000000;
        --font: serif;

        /* Apply Streamlit theme colors */
        [theme] {
            primary-color: var(--primary-color);
            background-color: var(--background-color);
            secondary-background-color: var(--secondary-background-color);
            text-color: var(--text-color);
            font: var(--font);
        }
    }

    .data-frame-container {
        max-width: 100%;
        overflow-x: auto;
        margin-top: 20px;
        border: 1px solid #ccc;
        padding: 10px;
        background-color: var(--secondary-background-color);
    }

    .chart-container {
        margin-top: 20px;
        padding: 10px;
        background-color: var(--secondary-background-color);
    }
    </style>
    """

    # Display custom HTML and CSS
    st.markdown(custom_html_css, unsafe_allow_html=True)
    st.markdown(custom_css, unsafe_allow_html=True)


    # Display data overview
    st.subheader("Data Overview")
    st.dataframe(data.head())

    # Display basic statistics
    st.subheader("Basic Statistics")
    st.write(data.describe())

    # Add charts and visualizations
    # Example 1: Bar chart of IMDB Scores
    st.subheader("IMDB Scores Distribution")
    fig1 = px.histogram(data, x='IMDB Score', nbins=20)
    st.plotly_chart(fig1)

    

    # Explode the 'genres_list' column into separate rows
    data_exploded = data.explode('genres_list')

    # Create a pie chart with the exploded DataFrame
    st.subheader("Genres Distribution")
    fig2 = px.pie(data_exploded, names='genres_list', title='Genres Distribution', labels={'genres_list': 'Genre'})
    st.plotly_chart(fig2)


    # Scatter plot of Runtime vs. IMDB Score with separate colors for each genre
    st.subheader("Runtime vs. IMDB Score")
    fig3 = px.scatter(data_exploded, x='Runtime', y='IMDB Score', color='genres_list', size='IMDB Score', hover_name='Title', title='Runtime vs. IMDB Score')
    st.plotly_chart(fig3)

    # Explode the 'languages_list' column into separate rows
    data_exploded_languages = data_exploded.explode('languages_list')

    # Scatter plot of Runtime vs. IMDB Score with separate colors for each language
    st.subheader("Runtime vs. IMDB Score with separate colors for each language")
    fig_runtime_language = px.scatter(data_exploded_languages, x='Runtime', y='IMDB Score', color='languages_list', size='IMDB Score', hover_name='Title', title='Runtime vs. IMDB Score with separate colors for each language')
    st.plotly_chart(fig_runtime_language)




    # Example 5: Bar chart of Languages Distribution
    # Reset the index
    data.reset_index(drop=True, inplace=True)

    # Group the data by language and count their frequency
    language_counts = data['languages_list'].explode().value_counts()

    # Create a new DataFrame with the counts
    language_counts_data = language_counts.reset_index()
    language_counts_data.columns = ['Language', 'Count']

    # Display a bar chart to visualize the languages and their frequencies
    st.subheader("Languages Distribution")
    fig = px.bar(language_counts_data, x='Language', y='Count', title='Languages Distribution')
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
