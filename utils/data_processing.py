import pandas as pd
from datetime import datetime

def filter_by_date_range(data, date_field, start_date, end_date):
    """
    Filter a list of dictionaries by date range
    
    Args:
        data: List of dictionaries containing date fields
        date_field: Name of the date field
        start_date: Start date for filtering
        end_date: End date for filtering
        
    Returns:
        Filtered data
    """
    filtered_data = []
    
    for item in data:
        if date_field in item:
            item_date = datetime.strptime(item[date_field], "%Y-%m-%dT%H:%M:%SZ").date()
            if start_date <= item_date <= end_date:
                filtered_data.append(item)
                
    return filtered_data

def convert_to_dataframe(data, fields):
    """
    Convert a list of dictionaries to a pandas DataFrame with selected fields
    
    Args:
        data: List of dictionaries
        fields: Dictionary mapping DataFrame column names to dictionary field paths
        
    Returns:
        pandas DataFrame
    """
    result = []
    
    for item in data:
        row = {}
        for col_name, field_path in fields.items():
            parts = field_path.split('.')
            value = item
            for part in parts:
                if part in value:
                    value = value[part]
                else:
                    value = None
                    break
            row[col_name] = value
        result.append(row)
        
    return pd.DataFrame(result)