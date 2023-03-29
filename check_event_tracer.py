import time
import pandas as pd
import datetime
from fuzzywuzzy import fuzz

if __name__ == '__main__':
    # Find the Event Tracer Download Path
    event_tracer_file = input('Enter the event tracer file path: ')
    event_tracer = pd.read_csv(event_tracer_file)
    match_type = input('Enter the match type (1,2,3): \n'
                       '1. IG source\n'
                       '2. Product Name + Purchase DateTime\n')


    partner_id = input('Enter the Partner ID: ')
    offer_id = input('Enter the Offer ID: ')

    event_tracer = event_tracer[event_tracer['publisher_id'] == int(partner_id)]
    event_tracer = event_tracer[event_tracer['offer_id'] == int(offer_id)]

    if match_type == '1':
        igsource = input('Enter the igsource: ')
        event_tracer['Match'] = event_tracer['sub'].str.contains(igsource)
        df_print = event_tracer[event_tracer['Match'] == True]
    elif match_type == '2':
        product_name = input('Enter the product or coupon name: ')
        event_tracer['Match'] = event_tracer['sub4'].apply(lambda x: fuzz.partial_ratio(x, product_name))

        purchase_date = input('Enter the purchase date (eg. 28/03/23 11:14): ')
        date_time_obj = datetime.datetime.strptime(purchase_date, '%d/%m/%y %H:%M')
        event_tracer['date'] = pd.to_datetime(event_tracer['date'])
        event_tracer['Time Diff'] = abs(event_tracer['date'] - date_time_obj)

        df_print = event_tracer.sort_values(by=['Match', 'Time Diff'], ascending=[False, True]).head(10)

    df_print.to_csv('event_tracer.csv', index=False)
    print("Saved to event_tracer.csv")