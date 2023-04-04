"""
This script will check the status code of a list of urls in a csv file.
The csv file should have a column with the urls.

How to use:
1. Get your target file path
2. Run the script and enter the file path
3. Enter the column name of the urls
4. The output will be saved to output.csv

Potential Error:
1. file not found: check the file path
2. output.csv is empty: check the column name
3. all 404: check the url manually
4. all 503: Block by the website
"""

import requests
import pandas as pd


def check_url(url):
    """
    Check the status code of a url
    """
    try:
        response = requests.get(url)
        status_code = response.status_code
    except requests.exceptions.RequestException:
        status_code = 404
    print("Checking " + url + ", status code: " + str(status_code))
    return status_code


if __name__ == '__main__':
    # Read the csv file
    url = input('Enter the file path: ')
    df = pd.read_csv(url)

    # Get the column name of the urls
    product_url_column = input('Enter the product url column name: ')

    # Check the status code of the urls
    df['status_code'] = df[product_url_column].apply(check_url)

    # Save the output to output.csv
    df.to_csv('output.csv', index=False)
    print('Done')
