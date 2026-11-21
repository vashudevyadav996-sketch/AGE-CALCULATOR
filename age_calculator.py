# AGE CALCULATOR 
import os
import random
from datetime import date
import numpy as np
import pandas as pd

file_name = "people.csv"

# ---------------------------------------------------------
# PYTHON DATA STRUCTURES
# ---------------------------------------------------------
# TUPLE - month names (values never change)
month_names = ("January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December")

# LIST - weekday names
weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]

# DICTIONARY - age group and its maximum age
age_groups = {"Child": 12, "Teenager": 19, "Young Adult": 35,
              "Adult": 59, "Senior": 200}

# SET - the separators we allow in a date (no duplicates)
allowed_separators = {"-", "/"}

# lists used for creating the dataset
first_names = ["Aman", "Shivam", "Ayush", "Harsh", "Saurabh", "Nikhil",
               "Anjali", "Shruti", "Pallavi", "Komal", "Divya", "Sakshi",
               "Vikas", "Deepak", "Manish", "Ritu", "Nisha", "Gaurav"]
last_names = ["Tiwari", "Pandey", "Chaubey", "Rai", "Maurya", "Srivastava", "Kushwaha"]
cities = ["Ballia", "Varanasi", "Lucknow", "Gorakhpur", "Kanpur", "Prayagraj", "Ghazipur"]


# ---------------------------------------------------------
# AGE FUNCTIONS
# ---------------------------------------------------------
# Function 1: convert text like 2000-05-21 into a date
def make_date(text):
    text = text.strip()
    for sep in allowed_separators:
        text = text.replace(sep, "-")
    parts = text.split("-")
    if len(parts) != 3:
        return None
    try:
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        return date(year, month, day)
    except ValueError:
        return None


# Function 2: calculate age in years, months and days
def calculate_age(dob):
    today = date.today()
    years = today.year - dob.year
    months = today.month - dob.month
    days = today.day - dob.day

    if days < 0:
        months = months - 1
        days = days + 30      # we take 30 days in a month (simple method)
    if months < 0:
        years = years - 1
        months = months + 12
    return years, months, days


# Function 3: total days lived
def total_days(dob):
    today = date.today()
    difference = today - dob
    return difference.days


# Function 4: days left for next birthday
def days_to_birthday(dob):
    today = date.today()
    day = dob.day
    if dob.month == 2 and dob.day == 29:
        day = 28              # for people born on 29 February
    birthday = date(today.year, dob.month, day)
    if birthday < today:
        birthday = date(today.year + 1, dob.month, day)
    difference = birthday - today
    return difference.days


# Function 5: find age group
def find_age_group(age):
    for group in age_groups:
        if age <= age_groups[group]:
            return group
    return "Unknown"


# Function 6: find the weekday on which the person was born
def birth_weekday(dob):
    number = dob.weekday()
    return weekday_names[number]


# ---------------------------------------------------------
# DATASET AND FILE HANDLING FUNCTIONS
# ---------------------------------------------------------
# Create the dataset (60 records) and save it as a CSV file
def create_dataset():
    random.seed(2026)

    ids = []
    names = []
    dobs = []
    city_list = []
    emails = []

    for i in range(1, 61):
        name = random.choice(first_names) + " " + random.choice(last_names)
        year = random.randint(1958, 2012)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        dob = str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)
        city = random.choice(cities)
        email = name.split()[0].lower() + str(i) + "@gmail.com"

        # leave some values empty so we can practise missing values
        if i % 9 == 0:
            email = ""
        if i % 14 == 0:
            city = ""

        ids.append(i)
        names.append(name)
        dobs.append(dob)
        city_list.append(city)
        emails.append(email)

    data = {"ID": ids, "Name": names, "DOB": dobs,
            "City": city_list, "Email": emails}
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)
    print("Dataset created with", len(df), "records.")


# Read the file using normal python file handling
def read_file_lines():
    file = open(file_name, "r")
    lines = file.readlines()
    file.close()
    return lines


# Read the CSV file with pandas and add Age and Age Group columns
def load_data():
    df = pd.read_csv(file_name)

    ages = []
    groups = []
    for dob_text in df["DOB"]:
        dob = make_date(dob_text)
        years, months, days = calculate_age(dob)
        ages.append(years)
        groups.append(find_age_group(years))

    df["Age"] = ages
    df["Age Group"] = groups
    return df


# Save the data back to the CSV file
def save_data(df):
    df[["ID", "Name", "DOB", "City", "Email"]].to_csv(file_name, index=False)


# ---------------------------------------------------------
# PROJECT OPERATIONS: ADD, DISPLAY, SEARCH
# ---------------------------------------------------------
# Operation 1: add a new record
def add_record(df, name, dob_text, city, email):
    dob = make_date(dob_text)
    years, months, days = calculate_age(dob)
    group = find_age_group(years)

    new_id = df["ID"].max() + 1
    if city == "":
        city = None
    if email == "":
        email = None

    df.loc[len(df)] = [new_id, name, dob_text, city, email, years, group]
    return df


# Operation 2: display all records
def display_all(df):
    print(df.to_string())
    print("Total records:", len(df))


# Operation 3: search a record by ID or by name
def search_record(df, text):
    if text.isdigit():
        result = df[df["ID"] == int(text)]
    else:
        result = df[df["Name"].str.contains(text, case=False)]
    return result


# ---------------------------------------------------------
# NUMPY AND PANDAS PRACTICE
# ---------------------------------------------------------
def numpy_work(df):
    print("----- NUMPY -----")

    # 1D array
    ages = np.array(df["Age"].tolist())
    print("1D array of ages (first 10):", ages[0:10])

    # 2D array (2 rows and 3 columns)
    table = np.array([[ages[0], ages[1], ages[2]],
                      [ages[3], ages[4], ages[5]]])
    print("2D array:")
    print(table)

    # indexing
    print("ages[0] =", ages[0])
    print("table[1][2] =", table[1][2])

    # slicing
    print("ages[2:6] =", ages[2:6])
    print("first row of table =", table[0])
    print("last 3 ages =", ages[-3:])

    # sum, mean, max, min, standard deviation
    print("Sum =", np.sum(ages))
    print("Mean =", round(np.mean(ages), 2))
    print("Maximum =", np.max(ages))
    print("Minimum =", np.min(ages))
    print("Standard deviation =", round(np.std(ages), 2))


def pandas_work(df):
    print("----- PANDAS -----")

    # create a small DataFrame
    small = pd.DataFrame({"Name": ["Ram", "Sita", "Mohan"], "Marks": [80, 90, 70]})
    print("Small DataFrame:")
    print(small)

    # selecting rows and columns
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nName and Age columns (first 5 rows):")
    print(df[["Name", "Age"]].head())
    print("\nRows 10 to 14:")
    print(df.iloc[10:15])

    # filtering
    print("\nPeople older than 50:")
    older = df[df["Age"] > 50]
    print(older[["ID", "Name", "Age"]])

    print("\nPeople from Ballia:")
    ballia = df[df["City"] == "Ballia"]
    print(ballia[["ID", "Name", "City"]])

    # sorting
    print("\nTop 5 oldest people:")
    sorted_df = df.sort_values("Age", ascending=False)
    print(sorted_df[["Name", "Age"]].head())

    # groupby
    print("\nAverage age in each city:")
    print(df.groupby("City")["Age"].mean())
    print("\nNumber of people in each age group:")
    print(df.groupby("Age Group")["ID"].count())

    # missing values
    print("\nMissing values in each column:")
    print(df.isnull().sum())
    df2 = df.fillna("Not given")
    print("Missing values after fillna:", df2.isnull().sum().sum())

    # statistics
    print("\nStatistics of Age:")
    print(df["Age"].describe())
    print("Median age:", df["Age"].median())


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
# create the dataset if the file is not there
if not os.path.exists(file_name):
    create_dataset()

lines = read_file_lines()
print("File read successfully. Total lines in file:", len(lines))
df = load_data()

# LIST of menu options
menu = ["1. Calculate age", "2. Add new record", "3. Display all records",
        "4. Search a record", "5. Pandas analysis", "6. NumPy analysis", "7. Exit"]

while True:
    print("\n===== AGE CALCULATOR =====")
    for item in menu:
        print(item)
    choice = input("Enter your choice (type a number from 1 to 7): ")

    if choice == "1":
        text = input("Enter date of birth (YYYY-MM-DD): ")
        dob = make_date(text)
        if dob is None:
            print("Wrong date! Please try again.")
        else:
            years, months, days = calculate_age(dob)
            print("Your age is", years, "years", months, "months", days, "days")
            print("Age group:", find_age_group(years))
            print("Total days lived:", total_days(dob))
            print("Days left for next birthday:", days_to_birthday(dob))
            print("You were born on a", birth_weekday(dob))

    elif choice == "2":
        name = input("Enter name: ")
        dob_text = input("Enter date of birth (YYYY-MM-DD): ")
        if make_date(dob_text) is None:
            print("Wrong date! Record not added.")
        else:
            city = input("Enter city (press enter to skip): ")
            email = input("Enter email (press enter to skip): ")
            df = add_record(df, name, dob_text, city, email)
            save_data(df)
            print("Record added successfully.")

    elif choice == "3":
        display_all(df)

    elif choice == "4":
        text = input("Enter ID or name to search: ")
        result = search_record(df, text)
        if len(result) == 0:
            print("No record found.")
        else:
            print(result.to_string())

    elif choice == "5":
        pandas_work(df)

    elif choice == "6":
        numpy_work(df)

    elif choice == "7":
        print("Thank you!")
        break

    else:
        print("Invalid choice! Please type only a number from 1 to 7.")
        print("(Type 2 to add a record, or 4 to search by name - the program will ask for the name after that.)")