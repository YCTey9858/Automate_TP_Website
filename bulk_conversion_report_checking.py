import pandas as pd
import datetime
from fuzzywuzzy import fuzz

if __name__ == '__main__':
    # conversion_report_file = input('Enter the conversion report file path: ')
    conversion_report_file = '/Users/yichuantey/PycharmProjects/Automate_TP_Website/ConversionReport_2023-03-22-2023-03-22-4409.csv'
    conversion_report = pd.read_csv(conversion_report_file)

    # record_file = input('Enter the record file path: ')
    record_file = '/Users/yichuantey/PycharmProjects/Automate_TP_Website/test_conversion_report.xlsx'
    record = pd.read_excel(record_file)
    record['file'] = None
    record.fillna(value='None', inplace=True)

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