"""
This script is to check the event tracer for a list of records.

How to use:
1. Get the event tracer file path that download by yourself
2. Get the record file path
3. Run the script and enter the event tracer file path
4. Run the script and enter the record file path
5. Match the event tracer with the record
    5.1 Match the partner id (filter)
    5.2 Match the order id (filter)
    5.3 Match the igsource or product name + purchase date
6. Save each record to a csv file
7. Save the output back to the record file

Potential Error:
1. file not found: check the file path
2. each record file is empty: check your input as it can be empty for no record found
3. data type error: check the data type of the record file
4. date format error: check the date format
5. fuzzywuzzy error: check the product name
6. Package not found: pip install fuzzywuzzy and pandas
"""
import pandas as pd
import datetime
from fuzzywuzzy import fuzz

if __name__ == '__main__':

    # Find the Event Tracer Download Path
    event_tracer_file = input('Enter the event tracer file path: ')
    # event_tracer_file = '/Users/yichuantey/PycharmProjects/Automate_TP_Website/eventLog_2023-03-28_11-44-01.csv'
    event_tracer = pd.read_csv(event_tracer_file)

    # Find the Record File Path
    record_file = input('Enter the record file path: ')
    # record_file = '/Users/yichuantey/PycharmProjects/Automate_TP_Website/test_event_tracer.xlsx'
    record = pd.read_excel(record_file)
    record['file'] = None
    record.fillna(value='None', inplace=True)

    # Match the Event Tracer with the Record, the method check with the single checker
    for index, row in record.iterrows():
        event_tracer = event_tracer[event_tracer['publisher_id'] == int(row['partner_id'])]
        event_tracer = event_tracer[event_tracer['offer_id'] == int(row['offer_id'])]

        product_name = row['product_name']
        igsource = str(row['igsource'])

        if igsource != 'None':
            event_tracer['Match'] = event_tracer['sub'].str.contains(igsource)
            df_print = event_tracer[event_tracer['Match'] == True]

        else:
            event_tracer['Match'] = event_tracer['sub4'].apply(lambda x: fuzz.partial_ratio(x, product_name))

            purchase_date = row['purchase_date'].strip()
            date_time_obj = datetime.datetime.strptime(purchase_date, '%d/%m/%y %H:%M')
            event_tracer['date'] = pd.to_datetime(event_tracer['date'])
            event_tracer['Time Diff'] = abs(event_tracer['date'] - date_time_obj)

            df_print = event_tracer.sort_values(by=['Match', 'Time Diff'], ascending=[False, True]).head(10)

        row['file'] = 'Record' + str(index)
        record.at[index, 'file'] = 'Record' + str(index) + '.csv'
        df_print.to_csv(row['file'], index=False)
        print("Done for record " + str(index))
    record.to_excel(record_file, index=False)
