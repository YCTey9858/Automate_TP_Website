"""
This script is used to check the conversion report from the Has Offer.

How to use:
1. Download the conversion report from Has Offer conversion report page
2. Run the script and enter the conversion report file path
3. Enter the match type
    3.1 IG source
    3.1.1 Enter the igsource
    3.1.2 It will match the igsource in the affiliate_source column
    3.1.3 The output will be the conversion report file with the matched rows

    3.2 Product Name + Purchase DateTime + Transaction ID
    3.2.1 Enter the product or coupon name
    3.2.2 Enter the Transaction ID
    3.2.3 Enter the purchase date (eg. 28/03/23 11:14)
    3.2.4 It will match the product name in the advertiser_sub_id_4 column and the purchase date in the date column
    3.2.5 The output will be the highest match score for each purchase

4. Save the output to conversion_report.csv

Potential Error:
1. file not found: check the file path
2. output.csv is empty: check your input as it can be empty for no record found
3. date format error: check the date format
4. fuzzywuzzy error: check the product name
5. Package not found: pip install fuzzywuzzy and pandas
"""
import time
import pandas as pd
import datetime
from fuzzywuzzy import fuzz

if __name__ == '__main__':
    # Find the Conversion Report Download Path
    conversion_report_file = input('Enter the conversion record file path: ')
    conversion_report = pd.read_csv(conversion_report_file)

    # Get the Match Type
    match_type = input('Enter the match type (1,2,3): \n'
                       '1. IG source\n'
                       '2. Product Name + Purchase DateTime + Transaction ID\n')

    # Get the Partner ID and Offer ID
    partner_id = input('Enter the Partner ID: ')
    offer_id = input('Enter the Offer ID: ')

    conversion_report = conversion_report[conversion_report['affiliate_id'] == int(partner_id)]
    conversion_report = conversion_report[conversion_report['offer_id'] == int(offer_id)]

    # Match the Conversion Report
    if match_type == '1':
        igsource = input('Enter the igsource: ')
        conversion_report['Match'] = conversion_report['affiliate_source'].str.contains(igsource)
        df_print = conversion_report[conversion_report['Match'] == True]
    elif match_type == '2':
        # Get the Product Name and Transaction ID
        product_name = input('Enter the product or coupon name: ')
        transaction_id = input('Enter the Transaction ID: ')

        # Match the Product Name and Transaction ID
        conversion_report = conversion_report[conversion_report['transaction_id'] == transaction_id]
        conversion_report['Match'] = conversion_report['advertiser_sub_id_4'].apply(
            lambda x: fuzz.partial_ratio(str(x), product_name))

        # Get the Purchase Date
        purchase_date = input('Enter the purchase date (eg. 28/03/23 11:14): ')
        date_time_obj = datetime.datetime.strptime(purchase_date, '%d/%m/%y %H:%M')
        conversion_report['date_time'] = pd.to_datetime(conversion_report['date_time'])

        # Match the Purchase Date
        conversion_report['Time Diff'] = abs(conversion_report['date_time'] - date_time_obj)

        # Get the Highest Match Score
        df_print = conversion_report.sort_values(by=['Match', 'Time Diff'], ascending=[False, True]).head(10)

    df_print.to_csv('conversion_report.csv', index=False)
    print("Saved to conversion_report.csv")
