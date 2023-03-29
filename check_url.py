import csv
import requests
from multiprocessing import Pool

def check_url(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
    except requests.exceptions.RequestException:
        status_code = 404
    return status_code

if __name__ == '__main__':
    # with open('/Users/yichuantey/PycharmProjects/Automate_TP_Website/iPrice_150030851_100k.csv', 'r') as infile, open('output.csv', 'w', newline='') as outfile:
    #     reader = csv.reader(infile)
    #     writer = csv.writer(outfile)
    #
    #     urls = [row[-5] for row in reader]
    #     chunksize = 1000  # process 1000 URLs at a time
    #     with Pool(processes=4) as pool:  # use 4 worker processes
    #         results = pool.imap_unordered(check_url, urls, chunksize)
    #
    #         for url, status_code in results:
    #             writer.writerow([url, status_code])
    #             print('Done')
    pass
