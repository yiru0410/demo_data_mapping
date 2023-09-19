import pandas as pd
import json
from datetime import datetime
import pytz


csv_file = 'SAP Contract Listing Report.csv'
df1 = pd.read_csv(csv_file)
print(df1)
metadata_contract = df1.loc[0]

csv_file = 'SAP PO Listing Report.csv'
df2 = pd.read_csv(csv_file)
print(df2)
metadata_po = df2.loc[0]

csv_file = 'BuySpeed Report.csv'
df3 = pd.read_csv(csv_file)
print(df3)
metadata_bs = df3.loc[0]

print("metadata_contrsct:")
print(metadata_contract)
print("metadata_po:")
print(metadata_po)
print("metadata_bs:")
print(metadata_bs)

def po_progress_data_transfer(date_string):
    date_object = datetime.strptime(date_string, "%B %d, %Y")
    desired_timezone = pytz.timezone("US/Pacific")
    localized_datetime = desired_timezone.localize(date_object.replace(hour=0, minute=0, second=0))
    formatted_date = localized_datetime.isoformat()
    return formatted_date

def contract_date_transfer(date_string):
    date_object = datetime.strptime(date_string, "%m/%d/%Y")
    desired_timezone = pytz.timezone("US/Pacific")
    localized_datetime = desired_timezone.localize(date_object.replace(hour=0, minute=0, second=0))
    formatted_date = localized_datetime.isoformat()
    return formatted_date

idx = 0
# awards/date
# print(df3.loc[0,"PO - In Progress Date"])
awards_date = po_progress_data_transfer(df3.loc[idx,"PO - In Progress Date"])
print(awards_date)

# awards/id
awards_id = df1.loc[idx,"Purchasing Document"]
print(awards_id)

# awards/status
if df2.loc[idx,"Delivery date"]:
    awards_status = "active"
print(awards_status)

# awards/value/amount
awards_value_amount = df2.loc[idx,"Order Quantity"].replace(',', '')
print(awards_value_amount)

# awards/value/currency
awards_value_currency = "USD"
print(awards_value_currency)

# awards/suppliers/name
awards_suppliers_name = df2.loc[idx, "Vendor Name"].title()
print(awards_suppliers_name)

# awards/suppliers/id

vendor_id = df2.loc[idx,"Vendor"]
awards_suppliers_id = f"pdx-vendor-{vendor_id}"
print(awards_suppliers_id)

# awards/contractPeriod/startDate
# print(df1.loc[idx,"Validity Per. Start"])
awards_contractPeriod_startDate = contract_date_transfer(df1.loc[idx,"Validity Per. Start"])
print(awards_contractPeriod_startDate)

# awards/contractPeriod/endDate
# print(df1.loc[idx,"Validity Period End"])
awards_contractPeriod_endDate = contract_date_transfer(df1.loc[idx,"Validity Period End"])
print(awards_contractPeriod_endDate)

# awards/title
awards_title = df1.loc[idx,"Short Text"].title()
print(awards_title)

# awards/description
awards_description = "Agreement for  construction services."
print(awards_description)
# Create awards library

awards = {
    "date": awards_date,
    "id": str(awards_id),
    "status": awards_status,
    "value":{
        "amount": awards_value_amount,
        "currency": awards_value_currency
    },
    "suppliers":{
        "name": awards_suppliers_name,
        "id": awards_suppliers_id
    },
    "contractPeriod":{
        "startDate": awards_contractPeriod_startDate,
        "endDate": awards_contractPeriod_endDate
    },
    "title": awards_title,
    "description": awards_description
}

print(awards)
file_name = "awards.json"

# Use a context manager to open the file and write the JSON data
with open(file_name, 'w') as json_file:
    json.dump(awards, json_file, indent=4)  # Serialize and write the data to the file with indentation
