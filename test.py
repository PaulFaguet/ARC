from classes.arc_multiple import ARC_Multiple
import pandas as pd 
from datetime import datetime, timedelta


# create a function that takes one argument, the number of months to add
def getDateAfterMonths(start_date, months):
    """
    Function used to get the date after X months to check results on Google Search Console
    """
    
    results = {
        "M-1": {
            "start_date": (datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=31)).strftime('%Y-%m-%d'),
            "end_date": start_date
        },
        "M+1": {
            "start_date": start_date,
            "end_date": (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d')
        }
    }
    
    for i in range(1, months):
        start_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=31)).strftime('%Y-%m-%d')
        results[f"M+{i+1}"] = {
            "start_date": start_date,
            "end_date": (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=31)).strftime('%Y-%m-%d')
        }
        
    return results

