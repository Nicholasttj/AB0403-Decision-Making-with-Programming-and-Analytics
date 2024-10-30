#!/usr/bin/env python
# coding: utf-8

# In[3]:


#(1) Overall COE Trends

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
coe_data = pd.read_csv('COE.csv')

# Extract year from 'month' column
coe_data['year'] = pd.to_datetime(coe_data['month']).dt.year

# Calculate the average COE premium for each year
average_premium_by_year = coe_data.groupby('year')['premium'].mean()

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.plot(average_premium_by_year.index, average_premium_by_year.values, marker='o', linestyle='-')
plt.title('Average COE Premium Over Years')
plt.xlabel('Year')
plt.ylabel('Average COE Premium (SGD)')
plt.grid(True)
plt.show()


# In[9]:


#(2) Relationship between COE Premium and COE Registrations/Renewals

import pandas as pd
import matplotlib.pyplot as plt

coe_data = pd.read_csv('COE.csv')
new_registrations_data = pd.read_csv('TotalAnnualNewRegistrationByMake.csv')
age_distribution_data = pd.read_csv('AnnualAgeDistributionofCars.csv')

# Compare COE renewal candidates with total new car registrations
age_distribution = age_distribution_data.pivot(index='year', columns='age_year', values='number')
total_registrations_by_year = new_registrations_data.groupby('year')['number'].sum()

# Plotting
fig, ax1 = plt.subplots(figsize=(12, 7))
ax2 = ax1.twinx()
age_distribution['10-<11'].plot(ax=ax1, color='b', label='Cars aged 10-11 (COE Renewal Candidates)')
total_registrations_by_year.plot(ax=ax2, color='g', label='Total New Car Registrations', linestyle='--')
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Vehicles (Aged 10-11 Years)')
ax2.set_ylabel('Total New Car Registrations')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.title('COE Renewal Candidates vs. Total New Car Registrations')
plt.grid(True)
plt.show()


# In[10]:


#(3) Navigating Finances in Vehicle Purchase for Growing Families

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data from the CSV file
file_path = 'COE.csv'
coe_data = pd.read_csv(file_path)

# Filter out the data for vehicle classes A and B
class_a_b_data = coe_data[(coe_data['vehicle_class'] == 'Category A') | (coe_data['vehicle_class'] == 'Category B')]

# Separate the data into two parts for plotting
bids_success_data = class_a_b_data[['vehicle_class', 'bids_success']]
premium_data = class_a_b_data[['vehicle_class', 'premium']]

# Define custom colors for the box plots
custom_colors = sns.color_palette("Set2")

# Create the box plots
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

# Box plot for average successful bids with red and blue colors for Category A and B respectively
sns.boxplot(ax=axes[0], data=bids_success_data, x='vehicle_class', y='bids_success', palette=custom_colors[:2])
axes[0].set_title('Box Plot of Average Successful Bids for Classes A and B')
axes[0].set_xlabel('Vehicle Class')
axes[0].set_ylabel('Average Successful Bids')

# Box plot for COE premiums with green and yellow colors for Category A and B respectively
sns.boxplot(ax=axes[1], data=premium_data, x='vehicle_class', y='premium', palette=custom_colors[2:])
axes[1].set_title('Box Plot of COE Premium for Classes A and B')
axes[1].set_xlabel('Vehicle Class')
axes[1].set_ylabel('COE Premium')

# Show the plots
plt.tight_layout()
plt.show()


# In[11]:


#(4) Top 5 Family Car Brands Among Young Families

import pandas as pd
import matplotlib.pyplot as plt

# Step 2: Read the CSV file into a DataFrame
df = pd.read_csv('TotalAnnualNewRegistrationByMake.csv')

# List of 5 brands you have in mind
selected_brands = ['KIA', 'NISSAN', 'SKODA', 'PEUGEOT', 'TOYOTA']

# Step 3: Filter the DataFrame to include only the selected brands
filtered_df = df[df['make'].isin(selected_brands)]

filtered_df = filtered_df.drop(['year'],axis=1).groupby('make').mean().reset_index()

# Step 4: Create the pie chart
plt.figure(figsize=(10, 8))
plt.pie(filtered_df['number'], labels=filtered_df['make'], autopct='%1.1f%%')
plt.title('Family Car Brands Distribution')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()


# In[12]:


#(5) Impact of COE Premium Prices on Car Brand Preference

import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
coe_path = "COE.csv"
registrations_path = "TotalAnnualNewRegistrationByMake.csv"

coe_data = pd.read_csv(coe_path)
registrations_data = pd.read_csv(registrations_path)

# Convert 'month' in COE data to datetime and extract the year for aggregation
coe_data['year'] = pd.to_datetime(coe_data['month']).dt.year

# Filter COE data for Category A and B only
category_a_b_coe = coe_data[coe_data['vehicle_class'].isin(['Category A', 'Category B'])]

# Calculate the annual average COE premium for Category A and B
annual_coe_average_category_a_b = category_a_b_coe.groupby('year')['premium'].mean().reset_index()

# Normalize the COE premium data for Category A and B
max_premium_category_a_b = annual_coe_average_category_a_b['premium'].max()
annual_coe_average_category_a_b['normalized_premium'] = annual_coe_average_category_a_b['premium'] / max_premium_category_a_b

# Merge the annual COE averages with the Total Annual New Registration by Make dataset
merged_data = pd.merge(registrations_data, annual_coe_average_category_a_b[['year', 'normalized_premium']], on='year', how='inner')

# Normalizing registrations for each brand
def normalize_and_plot(data, brand, color, ax):
    brand_data = data[data['make'] == brand].copy()  # Create a copy to modify
    max_registrations = brand_data['number'].max()
    brand_data.loc[:, 'normalized_registrations'] = brand_data['number'] / max_registrations
    ax.bar(brand_data['year'], brand_data['normalized_registrations'], color=color, label=f'{brand} Registrations')
    ax.plot(annual_coe_average_category_a_b['year'], annual_coe_average_category_a_b['normalized_premium'], color='red', label='COE Premium')
    ax.set_xlabel('Year')
    ax.set_ylabel('Proportion of Maximum Value')
    ax.set_title(f'{brand} Registrations and COE Premiums for Category A and B Over Time')
    ax.legend()

# Create subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 18))

normalize_and_plot(merged_data, 'TOYOTA', 'blue', axs[0])
normalize_and_plot(merged_data, 'AUDI', 'green', axs[1])
normalize_and_plot(merged_data, 'KIA', 'orange', axs[2])

plt.tight_layout()
plt.show()


# In[14]:


#(6) A Look Into the Future

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load the data from the CSV file
file_path = 'TotalAnnualNewRegistrationByMake.csv'
car_registrations = pd.read_csv(file_path)

# Filter out the data for BYD
byd_registrations = car_registrations[car_registrations['make'] == 'BYD']

# Only consider complete years, excluding any partial data for 2023 if present
byd_registrations_complete = byd_registrations[byd_registrations['year'] < 2023]

# Prepare the data for linear regression model
X_byd = byd_registrations_complete['year'].values.reshape(-1, 1)  # Reshape for sklearn which expects 2D arrays
y_byd = byd_registrations_complete['number'].values

# Fit the linear regression model
model_byd = LinearRegression()
model_byd.fit(X_byd, y_byd)

# Predicting for 2023
year_2023_byd = np.array([[2023]])
predicted_2023_byd = model_byd.predict(year_2023_byd)

# Extending the trend line from the earliest data point to 2023
X_byd_extended = np.linspace(X_byd.min(), year_2023_byd[0], num=100).reshape(-1, 1)  # For a smooth line
y_byd_extended = model_byd.predict(X_byd_extended)

# Plot the results
plt.figure(figsize=(10, 6))
plt.scatter(X_byd, y_byd, color='blue', label='Historical Data')  # Historical data points
plt.plot(X_byd_extended, y_byd_extended, color='red', label='Trend Line')  # Trend line
plt.scatter(year_2023_byd, predicted_2023_byd, color='green', marker='o', label='2023 Prediction')  # Prediction point
plt.title('BYD Annual New Registrations Prediction for 2023')
plt.xlabel('Year')
plt.ylabel('Number of New Registrations')
plt.ylim(bottom=0)  # Start y-axis from 0
plt.legend()
plt.grid(True)
plt.show()

# Display the predicted number of registrations for 2023
predicted_2023_byd

