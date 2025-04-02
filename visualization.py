from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import plotly.express as px

# Secure Database Connection with SSL
DATABASE_URL = "mysql+pymysql://KUjMcLa9iTZrfjU.root:Fd8vm7Rtr3stcucS@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/IMDB?ssl_ca=D:\Streamlit\isrgrootx.pem"

# Create SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

# Fetch Data
query = "SELECT * FROM movies"
df = pd.read_sql(query, engine)

# Streamlit App Title
st.title("🎬 IMDb 2024 Movie Analysis")

# Sidebar Filters
st.sidebar.header("🔍 Filter Movies")
selected_genre = st.sidebar.selectbox("🎭 Select Genre", ["All"] + sorted(df["genre"].unique()))
min_rating = st.sidebar.slider("⭐ Minimum Rating", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
min_votes = st.sidebar.slider("🗳️ Minimum Votes", min_value=int(df["votes"].min()), max_value=int(df["votes"].max()), value=int(df["votes"].min()))

# Apply Filters
filtered_df = df.copy()
if selected_genre != "All":
    filtered_df = filtered_df[filtered_df["genre"] == selected_genre]
filtered_df = filtered_df[(filtered_df["rating"] >= min_rating) & (filtered_df["votes"] >= min_votes)]

# Display Filtered Data
st.subheader("🎥 Filtered Movies")
st.dataframe(filtered_df)

# Top 10 Movies by Rating & Votes
st.subheader("🏆 Top 10 Movies by Rating & Votes")
top_movies = df.nlargest(10, ["rating", "votes"])
fig_top_movies = px.bar(top_movies, x="movie_name", y="rating", color="votes", title="Top 10 Movies", color_continuous_scale="rainbow")
st.plotly_chart(fig_top_movies)
st.write("**Insight:** These top movies have the highest ratings and votes, indicating their popularity among audiences.")

# Genre Distribution
st.subheader("🎭 Genre Distribution")
genre_counts = df["genre"].value_counts().reset_index()
genre_counts.columns = ["Genre", "Count"]
fig_genre = px.bar(genre_counts, x="Genre", y="Count", title="Movie Count by Genre", color="Count", color_continuous_scale="viridis")
st.plotly_chart(fig_genre)
st.write("**Insight:** Some genres, such as Drama and Action, dominate the 2024 movie list, reflecting audience preferences.")

# Average Duration by Genre
st.subheader("⏳ Average Duration by Genre")
avg_duration = df.groupby("genre")["duration"].mean().reset_index()
fig_duration = px.bar(avg_duration, x="duration", y="genre", orientation="h", title="Average Duration per Genre", color="duration", color_continuous_scale="plasma")
st.plotly_chart(fig_duration)
st.write("**Insight:** The average movie length varies by genre, with some genres having significantly longer runtimes. Notably, the Thriller genre tends to have longer movies.")

# Voting Trends by Genre
st.subheader("📊 Voting Trends by Genre")
avg_votes = df.groupby("genre")["votes"].mean().reset_index()
fig_votes = px.bar(avg_votes, x="genre", y="votes", title="Average Votes per Genre", color="votes", color_continuous_scale="cividis")
st.plotly_chart(fig_votes)
st.write("**Insight:** Genres with high votes reflect audience engagement and preferences, with the Sci-Fi genre receiving the most votes")

# Rating Distribution (Box Plot)
st.subheader("⭐ Rating Distribution")
fig_rating_dist = px.box(df, y="rating", title="Rating Distribution", color_discrete_sequence=["#FF9A9A"])
st.plotly_chart(fig_rating_dist)
st.write("**Insight:** This distribution highlights how movie ratings are spread out, identifying outliers. The ratings range from a low of 5.1 to a high of 8.7")

# Most Popular Genres by Voting (Pie Chart)
st.subheader("🍕 Most Popular Genres by Voting")
fig_genre_votes = px.pie(df, names="genre", values="votes", title="Genres with Highest Total Votes", color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig_genre_votes)
st.write("**Insight:** The most voted genres indicate what audiences engaged with the most, with Drama receiving the highest number of votes due to its large number of movies.")

# Shortest & Longest Movies
st.subheader("🎬 Shortest & Longest Movies")
shortest_movie = df.nsmallest(1, "duration")
longest_movie = df.nlargest(1, "duration")
st.write("**Shortest Movie:**", shortest_movie[["movie_name", "duration"]])
st.write("**Longest Movie:**", longest_movie[["movie_name", "duration"]])
st.write("**Insight:** Some movies are significantly shorter or longer than the average runtime. The shortest movie is Florp's Solar Vacation, while the longest is 24.")

# Ratings vs. Votes Correlation (Scatter Plot)
st.subheader("📈 Ratings vs. Votes Correlation")
fig_corr = px.scatter(df, x="votes", y="rating", title="Correlation Between Ratings & Votes", color="rating", size="votes", color_continuous_scale="plasma")
st.plotly_chart(fig_corr)
st.write("**Insight:**More ratings generally indicate higher engagement, but the vote distribution varies, possibly because some movies are newly released. ")

# Sunburst Chart for Genre & Votes
st.subheader("Sunburst Chart: Genre Popularity")
top_genres = df.groupby("genre")["votes"].sum().reset_index().nlargest(10, "votes")
fig_sunburst = px.sunburst(top_genres, path=["genre"], values="votes", title="Top 10 Genres by Votes", color="genre", color_discrete_sequence=px.colors.qualitative.Dark24)
st.plotly_chart(fig_sunburst)
st.write("**Overall Insight:** These genres dominate IMDb's 2024 list, indicating strong audience preference and engagement.")

# 📢 Overall Data Insights
st.subheader("📊 Overall Insights")
st.write("- Action & Drama are the most dominant genres in 2024's movie list.")
st.write("- Ratings are mostly centered between 5 to 8, with few extreme ratings.")
st.write("- Movies with higher votes usually have better ratings, but exceptions exist.")
st.write("- Some niche genres may have fewer movies but still receive strong ratings.")
st.write("- The sunburst chart reveals the distribution of movies across genres, helping in comparative analysis.")

st.write("🎬 **Enjoy exploring IMDb 2024 movies!** 🚀")
