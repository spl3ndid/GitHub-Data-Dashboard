import streamlit as st
import pandas as pd
from datetime import datetime

from utils.github_api import make_request
from components.sidebar import render_sidebar
from components.repository_info import display_repo_info
from components.contributors import display_contributors
from components.commits import display_commits
from components.languages import display_languages
from components.issues import display_issues
from components.pulls import display_pull_requests

# Set page config
st.set_page_config(
    page_title="GitHub Repository Analytics",
    page_icon="📊",
    layout="wide"
)

# App title and description
st.title("GitHub Repository Analytics Dashboard")
st.markdown("""
This dashboard provides insights into GitHub repositories by analyzing metrics such as:
- Contributor trends
- Issue closing time
- Commit frequency
- Programming language usage
- Issues vs. Pull Requests
""")

# Render sidebar and get repository and date selections
token, full_repo, start_date, end_date = render_sidebar()

# Data loading and analysis
if full_repo:
    st.header(f"📊 Analytics for {full_repo}")
    
    # Progress indicator
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Get repository information
    status_text.text("Loading repository information...")
    repo_url = f"https://api.github.com/repos/{full_repo}"
    repo_data = make_request(repo_url, token)
    progress_bar.progress(10)
    
    if repo_data:
        # Display repository information
        display_repo_info(repo_data)
        
        # Display contributors analysis
        status_text.text("Loading contributor data...")
        display_contributors(full_repo, token)
        progress_bar.progress(20)
        
        # Display commit analysis
        status_text.text("Loading commit history...")
        commits_df = display_commits(full_repo, token, start_date, end_date)
        progress_bar.progress(40)
        
        # Display language analysis
        status_text.text("Loading language statistics...")
        display_languages(full_repo, token)
        progress_bar.progress(60)
        
        # Display issues analysis
        status_text.text("Loading issue data...")
        issues_df = display_issues(full_repo, token, start_date, end_date)
        progress_bar.progress(80)
        
        # Display pull requests analysis
        status_text.text("Loading pull request data...")
        pulls_df = display_pull_requests(full_repo, token, start_date, end_date)
        progress_bar.progress(90)
        
        # Compare issues vs PRs over time
        if 'issues_df' in locals() and not issues_df.empty and 'pulls_df' in locals() and not pulls_df.empty:
            from components.pulls import compare_issues_and_prs
            compare_issues_and_prs(issues_df, pulls_df)
        
        progress_bar.progress(100)
        status_text.text("Data analysis complete!")
    else:
        st.error(f"Could not retrieve data for repository: {full_repo}")
else:
    st.info("Please select a GitHub repository to analyze")

# Footer
st.markdown("---")
st.markdown("GitHub Repository Analytics Dashboard | Built with Streamlit")