import streamlit as st
import pandas as pd
import plotly.express as px
from utils.github_api import make_request

def display_languages(full_repo, token):
    """
    Display language analysis
    
    Args:
        full_repo: Repository in format "user/repo"
        token: GitHub personal access token
    """
    languages_url = f"https://api.github.com/repos/{full_repo}/languages"
    languages_data = make_request(languages_url, token)
    
    if languages_data:
        # Create languages dataframe
        languages_df = pd.DataFrame({
            'language': list(languages_data.keys()),
            'bytes': list(languages_data.values())
        })
        
        # Sort and calculate percentages
        languages_df = languages_df.sort_values('bytes', ascending=False)
        languages_df['percentage'] = languages_df['bytes'] / languages_df['bytes'].sum() * 100
        
        # Display language distribution
        st.subheader("Language Distribution")
        
        fig_languages = px.pie(
            languages_df,
            values='bytes',
            names='language',
            title="Repository Language Distribution",
            hover_data=['percentage'],
            labels={'percentage': 'Percentage (%)'}
        )
        st.plotly_chart(fig_languages, use_container_width=True)
        
        return languages_df
    
    return pd.DataFrame()