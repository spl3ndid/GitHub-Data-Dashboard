import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.github_api import get_paginated_data

def display_commits(full_repo, token, start_date, end_date):
    """
    Display commit analysis
    
    Args:
        full_repo: Repository in format "user/repo"
        token: GitHub personal access token
        start_date: Start date for filtering
        end_date: End date for filtering
        
    Returns:
        DataFrame of commit data
    """
    commits_url = f"https://api.github.com/repos/{full_repo}/commits"
    commits_data = get_paginated_data(commits_url, token)
    
    if commits_data:
        # Parse commit dates
        commit_dates = []
        commit_authors = []
        
        for commit in commits_data:
            if "commit" in commit and "author" in commit["commit"] and "date" in commit["commit"]["author"]:
                date_str = commit["commit"]["author"]["date"]
                commit_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                
                # Filter by date range
                if start_date <= commit_date.date() <= end_date:
                    commit_dates.append(commit_date)
                    author = commit["commit"]["author"]["name"] if "name" in commit["commit"]["author"] else "Unknown"
                    commit_authors.append(author)
        
        # Create commits dataframe
        commits_df = pd.DataFrame({
            'date': commit_dates,
            'author': commit_authors
        })
        
        if not commits_df.empty:
            # Commits over time
            st.subheader("Commit Activity")
            
            # Group commits by week
            commits_df['week'] = commits_df['date'].dt.isocalendar().week
            commits_df['year'] = commits_df['date'].dt.year
            commits_df['yearweek'] = commits_df['year'].astype(str) + "-" + commits_df['week'].astype(str).str.zfill(2)
            
            weekly_commits = commits_df.groupby('yearweek').size().reset_index(name='commits')
            weekly_commits = weekly_commits.tail(52)  # Last 52 weeks
            
            fig_commits = px.line(
                weekly_commits, 
                x="yearweek", 
                y="commits",
                labels={"yearweek": "Week", "commits": "Number of Commits"},
                title="Weekly Commit Activity"
            )
            st.plotly_chart(fig_commits, use_container_width=True)
            
            # Top committers
            st.subheader("Top Committers")
            top_committers = commits_df['author'].value_counts().head(10).reset_index()
            top_committers.columns = ['author', 'commits']
            
            fig_committers = px.bar(
                top_committers,
                x="author",
                y="commits",
                labels={"author": "Committer", "commits": "Number of Commits"},
                title="Top 10 Committers"
            )
            st.plotly_chart(fig_committers, use_container_width=True)
            
            return commits_df
    
    return pd.DataFrame()