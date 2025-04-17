import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.github_api import get_paginated_data

def display_issues(full_repo, token, start_date, end_date):
    """
    Display issue analysis
    
    Args:
        full_repo: Repository in format "user/repo"
        token: GitHub personal access token
        start_date: Start date for filtering
        end_date: End date for filtering
        
    Returns:
        DataFrame of issue data
    """
    # Fix: Correctly format the URL parameters
    issues_url = f"https://api.github.com/repos/{full_repo}/issues"
    # The base URL should not include query parameters - they're added in get_paginated_data
    issues_data = get_paginated_data(issues_url, token, params="state=all")
    
    if issues_data:
        # Prepare issues dataframe
        issues_list = []
        
        for issue in issues_data:
            # Skip pull requests
            if "pull_request" in issue:
                continue
                
            created_at = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            
            # Filter by date range
            if not (start_date <= created_at.date() <= end_date):
                continue
                
            issue_dict = {
                "number": issue["number"],
                "title": issue["title"],
                "state": issue["state"],
                "created_at": created_at,
                "user": issue["user"]["login"] if "login" in issue["user"] else "Unknown"
            }
            
            # Calculate time to close if closed
            if issue["state"] == "closed" and issue["closed_at"]:
                closed_at = datetime.strptime(issue["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
                issue_dict["closed_at"] = closed_at
                issue_dict["days_to_close"] = (closed_at - created_at).days
            
            issues_list.append(issue_dict)
        
        issues_df = pd.DataFrame(issues_list)
        
        if not issues_df.empty:
            # Issues analysis
            st.subheader("Issue Analysis")
            
            # Issue status distribution
            issue_status = issues_df["state"].value_counts().reset_index()
            issue_status.columns = ["State", "Count"]
            
            fig_issue_status = px.pie(
                issue_status,
                values="Count",
                names="State",
                title="Issue Status Distribution",
                color="State",
                color_discrete_map={"open": "red", "closed": "green"}
            )
            st.plotly_chart(fig_issue_status, use_container_width=True)
            
            # Calculate average time to close issues
            closed_issues = issues_df[issues_df["state"] == "closed"]
            
            if not closed_issues.empty and "days_to_close" in closed_issues.columns:
                avg_days_to_close = closed_issues["days_to_close"].mean()
                median_days_to_close = closed_issues["days_to_close"].median()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Average Days to Close", f"{avg_days_to_close:.1f}")
                with col2:
                    st.metric("Median Days to Close", f"{median_days_to_close:.1f}")
                
                # Distribution of time to close
                fig_close_time = px.histogram(
                    closed_issues,
                    x="days_to_close",
                    nbins=20,
                    labels={"days_to_close": "Days to Close", "count": "Number of Issues"},
                    title="Distribution of Time to Close Issues"
                )
                st.plotly_chart(fig_close_time, use_container_width=True)
            
            # Issues over time
            issues_df["month"] = issues_df["created_at"].dt.strftime("%Y-%m")
            monthly_issues = issues_df.groupby("month").size().reset_index(name="count")
            
            fig_issues_time = px.line(
                monthly_issues,
                x="month",
                y="count",
                labels={"month": "Month", "count": "Number of Issues"},
                title="Monthly Issue Creation Trend"
            )
            st.plotly_chart(fig_issues_time, use_container_width=True)
            
            return issues_df
    
    return pd.DataFrame()