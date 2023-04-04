"""
This script is used to check the number of channels for a site.

How to use:
1. Download the csv file from Productsup main page
2. Run the script and enter the csv file path
3. The output will be saved to output.csv

Potential Error:
1. file not found: check the file path
2. API cannot be reached: check the API key
3. output.csv is empty: check the site id
4. Package not found: check the package name and reinstall the package
"""

import requests
import pandas as pd


def get_number_of_channels(site_id):
    """
    Get the number of channels for a site
    """
    # Productsup API Key for iPrice Get from Productsup or your Manager
    PU_CRED = "Replace Me"

    # URL Formation
    urls = 'https://platform-api.productsup.io/platform/v2/sites/' + str(site_id) + '/channels'

    response = requests.get(urls, headers=PU_CRED)
    json_file = response.json()
    number_of_channels = len(json_file['Channels'])

    print("Checking " + str(site_id) + ", number of channels: " + str(number_of_channels))

    return number_of_channels


if __name__ == '__main__':
    # Read the csv file that download from Productsup main page
    check_list_path = input('Enter the full csv file path: ')
    check_list = pd.read_csv(check_list_path)
    check_list.dropna(axis=1, inplace=True)
    check_list['number_of_channels'] = check_list['Site ID'].apply(get_number_of_channels)
    check_list.to_csv('output.csv', index=False)
