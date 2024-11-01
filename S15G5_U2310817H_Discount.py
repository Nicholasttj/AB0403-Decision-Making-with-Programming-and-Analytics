#link - https://youtu.be/tgR5Mi7d_W0

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:19:01 2024

@author: Nicholas
"""

import csv

# Create standard value format throughout the program
def format_currency(value):
    return "${:,.2f}".format(value)

# Import data & creating empty dictionary
def discount_csv(filename):
    try:
        data = []
        quarter_list = {'Q1': {'None': 0, 'Low': 0, 'Medium': 0, 'High': 0},
                        'Q2': {'None': 0, 'Low': 0, 'Medium': 0, 'High': 0},
                        'Q3': {'None': 0, 'Low': 0, 'Medium': 0, 'High': 0},
                        'Q4': {'None': 0, 'Low': 0, 'Medium': 0, 'High': 0}}


        total_discounts = {'None': 0, 'Low': 0, 'Medium': 0, 'High': 0}
        with open(filename, "r", newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            for row in reader:
                data.append(row)    


            # Filtering the month and the respective data by their respective quarters
            for row in data:
                if int(row[1]) == 2023:
                    month = row[0].strip()  # Remove leading and trailing whitespaces
                    discount_band = row[5].strip()  # Remove leading and trailing whitespaces
                    if month in ('January', 'February', 'March'):
                        quarter = 'Q1'
                        quarter_list[quarter][discount_band] += float(row[10])
                    elif month in ('April', 'May', 'June'):
                        quarter = 'Q2'
                        quarter_list[quarter][discount_band] += float(row[10])
                    elif month in ('July', 'August', 'September'):
                        quarter = 'Q3'
                        quarter_list[quarter][discount_band] += float(row[10])
                    elif month in ('October', 'November', 'December'):
                        quarter = 'Q4'
                        quarter_list[quarter][discount_band] += float(row[10])


        # Print the table header
        print(" ___________________________________________________________________________________________________________")
        print("|  Discount Bands |    Quarter 1    |    Quarter 2    |    Quarter 3    |    Quarter 4    |      Total      |")
        print("|-----------------|-----------------|-----------------|-----------------|-----------------|-----------------|")


        # Print each row in the table
        for band in total_discounts:
            q1_value = format_currency(quarter_list['Q1'][band])
            q2_value = format_currency(quarter_list['Q2'][band])
            q3_value = format_currency(quarter_list['Q3'][band])
            q4_value = format_currency(quarter_list['Q4'][band])
            total_value = format_currency(sum(quarter_list[q][band] for q in quarter_list))
            print(f"| {band:<15} | {q1_value:<15} | {q2_value:<15} | {q3_value:<15} | {q4_value:<15} | {total_value:<15} |")


        # Print the table footer
        print("|_________________|_________________|_________________|_________________|_________________|_________________|")


        # Defining the total discounts per quarter
        total_discounts_q1 = sum(quarter_list['Q1'].values())
        total_discounts_q2 = sum(quarter_list['Q2'].values())
        total_discounts_q3 = sum(quarter_list['Q3'].values())
        total_discounts_q4 = sum(quarter_list['Q4'].values())
        total_discounts_year = sum(sum(quarter_list[q].values()) for q in quarter_list)


        # Print summary of insights after collating total quarter values
        print("\nSummary of Insights:")
        print("-" * 55)
        print("{:<40} {:<20}".format("Total Discounts for Q1 2023:", format_currency(total_discounts_q1)))
        print("{:<40} {:<20}".format("Total Discounts for Q2 2023:", format_currency(total_discounts_q2)))
        print("{:<40} {:<20}".format("Total Discounts for Q3 2023:", format_currency(total_discounts_q3)))
        print("{:<40} {:<20}".format("Total Discounts for Q4 2023:", format_currency(total_discounts_q4)))
        print("{:<40} {:<20}".format("Total Discounts for the Year 2023:", format_currency(total_discounts_year)))
        print("-" * 55)

        
        def find_quarter_with_highest_discount(quarter_discounts):
            max_discount = 0
            max_quarter = None
            for quarter, discounts in quarter_discounts.items():
                quarter_total = sum(discounts.values())
                if quarter_total > max_discount:
                    max_discount = quarter_total
                    max_quarter = quarter
            return max_quarter

        # Call the function with quarter_list from your main code
        quarter_with_highest_discount = find_quarter_with_highest_discount(quarter_list)
        if quarter_with_highest_discount:
            quarter_label = f"Quarter {quarter_with_highest_discount[1]}  (Q{quarter_with_highest_discount[1]})"
            print("\n-------------------------------------------------------")
            print("{:<40} {:<20}".format("Quarter with Highest Discount:", quarter_label))
            print("-------------------------------------------------------")
        
        def growth_rate(previous_value, current_value):
            return ((current_value - previous_value)/previous_value)*100 if previous_value != 0 else None

        # Calculate growth rates
        Q2_growth = growth_rate(total_discounts_q1, total_discounts_q2)
        Q3_growth = growth_rate(total_discounts_q2, total_discounts_q3)
        Q4_growth = growth_rate(total_discounts_q3, total_discounts_q4)

        # Print growth rates
        # Print growth rates table header
        print(" ___________________________________________________")
        print("|              Quarterly Growth Rates               |")
        print("|___________________________________________________|")
        print("|    Quarter   |          Growth Rate (%)           |")
        print("|--------------|------------------------------------|")

        # Print each row in the table
        print(f"|  Q1 to Q2    |  {Q2_growth:>20.2f}%             |")
        print(f"|  Q2 to Q3    |  {Q3_growth:>20.2f}%             |")
        print(f"|  Q3 to Q4    |  {Q4_growth:>20.2f}%             |")

        # Print the table footer
        print("|______________|____________________________________|")
      
        
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

discount_csv('product_data.csv')
