import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.github_api import get_paginated_data

def display_pull_requests(full_repo, token, start_date, end_date):
    """
    Display pull request analysis
    
    Args:
        full_repo: Repository in format "user/repo"
        token: GitHub personal access token
        start_date: Start date for filtering
        end_date: End date for filtering
        
    Returns:
        DataFrame of pull request data
    """
    pulls_url = f"https://api.github.com/repos/{full_repo}/pulls"
    # Fix: Use the params argument correctly
    pulls_data = get_paginated_data(pulls_url, token, params="state=all")
    
    if pulls_data:
        # Prepare pull requests dataframe
        pulls_list = []
        
        for pr in pulls_data:
            created_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            
            # Filter by date range
            if not (start_date <= created_at.date() <= end_date):
                continue
                
            pr_dict = {
                "number": pr["number"],
                "title": pr["title"],
                "state": pr["state"],
                "created_at": created_at,
                "user": pr["user"]["login"] if "login" in pr["user"] else "Unknown"
            }
            
            # Calculate time to merge if merged
            if pr["merged_at"]:
                merged_at = datetime.strptime(pr["merged_at"], "%Y-%m-%dT%H:%M:%SZ")
                pr_dict["merged_at"] = merged_at
                pr_dict["days_to_merge"] = (merged_at - created_at).days
            
            pulls_list.append(pr_dict)
        
        pulls_df = pd.DataFrame(pulls_list)
        
        if not pulls_df.empty:
            # Pull requests analysis
            st.subheader("Pull Request Analysis")
            
            # PR status distribution
            pr_status = pulls_df["state"].value_counts().reset_index()
            pr_status.columns = ["State", "Count"]
            
            fig_pr_status = px.pie(
                pr_status,
                values="Count",
                names="State",
                title="Pull Request Status Distribution",
                color="State",
                color_discrete_map={"open": "red", "closed": "green"}
            )
            st.plotly_chart(fig_pr_status, use_container_width=True)
            
            # Top PR contributors
            top_pr_contributors = pulls_df["user"].value_counts().head(10).reset_index()
            top_pr_contributors.columns = ["User", "Count"]
            
            fig_pr_contributors = px.bar(
                top_pr_contributors,
                x="User",
                y="Count",
                labels={"User": "Contributor", "Count": "Number of PRs"},
                title="Top 10 Pull Request Contributors"
            )
            st.plotly_chart(fig_pr_contributors, use_container_width=True)
            
            return pulls_df
    
    return pd.DataFrame()

def compare_issues_and_prs(issues_df, pulls_df):
    """
    Compare issues and pull requests over time
    
    Args:
        issues_df: DataFrame of issues
        pulls_df: DataFrame of pull requests
    """
    st.subheader("Issues vs Pull Requests Over Time")
    
    # Prepare data
    issues_df["month"] = issues_df["created_at"].dt.strftime("%Y-%m")
    pulls_df["month"] = pulls_df["created_at"].dt.strftime("%Y-%m")
    
    monthly_issues = issues_df.groupby("month").size().reset_index(name="issues")
    monthly_pulls = pulls_df.groupby("month").size().reset_index(name="pulls")
    
    # Merge dataframes
    monthly_comparison = pd.merge(monthly_issues, monthly_pulls, on="month", how="outer").fillna(0)
    
    # Convert to integers
    monthly_comparison["issues"] = monthly_comparison["issues"].astype(int)
    monthly_comparison["pulls"] = monthly_comparison["pulls"].astype(int)
    
    # Create figure
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Scatter(
        x=monthly_comparison["month"],
        y=monthly_comparison["issues"],
        mode="lines+markers",
        name="Issues"
    ))
    
    fig_comparison.add_trace(go.Scatter(
        x=monthly_comparison["month"],
        y=monthly_comparison["pulls"],
        mode="lines+markers",
        name="Pull Requests"
    ))
    
    fig_comparison.update_layout(
        title="Issues vs Pull Requests Over Time",
        xaxis_title="Month",
        yaxis_title="Count",
        legend_title="Type"
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)