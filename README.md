Campus Energy-Use Dashboard

Capstone Project – Programming for Problem Solving using Python

Author: Manthan Sharma

Roll No.: 2501410037

1. Project Overview

This capstone project focuses on analyzing electricity consumption across multiple campus buildings. The goal is to build a complete end-to-end pipeline that reads raw meter data, cleans and merges it, performs time-based aggregations, uses OOP to structure the system, generates visual insights, and finally exports a summary for administrative use.

The final output includes:

A cleaned combined dataset
Building-wise summary statistics
Daily and weekly consumption trends
A multi-chart dashboard (PNG)
A short written executive summary (TXT)

This assignment demonstrates practical skills in data ingestion, preprocessing, time-series analysis, visualization, and Python OOP.

3. Dataset Description

The dataset consists of hourly energy consumption records for three campus buildings:

Library
Admin
Hostel

Each CSV file contains:
timestamp, kwh, building

Where:
timestamp = date & hour of the reading
kwh = energy consumption for that hour
building = building name

These files are placed in the /data folder and automatically detected by the script.

4. Features Implemented
4.1 Data Ingestion & Validation

Automatically loops through all CSV files in /data

Handles missing or invalid rows

Auto-detects column names (timestamp, kwh, building)

Adds metadata (building name) when needed

Merges all buildings into one master DataFrame

4.2 Data Cleaning

Removes corrupt entries
Converts timestamp to datetime format
Ensures kWh values are numeric
Sorts data chronologically
Standardizes column names

4.3 Aggregation Logic

Using Pandas time-series functions:
Daily totals (per building)
Weekly totals (per building)

Building summary:
total kWh
mean consumption
min/max consumption
peak-hour usage

These results are used for the dashboard and report.

4.4 Object-Oriented Structure

Three core classes:

MeterReading

Represents a single meter record (timestamp + kWh).

Building

Stores all readings for a building and can:
add readings
compute totals
compute daily aggregations
detect peak hour
BuildingManager
Manages multiple buildings together.

This satisfies the capstone OOP requirement and keeps code organized.

4.5 Visualization Dashboard

Generated using Matplotlib and saved as dashboard.png.

The dashboard includes:

Daily consumption trend (line chart for each building)
Average weekly usage per building (bar chart)
Peak consumption per building (scatter plot)
These three charts appear in a single figure.

4.6 Exported Files

The script saves:

cleaned_energy_data.csv – combined processed dataset
building_summary.csv – aggregated stats per building
summary.txt – short executive summary including:

total campus consumption
highest-consuming building
peak load time
notes on trends
