"""
This script is used to check the event tracer file for a specific partner, offer and purchase.

How to use:
1. Download the event tracer file from Has Offer event tracer page
2. Run the script and enter the event tracer file path
3. Enter the match type
    3.1 IG source
    3.1.1 Enter the igsource
    3.1.2 It will match the igsource in the sub column
    3.1.3 The output will be the event tracer file with the matched rows

    3.2 Product Name + Purchase DateTime
    3.2.1 Enter the product or coupon name
    3.2.2 Enter the purchase date (eg. 28/03/23 11:14)
    3.2.3 It will match the product name in the sub4 column and the purchase date in the date column
    3.2.4 The output will be the highest match score for each purchase
4. Save the output to event_tracer.csv

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
    # Find the Event Tracer Download Path
    event_tracer_file = input('Enter the event tracer file path: ')
    event_tracer = pd.read_csv(event_tracer_file)

    # Get the Match Type
    match_type = input('Enter the match type (1,2,3): \n'
                       '1. IG source\n'
                       '2. Product Name + Purchase DateTime\n')

    # Get the Partner ID and Offer ID
    partner_id = input('Enter the Partner ID: ')
    offer_id = input('Enter the Offer ID: ')

    # Filter the Event Tracer
    event_tracer = event_tracer[event_tracer['publisher_id'] == int(partner_id)]
    event_tracer = event_tracer[event_tracer['offer_id'] == int(offer_id)]

    # Match the Event Tracer
    if match_type == '1':
        igsource = input('Enter the igsource: ')
        event_tracer['Match'] = event_tracer['sub'].str.contains(igsource)
        df_print = event_tracer[event_tracer['Match'] == True]
    elif match_type == '2':
        product_name = input('Enter the product or coupon name: ')

        # Match the product name or coupon name
        event_tracer['Match'] = event_tracer['sub4'].apply(lambda x: fuzz.partial_ratio(x, product_name))

        # Match the purchase date
        purchase_date = input('Enter the purchase date (eg. 28/03/23 11:14): ')
        date_time_obj = datetime.datetime.strptime(purchase_date, '%d/%m/%y %H:%M')
        event_tracer['date'] = pd.to_datetime(event_tracer['date'])
        event_tracer['Time Diff'] = abs(event_tracer['date'] - date_time_obj)

        # Get the highest match score for each purchase
        df_print = event_tracer.sort_values(by=['Match', 'Time Diff'], ascending=[False, True]).head(10)

    df_print.to_csv('event_tracer.csv', index=False)
    print("Saved to event_tracer.csv")
