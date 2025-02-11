import pandas as pd
from sklearn.linear_model import LinearRegression
from collections import Counter
import matplotlib.pyplot as plt

# Load the data
file_path = 'hasil filtering tanggal.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Ensure the required columns are present
if 'Stemmed_Keywords' not in data.columns or 'Date' not in data.columns:
    raise ValueError("The file must contain 'Stemmed_Keywords' and 'Date' columns.")

# Extract year from the Date column
data['Year'] = pd.to_datetime(data['Date'], format='%Y-%m').dt.year
data = data.dropna(subset=['Year', 'Stemmed_Keywords'])

# Normalize keywords to lowercase and split them into a list
data['Stemmed_Keywords'] = data['Stemmed_Keywords'].str.lower()
data['Keyword_List'] = data['Stemmed_Keywords'].apply(lambda x: x.split(','))

# Count keyword occurrences by year
keyword_trends = {}
for _, row in data.iterrows():
    year = row['Year']
    for keyword in row['Keyword_List']:
        if keyword not in keyword_trends:
            keyword_trends[keyword] = []
        keyword_trends[keyword].append(year)

# Aggregate keyword counts by year
keyword_year_counts = {
    keyword: Counter(years)
    for keyword, years in keyword_trends.items()
}

# Prepare data for trend prediction
future_year = max(data['Year']) + 1
predictions = {}
for keyword, year_counts in keyword_year_counts.items():
    years = list(year_counts.keys())
    counts = list(year_counts.values())
    if len(years) > 1:  # Only predict for keywords with historical data
        model = LinearRegression()
        model.fit([[y] for y in years], counts)
        predictions[keyword] = model.predict([[future_year]])[0]

# Predict the most used keyword in the future
most_used_future_keyword = max(predictions, key=predictions.get)
print(f"Keyword predicted to be most used in {future_year}: {most_used_future_keyword}")

# Visualization of top predicted keywords
top_keywords = sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:10]
plt.figure(figsize=(10, 6))
plt.barh([kw[0] for kw in top_keywords], [kw[1] for kw in top_keywords], color='skyblue')
plt.xlabel('Predicted Usage Count')
plt.ylabel('Keywords')
plt.title(f'Top 10 Keywords Predicted for {future_year}')
plt.gca().invert_yaxis()
plt.show()
