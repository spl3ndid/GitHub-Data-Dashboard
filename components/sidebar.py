import streamlit as st
from datetime import datetime, timedelta
from utils.github_api import make_request

def render_sidebar():
    """
    Render the sidebar UI and return selected parameters
    
    Returns:
        token: GitHub personal access token
        full_repo: Selected repository in format "user/repo"
        start_date: Start date for data filtering
        end_date: End date for data filtering
    """
    # Authentication section
    st.sidebar.header("GitHub Authentication")
    use_token = st.sidebar.checkbox("Use GitHub Personal Access Token")
    token = st.sidebar.text_input("GitHub Personal Access Token", type="password") if use_token else ""

    # Repository selection
    st.sidebar.header("Repository Selection")
    repo_input_method = st.sidebar.radio("Select repository by:", ["User/Org + Repository", "Direct URL"])
    
    full_repo = None
    
    if repo_input_method == "User/Org + Repository":
        user_or_org = st.sidebar.text_input("GitHub Username or Organization")
        
        if user_or_org:
            # Get user repositories
            repos_url = f"https://api.github.com/users/{user_or_org}/repos"
            repos_data = make_request(repos_url, token)
            
            if repos_data:
                repo_names = [repo["name"] for repo in repos_data]
                selected_repo = st.sidebar.selectbox("Select Repository", repo_names)
                
                if selected_repo:
                    full_repo = f"{user_or_org}/{selected_repo}"
            else:
                st.sidebar.warning("Please enter a valid GitHub username or organization")
    else:  # Direct URL
        repo_url = st.sidebar.text_input("GitHub Repository URL (e.g., https://github.com/username/repo)")
        
        if repo_url:
            # Extract user and repo from URL
            parts = repo_url.strip("/").split("/")
            if len(parts) >= 5 and parts[2] == "github.com":
                user_or_org = parts[3]
                selected_repo = parts[4]
                full_repo = f"{user_or_org}/{selected_repo}"
            else:
                st.sidebar.warning("Please enter a valid GitHub repository URL")

    # Date range selection for filtering data
    st.sidebar.header("Date Range")
    today = datetime.now()
    default_start_date = today - timedelta(days=365)
    start_date = st.sidebar.date_input("Start Date", default_start_date)
    end_date = st.sidebar.date_input("End Date", today)

    if start_date > end_date:
        st.sidebar.error("Start date should be before end date")

    # Add help sections
    st.sidebar.markdown("---")
    st.sidebar.header("User Guide")
    st.sidebar.info("""
    1. Enter a GitHub username/organization or repository URL
    2. Select a repository if using username/organization
    3. Adjust date range if needed
    4. For higher API rate limits, provide a GitHub token
    5. Explore the analytics!
    """)
    
    st.sidebar.header("About GitHub API Tokens")
    st.sidebar.info("""
    Without a token, GitHub API limits you to 60 requests per hour.
    With a token, you get 5,000 requests per hour.
    
    To create a token:
    1. Go to GitHub → Settings → Developer settings → Personal access tokens
    2. Generate a new token with "repo" scope
    3. Copy and paste it here
    """)
    
    return token, full_repo, start_date, end_date