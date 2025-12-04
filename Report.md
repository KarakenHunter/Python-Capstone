Campus Energy Consumption Analysis – Capstone Project Report

Course: Programming for Problem Solving using Python
Student: Manthan Sharma
Roll No.: 2501410037

1. Introduction

Understanding energy consumption patterns is essential for efficient campus management.
This capstone project focuses on building a complete data-processing system that analyzes electricity usage across multiple campus buildings. The system automates data ingestion, cleans raw CSV files, aggregates consumption at different time scales, visualizes trends, and generates a final summary for decision-making.

The project demonstrates practical applications of Python in handling real-world style datasets using Pandas, NumPy, Matplotlib, and object-oriented programming.

2. Objectives

The primary goals of the project were:

Read and merge multiple building-wise energy datasets automatically

Clean and standardize meter data

Perform daily, weekly, and building-level aggregations

Build an object-oriented model to represent buildings and their readings

Create a dashboard of visual insights

Generate a final written summary and export cleaned datasets

These objectives align with the capstone requirements outlined in the assignment document.

3. Dataset Description

Three sample datasets were created for this project:

Library_Jan.csv

Admin_Jan.csv

Hostel_Jan.csv

Each file contains hourly electricity usage readings for two days, with the following fields:

timestamp (datetime)
kwh (energy used in that hour)
building (building name)


The datasets were placed in a /data folder and automatically detected by the script.

4. Data Ingestion and Cleaning
4.1 Ingestion

The program loops through all CSV files inside the data/ directory.
For each file:

Missing or incorrect rows are skipped

Columns are detected automatically (timestamp, kwh, building)

Metadata is added from filenames when necessary

All files are merged into a single combined DataFrame

4.2 Cleaning

Data issues addressed:

Non-standard column names

Missing timestamps or missing kWh values

Invalid numeric entries

Mixed date formats

After cleaning:

All timestamps were converted to proper datetime objects

kWh values were ensured to be numeric

Rows with missing critical fields were removed

The final cleaned dataset was sorted chronologically

The cleaned dataset was saved as cleaned_energy_data.csv.

5. Aggregation and Analysis
5.1 Daily Aggregation

Daily totals were computed for each building across the two-day period.
This helps identify which days show higher or lower utilization.

5.2 Weekly Aggregation

Weekly totals were generated using Pandas' resampling features.
Since the dataset spans only two days, weekly values reflect that limited period but still satisfy the requirement.

5.3 Building Summary

For each building:

Total kWh consumption

Average hourly usage

Minimum and maximum readings

Peak-hour consumption and timestamp

This summary was exported in building_summary.csv.

6. Object-Oriented Implementation

The OOP section includes three core classes:

MeterReading

Stores a single timestamp + kWh record.

Building

Represents a building and provides methods to:

Add meter readings

Compute total consumption

Generate daily series

Identify peak-hour usage

BuildingManager

Manages multiple buildings, merging data and generating building-wise summaries.

This structure separates concerns logically and reflects real-world modeling.

7. Visualization Dashboard

A three-part dashboard was created using Matplotlib and saved as dashboard.png.

7.1 Daily Consumption Trend

Line chart showing energy usage across hours for each building.
The Admin building shows the highest hourly values, while Hostel sees lighter usage.

7.2 Average Weekly Consumption per Building

Bar chart comparing average weekly consumption across buildings.
Again, the Admin building stands out as the highest consumer.

7.3 Peak Consumption Scatter Plot

Shows maximum single-hour readings for each building.
This helps identify which buildings have sudden high-load events.

8. Key Insights

From the processed data and visualizations:

Admin Building has the highest total energy usage among the three buildings.

Library maintains moderate usage with predictable mid-day peaks.

Hostel shows the lowest consumption overall.

Peak usage tends to occur in the afternoon hours across all buildings.

Daily patterns show clear differences in usage behavior, reflecting real-world functional differences of buildings.

These insights would help campus authorities plan load distribution or scheduling maintenance.

9. Exported Outputs

The program automatically generates:

cleaned_energy_data.csv – cleaned merged dataset

building_summary.csv – summary per building

summary.txt – executive written summary

dashboard.png – visualization dashboard

These files are stored in the output/ directory.

10. Conclusion

This capstone project demonstrates a full-scale data analytics workflow using Python:

Reading from multiple files

Cleaning messy data

Creating time-based aggregations

Using OOP to model domain entities

Generating professional visualizations

Producing structured outputs for reporting

The project highlights how Python can be applied to real-world data monitoring scenarios such as campus utilities, energy management, and operational analysis.

It provides hands-on experience with essential programming concepts, data processing pipelines, and modular code design.
