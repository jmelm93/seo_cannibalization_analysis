import pandas as pd
import numpy as np

def remove_brand_queries(df, brand_variants):
    """
    Remove queries that contain brand variants.
    """
    df = df[~df['query'].str.contains('|'.join(brand_variants))]
    print("'|'.join(brand_variants)", '|'.join(brand_variants))
    return df


def calculate_query_page_metrics(df):
    """
    Calculate metrics for each combination of "query" and "page".
    """
    query_page_counts = df.groupby(['query', 'page']).agg({
        'clicks': 'sum',
        'impressions': 'sum',
        'position': 'mean'
    }).reset_index()
    
    query_page_counts = query_page_counts.rename(columns={'position': 'avg_position'})
    return query_page_counts


def filter_queries_by_clicks_and_pages(query_page_counts):
    """
    Filter queries based on the click condition and distinct pages.
    """
    query_counts = query_page_counts.groupby('query').agg({
        'page': 'nunique',
        'clicks': 'sum'
    }).reset_index()
    
    query_counts = query_counts[(query_counts['page'] >= 2) & (query_counts['clicks'] >= 1)]
    return query_counts


def merge_and_aggregate(query_page_counts, query_counts):
    """
    Merge metrics and join with filtered queries.
    """
    df = query_page_counts.merge(query_counts[['query']], on='query', how='inner')
    df = df.groupby(['page', 'query']).agg({
        'clicks': 'sum',
        'impressions': 'sum',
        'avg_position': 'mean'
    }).reset_index()
    return df


def calculate_click_percentage(df):
    """
    Calculate percentage of clicks for each page per query.
    """
    df['clicks_pct_vs_query'] = df.groupby('query')['clicks'].transform(lambda x: x / x.sum())
    return df


def filter_by_click_percentage(df):
    """
    Identify and filter by queries that meet specific conditions.
    Only keep queries that have at least 2 pages with 10% or more clicks
    """
    queries_to_keep = df[df['clicks_pct_vs_query'] >= 0.1].groupby('query').filter(lambda x: len(x) >= 2)['query'].unique()
    df = df[df['query'].isin(queries_to_keep)]
    return df


def merge_with_page_clicks(wip_df, initial_df):
    """
    Merge with page-level click metrics and calculate percentage metrics.
    """
    page_clicks = initial_df.groupby('page').agg({'clicks': 'sum'}).reset_index()
    wip_df = wip_df.merge(page_clicks, on='page', how='inner')
    
    wip_df['clicks_pct_vs_page'] = wip_df['clicks_x'] / wip_df['clicks_y']
    
    # Renaming columns
    wip_df = wip_df.rename(columns={'clicks_x': 'clicks_query', 'clicks_y': 'clicks_page'})
    
    return wip_df


def define_opportunity_levels(wip_df):
    """
    Create 'comment' column based on 'clicks_pct_vs_query' and 'clicks_pct_vs_page'.
    """

    wip_df['comment'] = np.where(
        (wip_df['clicks_pct_vs_query'] >= 0.1) & (wip_df['clicks_pct_vs_page'] >= 0.1),
        'Potential Opportunity',
        'Risk - Low percentage of either query-level or page-level clicks'
    )    
    
    return wip_df


def sort_and_finalize_output(wip_df):
    """
    Sort data and format final output.
    """
    # Sorting
    wip_df = wip_df.sort_values(['query', 'clicks_pct_vs_query', 'clicks_pct_vs_page'], ascending=[True, False, False])
    
    # Formatting final output
    metric_col_order = ['impressions', 'avg_position', 'clicks_query', 'clicks_pct_vs_query', 'clicks_page', 'clicks_pct_vs_page','comment']
    wip_df = wip_df[['query', 'page'] + metric_col_order]
    wip_df[metric_col_order] = wip_df[metric_col_order].round(2)
    
    return wip_df


def create_qa_dataframe(initial_df, final_df):
    """
    Df that contains all the query-level data for pages existing in the final_df.
    Used to check all queries to see whether rows in the final_df that are 'Risk' are actually worth consolidating.
    """
    return initial_df[initial_df['page'].isin(final_df['page'].unique())]


def immediate_opps(final_df):
    """
    If 2+ pages for a query are marked as 'Potential Opportunity,' then return those rows as they're 'Immediate Opportunities.'
    """
    return final_df[final_df['comment'] == 'Potential Opportunity'].groupby('query').filter(lambda x: len(x) >= 2)