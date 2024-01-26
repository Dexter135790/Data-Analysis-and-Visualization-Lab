# Importing Necessary Libaries
import pandas as pd
import json

# Task 1:Create two data frames by reading above two files. 
# Reading the data from the csv file 
csv_data = pd.read_csv("district_level_service_msme.csv")

# Converting csv data to dataframe
df1 = pd.DataFrame(csv_data)

# Reading data from the json file
filepath="district_level_manufacturing_msme.json"
f = open(filepath)
data=json.load(f)

# Converting json data to dataframe
df=pd.DataFrame(data["data"])
clmns=[dic["label"] for dic in data["fields"]]
df2=pd.DataFrame(data["data"],columns=clmns)

# Task 1 Output
print("Task 1:  **************************************************")
print("Data Frame 1 is: ",df1)
print("Data Frame 2 is: ",df2)

# Task 2: Find out total ”Small” Manufacturing MSME in India. 
# Converting the data type of SMALL column to numeric
df2["SMALL"] = pd.to_numeric(df2["SMALL"])
small_msme = df2.groupby("STATE_NAME")["SMALL"].sum()
print("Task 2:  **************************************************")
print("Total Small Manufacturing MSME in India is: ",small_msme)

# Task 3: Create a dataframe having a state wise total number of ”Micro”,”Small” and ”Medium” Services MSE (as shown below) and save the results as a CSV file. 
pivot_table_result = df1.pivot_table(values=['SMALL', 'MICRO', 'MEDIUM'],
                                    index='STATE_NAME',
                                    aggfunc='sum')
print("Task 3:  **************************************************")
print(pivot_table_result)
# Saving the result as csv file
pivot_table_result.to_csv("state_wise_total.csv")

# Task 4: Join the both the data frame based on common STATE NAME, DISTRICT NAME, Lg Dist Code and Last Updated. The result should look like  ”x” and ”y” in the image  represent the manufacturing MSME and service MSME respectively.

# Converting the data type of Lg_Dist_Code column to numeric
df2['Lg_Dist_Code'] = df2['Lg_Dist_Code'].astype(int)
common_columns = ['STATE_NAME', 'DISTRICT_NAME', 'Lg_Dist_Code', 'Last_Updated']
# Merging the two dataframes
merged_df = pd.merge(df2, df1, on=["STATE_NAME", "DISTRICT_NAME", "Last_Updated", "Lg_Dist_Code"],how='inner', suffixes=('_x', '_y'))
print("Task 4:  **************************************************")
print("Merged Dataframe is : ")
print(merged_df)

# Task 5: Create a Pivot Table having rows STATE NAME and columns Service and Manufacturing ”MSME” as shown below. Use ”Sum” to add up district wise numbers. 

# Converting the data type of MICRO_x and MEDIUM_x columns to numeric
merged_df['MEDIUM_x'] = pd.to_numeric(merged_df['MEDIUM_x'], errors='coerce')
merged_df['MICRO_x'] = pd.to_numeric(merged_df['MICRO_x'], errors='coerce')

pivot_table_result = merged_df.pivot_table(values=["MICRO_x", "SMALL_x", "MEDIUM_x", "MICRO_y", "SMALL_y", "MEDIUM_y"],
                                    index=['STATE_NAME'] ,
                                    aggfunc='sum',
                                           dropna=False)
# Task 5 Output
print("Task 5:  **************************************************")
print("Result of task 5: ", pivot_table_result)


