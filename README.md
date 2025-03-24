# IMDB_Project1

1. Data Scraping and Storage
   
*    Data Source: IMDb 2024 Movies page ("https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31").
*    Scraping Method: Used Selenium to extract the following fields:
    Movie Name
    Genre
    Ratings
    Voting Counts
    Duration
*    Genre-wise Storage: Save extracted data as individual CSV files for each genre like action.csv, adventure.csv, crime.csv, etc,.
*    Combine Data: Merged all genre-wise CSVs into a single DataFrame named as merged_movies_final.csv
*    SQL Storage: Stored the merged dataset into an SQL database named as IMDB

2.    Created interactive dashboard for real time users using streamlit and python
*    showcased visualizations, insights, and filtering functionality using Matplotlib and seaborn.
