import pandas as pd
import glob # will need glob when we have a big file of csvs
import re

# info will consist of "email": [First, Last, Year, major, gender, points]
studnet_info = {}
dues = {}
df = pd.read_csv(r"C:\Users\keita\Downloads\First GBM Sign-In (Responses) - Form Responses 1.csv")

# Initialize regex patterns
email_search = re.compile(r"email", re.IGNORECASE)
firstName_search = re.compile(r"first", re.IGNORECASE)
lastName_search = re.compile(r"last", re.IGNORECASE)
year_search = re.compile(r"year", re.IGNORECASE)
gender_search = re.compile(r"gender", re.IGNORECASE)
chapterDues_search = re.compile(r"chapter", re.IGNORECASE)
nationalDues_search = re.compile(r"national", re.IGNORECASE)

# Initialize variables to hold column names
email_column = None
firstName_column = None
lastName_column = None
year_column = None
gender_column = None
chapterDues_column = None
nationalDues_column = None

# Iterate over columns to match with regex patterns
for col in df.columns:
    if email_search.search(col):
        email_column = col
        df[email_column] = df[email_column].str.lower()

# Step 2: Drop duplicates based on the email column
        df = df.drop_duplicates(subset=[email_column]).reset_index(drop=True)
        email = df[email_column]#.str.lower()
    elif firstName_search.search(col):
        firstName_column = col
        firstName = df[firstName_column]
    elif lastName_search.search(col):
        lastName_column = col
        lastName = df[lastName_column]
    elif year_search.search(col):
        year_column = col
        year = df[year_column]
    elif gender_search.search(col):
        gender_column = col
        gender = df[gender_column]
    elif chapterDues_search.search(col):
        chapterDues_column = col
        chapterDues = df[chapterDues_column]
    elif nationalDues_search.search(col):
        nationalDues_column = col
        nationalDues = df[nationalDues_column]

# # Output the results
# print(f"Email Column: {email}")
# print(f"First Name Column: {firstName}")
# print(f"Last Name Column: {lastName}")
# print(f"Year Column: {year}")
# print(f"Gender Column: {gender}")
# print(f"Chapter Dues Column: {chapterDues}")
# print(f"National Dues Column: {nationalDues}")


    
points = int(input("How many points is event for?: "))
for info in range(len(df)):
    if email[info] not in studnet_info:
        studnet_info[email[info]] = [firstName[info],lastName[info],email[info],year[info],gender[info], points]
        if email[info] not in dues:
            dues[email[info]] = [chapterDues[info],nationalDues[info]]
    else:
        studnet_info[email[info]][5] += points
        if chapterDues_column != None and nationalDues_column != None:
            if chapterDues[info].strip().lower() == "Yes":
                dues[email[info]][0] = "Yes"
            if nationalDues[info].strip().lower() == "Yes":
                dues[email][1] = "Yes"

for stuff in studnet_info.items():
    print(stuff)
print(len(studnet_info))

