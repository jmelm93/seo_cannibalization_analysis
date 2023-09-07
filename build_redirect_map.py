import pandas as pd

# Load CSV data
df = pd.read_csv("data.csv")

# Define a function to process each group
def process_group(group):
    # Filter rows where "clicks_pct_vs_page" > 0.50
    filtered = group[group["clicks_pct_vs_page"] > 0.5]
    if len(filtered) >= 2:
        # Get the page with the highest clicks_query (using the first in case of ties)
        url_to_row = filtered.sort_values(by="clicks_query", ascending=False).iloc[0]
        url_to = url_to_row["page"]
        
        # Get the pages with lower clicks_query
        url_froms = filtered[filtered["page"] != url_to]
        
        # list comprehension: Return as a list of dicts to create a DataFrame later
        return [
            {
                "query": group.name, 
                "url_from": row["page"], 
                "url_from_query_clicks": row["clicks_query"],
                "url_from_pct_page_clicks": row["clicks_pct_vs_page"],
                "url_to": url_to,
                "url_to_query_clicks": url_to_row["clicks_query"],
                "url_to_pct_page_clicks": url_to_row["clicks_pct_vs_page"],
            } for _, row in url_froms.iterrows()
        ]
    return []

# Apply the function to each group and flatten the list of lists
results = [item for group in df.groupby("query").apply(process_group) for item in group]

# Convert the list of dicts to a DataFrame
result_df = pd.DataFrame(results)

result_df.to_csv("result.csv", index=False)
