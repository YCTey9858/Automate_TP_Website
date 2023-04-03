import time
import pandas as pd
import datetime
from fuzzywuzzy import fuzz

if __name__ == '__main__':
    # Find the Conversion Report Download Path
    conversion_report_file = input('Enter the conversion record file path: ')
    conversion_report = pd.read_csv(conversion_report_file)
    match_type = input('Enter the match type (1,2,3): \n'
                       '1. IG source\n'
                       '2. Product Name + Purchase DateTime + Transaction ID\n')


    partner_id = input('Enter the Partner ID: ')
    offer_id = input('Enter the Offer ID: ')

    conversion_report = conversion_report[conversion_report['affiliate_id'] == int(partner_id)]
    conversion_report = conversion_report[conversion_report['offer_id'] == int(offer_id)]

    if match_type == '1':
        igsource = input('Enter the igsource: ')
        conversion_report['Match'] = conversion_report['affiliate_source'].str.contains(igsource)
        df_print = conversion_report[conversion_report['Match'] == True]
    elif match_type == '2':
        product_name = input('Enter the product or coupon name: ')
        transaction_id = input('Enter the Transaction ID: ')

        conversion_report = conversion_report[conversion_report['transaction_id'] == transaction_id]
        conversion_report['Match'] = conversion_report['advertiser_sub_id_4'].apply(lambda x: fuzz.partial_ratio(str(x), product_name))

        purchase_date = input('Enter the purchase date (eg. 28/03/23 11:14): ')
        date_time_obj = datetime.datetime.strptime(purchase_date, '%d/%m/%y %H:%M')
        conversion_report['date_time'] = pd.to_datetime(conversion_report['date_time'])
        conversion_report['Time Diff'] = abs(conversion_report['date_time'] - date_time_obj)

        df_print = conversion_report.sort_values(by=['Match', 'Time Diff'], ascending=[False, True]).head(10)

    df_print.to_csv('conversion_report.csv', index=False)
    print("Saved to conversion_report.csv")