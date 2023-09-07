import pandas as pd
from helpers import *

FILE_LOCATION = "data/dataset.csv"
BRAND_VARIANTS = ["variant1", "variant2", "variant3"]

def job(file_location, brand_variants):
    """
    Main function for the job.
    """
    print('-- Start: Creating primary analysis df')
    initial_df = pd.read_csv(file_location)
    non_brand_df = remove_brand_queries(initial_df, brand_variants)
    query_page_counts = calculate_query_page_metrics(non_brand_df)
    query_counts = filter_queries_by_clicks_and_pages(query_page_counts)
    wip_df = merge_and_aggregate(query_page_counts, query_counts)
    wip_df = calculate_click_percentage(wip_df)
    wip_df = filter_by_click_percentage(wip_df)
    wip_df = merge_with_page_clicks(wip_df, initial_df)
    wip_df = define_opportunity_levels(wip_df)
    final_df = sort_and_finalize_output(wip_df)
    print('-- End: Creating primary analysis df')
    
    print('-- Start: Creating supporting dfs')
    qa_df = create_qa_dataframe(initial_df, final_df)
    immediate_opps_df = immediate_opps(final_df)
    instructions_df = create_instructions_df()
    print('-- End: Creating supporting dfs')
    
    dict_of_dfs = {
        "instructions": instructions_df, 
        "cannibalization_opps": final_df, 
        "immediate_opps": immediate_opps_df,
        "risk_qa_data": qa_df 
    }
    
    print('-- Start: Creating excel file')
    create_excel_file(dict_of_dfs)
    print('-- End: Creating excel file')
    
    return "Job complete!"


# Main script execution
if __name__ == "__main__":
    status = job(FILE_LOCATION, BRAND_VARIANTS)
    print(status)