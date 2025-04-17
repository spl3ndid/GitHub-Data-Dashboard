import streamlit as st
import pandas as pd
import plotly.express as px
from utils.github_api import make_request

def display_contributors(full_repo, token):
    """
    Display contributor analysis
    
    Args:
        full_repo: Repository in format "user/repo"
        token: GitHub personal access token
    """
    contributors_url = f"https://api.github.com/repos/{full_repo}/contributors"
    contributors_data = make_request(contributors_url, token)
    
    if contributors_data:
        # Prepare contributor data
        contributors_df = pd.DataFrame(contributors_data)
        contributors_df = contributors_df[["login", "contributions"]].sort_values("contributions", ascending=False)
        
        # Display top contributors
        st.subheader("Top Contributors")
        top_contributors = contributors_df.head(10)
        
        fig_contributors = px.bar(
            top_contributors, 
            x="login", 
            y="contributions",
            labels={"login": "Contributor", "contributions": "Contributions"},
            title="Top 10 Contributors by Commit Count"
        )
        st.plotly_chart(fig_contributors, use_container_width=True)
        
        return contributors_df
    
    return pd.DataFrame()