import requests
import streamlit as st
import time

def make_request(url, token=None, headers=None, params=None):
    """
    Make a request to the GitHub API with rate limit handling
    
    Args:
        url: API endpoint URL
        token: GitHub personal access token
        headers: Additional headers
        params: URL parameters as a string ("param1=value1&param2=value2")
        
    Returns:
        JSON response or None if error
    """
    if headers is None:
        headers = {}
        
    if token:
        headers["Authorization"] = f"token {token}"
    
    # Append params to URL if provided
    if params:
        if '?' in url:
            url = f"{url}&{params}"
        else:
            url = f"{url}?{params}"
    
    response = requests.get(url, headers=headers)
    
    # Check if we're rate limited
    if response.status_code == 403 and "X-RateLimit-Remaining" in response.headers and int(response.headers["X-RateLimit-Remaining"]) == 0:
        reset_time = int(response.headers["X-RateLimit-Reset"])
        wait_time = max(0, reset_time - time.time())
        st.warning(f"Rate limit exceeded. Waiting {wait_time:.1f} seconds for reset...")
        time.sleep(wait_time + 1)
        return make_request(url, token, headers)
    
    # Handle other errors
    if response.status_code != 200:
        st.error(f"Error accessing GitHub API: {response.status_code} - {response.text}")
        return None
        
    return response.json()

def get_paginated_data(base_url, token=None, max_pages=10, params=None):
    """
    Get paginated data from GitHub API
    
    Args:
        base_url: Base API URL
        token: GitHub personal access token
        max_pages: Maximum number of pages to fetch
        params: Additional URL parameters as a string
        
    Returns:
        List of results
    """
    all_data = []
    page = 1
    
    while True:
        # Build pagination parameter
        pagination_param = f"page={page}&per_page=100"
        
        # Combine with other params if any
        request_params = pagination_param
        if params:
            request_params = f"{params}&{pagination_param}"
            
        page_data = make_request(base_url, token, params=request_params)
        
        if not page_data or len(page_data) == 0:
            break
            
        all_data.extend(page_data)
        page += 1
        
        if page > max_pages:  # Limit to avoid too many API calls
            break
            
    return all_data