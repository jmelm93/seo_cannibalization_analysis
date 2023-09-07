import pandas as pd

def create_instructions_df():
    """
    Create a DataFrame with the instructions
    """
    instructions_data = {
        "Instructions": [
            "Tabs Explained:",
            "- 'all_potential_opps': Contains the final analysis output.",
            "- 'high_likelihood_opps': Lists queries with 2+ pages marked as 'Potential Opportunity.'",
            "- 'risk_qa_data': Includes query-level data for pages in 'all_potential_opps.'",
            "",
            "Explanation:",
            "For consolidation consideration:",
            "- If a query has 2+ pages with 10%+ clicks (defined by 'clicks_pct_vs_query').",
            "- The query itself is more than 10% of the page clicks (defined by 'clicks_pct_vs_page').",
            "Queries marked 'Potential Opportunity' are considered for consolidation.",
            "Queries marked 'Risk' suggest caution:",
            "- If a query is <10% of page clicks, more valuable queries may be risked during consolidation.",
            "This doesn't mean consolidation is unwarranted for 'Risk' queries but warrants further investigation.",
            "",
            "How To Use:",
            "- 'all_potential_opps' tab: Identify consolidation opportunities. Use the 'comments' column to see if a query is 'Potential Opportunity' or 'Risk.'",
            "- If a query has 2+ pages as 'Potential Opportunity,' consider consolidation.",
            "- 'high_likelihood_opps' tab: Lists queries with 2+ 'Potential Opportunity' pages.",
            "- Even if something is in 'high_likelihood_opps,' it should still be reviewed prior to implementation.",
            "- If only 1 'Potential Opportunity' page and the rest are 'Risk,' consider:",
            "   1) Check 'risk_qa_data' tab to see if 'Risk' and 'Potential Opportunity' pages align in intent.",
            "   2) If they align, consolidation may be a good idea.",
        ]
    }

    return pd.DataFrame(instructions_data)