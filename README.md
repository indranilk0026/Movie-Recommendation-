# Movie Recommendation System

A simple interactive movie recommendation app built with Python and Streamlit.

## Features

- Select a movie from a searchable list
- Get related movie recommendations
- Surprise-me option for random recommendations
- Clean and simple Streamlit interface

## Project Structure

- app.py - Main Streamlit application
- datasets/ - Original movie CSV files
- requirements.txt - Python dependencies
- MovieRecommendation.ipynb - Notebook

## Requirements

Install the required packages:

```bash
pip install -r requirements.txt
```

## Run the App

From the project folder, run:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal in your browser.

## Notes

- The app currently uses the precomputed movie similarity data from the pickle files.
- The TMDB poster integration is kept as commented code for future use.

## Example

1. Launch the app
2. Choose a movie from the dropdown
3. Click "Show recommendations"
4. Explore the suggested movies
