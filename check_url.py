"""Check if a URL is valid or not."""
import requests

def check_url(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
    except requests.exceptions.RequestException:
        status_code = 404
    return status_code

if __name__ == '__main__':
    url = input('Enter the url: ')
    print(check_url(url))
