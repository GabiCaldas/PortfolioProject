#Import libraries
import pandas as pd
import numpy as np
import os
from datetime import datetime


df = pd.read_excel(r'\\xxxxxxxxxxxxx\HIX0332 - MA21 Notice ID_D2023-08-04.xlsx', dtype={'MEMBER_SSN': str, 'NOTICE_ID': str, 'MAIL_ZIP': str, 'HOME_ZIP': str, 'MEMBER_ACTIVE_ID_MEDICAID': str})

#Define folder path
folder_name = datetime.today().strftime('%Y %m %d')
folder_path = r'\\xxxxxxxxxxxx\OPERATIONS' + '/' + folder_name

# Check if the folder already exists
if not os.path.exists(folder_path):
    # Create the folder if it doen't exist
    os.makedirs(folder_path)
    print(f"Folder '{folder_name}' created successfully.")
else:
    print(f"Folder '{folder_name}' already exists.")

pd.set_option('display.max.rows', 206)

#Sort NOTICE_PRINT_DATE by newest to oldest
df.sort_values(by= 'NOTICE_PRINT_DATE', ascending= False)

#Delete all rows except current file date
dropdf=df[(df['NOTICE_PRINT_DATE'] < '2023-08-04')].index
df.drop(dropdf, inplace=True)

#Delete rows that have NULLS
df= df.dropna(subset=['NOTICE_PRINT_DATE'])
#Find the number of rows
df.shape

#Remove duplicates based on the NOTICE_ID
df= df.drop_duplicates(subset=['NOTICE_ID'])

#Format the columns DOB and Notice print date
df['MEMBER_DATE_OF_BIRTH']= df['MEMBER_DATE_OF_BIRTH'].dt.strftime('%m/%d/%Y')
df['NOTICE_PRINT_DATE']= df['NOTICE_PRINT_DATE'].dt.strftime('%m/%d/%Y')

# Drop the extra columns
extra_columns=['AIDCAT', 'AIDCAT_EFF', 'AIDCAT_END', 'AGENCY', 'ARD_LAST_NAME', 'ARD_FIRST_NAME', 'ARD_MIDDLE_NAME', 'ARD_ADDR_LINE1', 'ARD_ADDR_LINE2', 'ARD_CITY', 'ARD_STATE', 'ARD_ZIP', 'ARD_LAST_NAME_2', 'ARD_FIRST_NAME_2', 'ARD_MIDDLE_NAME_2', 'ARD_ADDR_LINE1_2', 'ARD_ADDR_LINE2_2', 'ARD_CITY_2', 'ARD_STATE_2', 'ARD_ZIP_2', 'ARD_LAST_NAME_3', 'ARD_FIRST_NAME_3', 'ARD_MIDDLE_NAME_3', 'ARD_ADDR_LINE1_3', 'ARD_ADDR_LINE2_3', 'ARD_CITY_3', 'ARD_STATE_3',	'ARD_ZIP_3', 'ARD_LAST_NAME_4', 'ARD_FIRST_NAME_4', 'ARD_MIDDLE_NAME_4', 'ARD_ADDR_LINE1_4', 'ARD_ADDR_LINE2_4', 'ARD_CITY_4', 'ARD_STATE_4', 'ARD_ZIP_4', 'ARD_LAST_NAME_5', 'ARD_FIRST_NAME_5', 'ARD_MIDDLE_NAME_5', 'ARD_ADDR_LINE1_5', 'ARD_ADDR_LINE2_5', 'ARD_CITY_5', 'ARD_STATE_5', 'ARD_ZIP_5']
df = df.drop(extra_columns, axis=1)

#Sort MEMBER_SSN by newest to oldest
df.sort_values(by= 'MEMBER_SSN', ascending= False)

# Replace NaN values to 0s
df['MEMBER_SSN']=df2['MEMBER_SSN'].replace(np.NaN, 0)

# Capitalize the first letter and lower case the rest
# Need to fix the address
df['MEMBER_LAST_NAME'] = df['MEMBER_LAST_NAME'].str.title()
df['MEMBER_FIRST_NAME'] = df['MEMBER_FIRST_NAME'].str.title()
df['HOME_ADDR_LINE1'] = df['HOME_ADDR_LINE1'].str.title()
df['HOME_ADDR_LINE2'] = df['HOME_ADDR_LINE2'].str.title()
df['HOME_CITY'] = df['HOME_CITY'].str.title()
df['MAIL_ADDR_LINE1'] = df['MAIL_ADDR_LINE1'].str.title()
df['MAIL_ADDR_LINE2'] = df['MAIL_ADDR_LINE2'].str.title()
df['MAIL_CITY'] = df['MAIL_CITY'].str.title()

#Add dashes at specific positions in a 9-digit number
df['MEMBER_SSN'] = df['MEMBER_SSN'].str[:3] + '-' + df['MEMBER_SSN'].str[3:5] + '-' + df['MEMBER_SSN'].str[5:]

# Add leading 0s to Notice_ID column until you get 11-digits
df['NOTICE_ID'] = df['NOTICE_ID'].str.zfill(11)

#Remove bad phone numbers
df.sort_values(by= 'PHONE_NUMBER_1', ascending= False)
df['PHONE_NUMBER_1'] = df['PHONE_NUMBER_1'].replace(['1111111111', '9999999999', '+'], '')

#Remove bad phone numbers- Phone number 2
df.sort_values(by= 'PHONE_NUMBER_2', ascending= False)
df['PHONE_NUMBER_2'] = df2['PHONE_NUMBER_2'].replace(['1111111111', '9999999999', '6170000000', '7740000000', '+'], '')

#Extract the first 5 digits from the zip codes. 
df['MAIL_ZIP'] = df['MAIL_ZIP'].str[:5]
df['HOME_ZIP'] = df['HOME_ZIP'].str[:5]

#Set the Excel writer object
writer = pd.ExcelWriter(r'\\xxxxxxxxxxxxx\OPERATIONS\2023 08 04\2023 08 04 HIX0332 - MA21 Notice ID.xlsx', engine = 'xlsxwriter')
df2= df2.to_excel(writer, sheet_name = 'Sheet1', index = False)
workbook= writer.book
worksheet = writer.sheets['Sheet1']

#Freeze the top row
worksheet.freeze_panes(1,0)

# Save the Excel file
writer.save()