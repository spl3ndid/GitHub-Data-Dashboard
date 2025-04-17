import streamlit as st

def display_repo_info(repo_data):
    """
    Display basic repository information metrics
    
    Args:
        repo_data: Repository data from GitHub API
    """
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Stars", repo_data["stargazers_count"])
    with col2:
        st.metric("Forks", repo_data["forks_count"])
    with col3:
        st.metric("Open Issues", repo_data["open_issues_count"])