import requests
import pandas as pd

def get_number_of_channels(site_id):
    PU_CRED = {"X-Auth-Token": "4326:145rvcD4g1xgxsd6s4s3ss4aCaaF23as"}
    urls = 'https://platform-api.productsup.io/platform/v2/sites/' + str(site_id) + '/channels'

    response = requests.get(urls, headers=PU_CRED)
    json_file = response.json()
    number_of_channels = len(json_file['Channels'])

    print("Checking " + str(site_id) + ", number of channels: " + str(number_of_channels))

    return number_of_channels

if __name__ == '__main__':
    check_list = pd.read_csv('/Users/yichuantey/PycharmProjects/Automate_TP_Website/Productsup_iprice group Sdn Bhd-4326-20230330.csv')
    check_list.dropna(axis=1, inplace=True)
    check_list['number_of_channels'] = check_list['Site ID'].apply(get_number_of_channels)
    check_list.to_csv('output.csv', index=False)