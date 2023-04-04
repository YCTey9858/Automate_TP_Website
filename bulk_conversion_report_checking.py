"""
This script is used to check the conversion report for bulk records.

How to use:
1. Download the conversion report from Has Offer conversion report page
2. Run the script and enter the conversion report file path
3. Enter the record file path
4. Match the conversion report with the record file
    4.1 Match the partner_id and offer_id (filter)
    4.2 Match the product name, transaction_id and purchase date (fuzzywuzzy) or igsource (contains)
5. Save each record to a csv file
6. Save the record file with the file name

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

    # Find the Conversion Report Download Path
    conversion_report_file = input('Enter the conversion report file path: ')
    # conversion_report_file = '/Users/yichuantey/PycharmProjects/Automate_TP_Website/ConversionReport_2023-03-22-2023-03-22-4409.csv'
    conversion_report = pd.read_csv(conversion_report_file)

    # Find the Record File Path
    record_file = input('Enter the record file path: ')
    # record_file = '/Users/yichuantey/PycharmProjects/Automate_TP_Website/test_conversion_report.xlsx'
    record = pd.read_excel(record_file)
    record['file'] = None
    record.fillna(value='None', inplace=True)

    # Match the Conversion Report with the Record, the method check with the single checker
    for index, row in record.iterrows():
        conversion_report = conversion_report[conversion_report['affiliate_id'] == int(row['partner_id'])]
        conversion_report = conversion_report[conversion_report['offer_id'] == int(row['offer_id'])]

        product_name = row['product_name']
        transaction_id = row['transaction_id']
        igsource = str(row['igsource'])
        if igsource != 'None':
            conversion_report['Match'] = conversion_report['affiliate_source'].str.contains(igsource)
            df_print = conversion_report[conversion_report['Match'] == True]

        else:
            conversion_report = conversion_report[conversion_report['transaction_id'] == transaction_id]
            conversion_report['Match'] = conversion_report['advertiser_sub_id_4'].apply(lambda x: fuzz.partial_ratio(str(x), product_name))

            purchase_date = row['purchase_date'].strip()
            date_time_obj = datetime.datetime.strptime(purchase_date, '%d/%m/%y %H:%M')
            conversion_report['date_time'] = pd.to_datetime(conversion_report['date_time'])
            conversion_report['Time Diff'] = abs(conversion_report['date_time'] - date_time_obj)

            df_print = conversion_report.sort_values(by=['Match', 'Time Diff'], ascending=[False, True]).head(10)
        row['file'] = 'Record' + str(index)
        record.at[index, 'file'] = 'Record' + str(index) + '.csv'
        df_print.to_csv(row['file'], index=False)
        print("Done for record " + str(index))
    record.to_excel(record_file, index=False)