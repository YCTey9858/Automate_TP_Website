import requests
import pandas as pd
def check_url(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
    except requests.exceptions.RequestException:
        status_code = 404
    print("Checking " + url + ", status code: " + str(status_code))
    return status_code

if __name__ == '__main__':
    url = input('Enter the file path: ')
    df = pd.read_csv(url)
    product_url_column = input('Enter the product url column name: ')
    df['status_code'] = df[product_url_column].apply(check_url)
    df.to_csv('output.csv', index=False)
    print('Done')
