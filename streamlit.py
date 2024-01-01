import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import requests
import os
import json
import datetime
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()

def create_price_plots(car_details):
    st.title('These are plots for :blue[Distribution of car prices]')
    price = []
    brand = []
    model = []
    manufacturing_year = []
    for car_detail in car_details:
        # Extract the price as a string and remove the currency symbol and commas
        price_str = car_detail['general']['price'].replace('RM ', '').replace(',', '')

        try:
            price_value = float(price_str)
            price.append(price_value)
            brand.append(car_detail['general']['brand'])
            model.append(car_detail['general']['model'])
            # manufacturing_year.append(car_detail['general']['mfg_year'])
            for item in car_detail['general']['mfg_year'].split(' '):
                try:
                    manufacturing_year.append(int(item))
                except Exception as _:
                    continue
        except ValueError:
            continue

    # Histogram (Distribution of Car Prices)
    fig, ax = plt.subplots(figsize=(10, 5))
    counts, bins, patches = ax.hist(price, bins='auto')  # Use the calculated bin edges
    ax.set_xticks(bins)  # Set x-ticks at bin edges
    ax.set_xticklabels(['{:.2f}'.format(b) for b in bins], rotation=90, ha='right')
    ax.set_xlabel('Price (RM)')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Car Prices')
    st.pyplot(fig)

    # Box Plot (Price Distribution by Brand)
    fig, ax = plt.subplots(figsize=(10, 5))
    brands_unique = list(set(brand))
    prices_by_brand = {b:[] for b in brands_unique}
    
    for i, b in enumerate(brand):
        prices_by_brand[b].append(price[i])
        
    prices_list = [prices_by_brand[b] for b in brands_unique]
    print(prices_list)
    ax.boxplot(prices_list)
    ax.set_xticklabels(brands_unique, rotation=90, ha='right')
    ax.set_xlabel('Brand')
    ax.set_ylabel('Price (RM)')
    ax.set_title('Price Distribution by Brand')
    st.pyplot(fig)

    # Scatter Plot (Price vs. Manufacturing Year)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(manufacturing_year, price)
    ax.set_xticks(sorted(set(manufacturing_year)))
    ax.set_xticklabels(sorted(set(manufacturing_year)), rotation=90, ha='right')
    ax.set_xlabel('Manufacturing Year')
    ax.set_ylabel('Price (RM)')
    ax.set_title('Relationship between Manufacturing Year and Price')
    st.pyplot(fig)

    # Bar Chart (Average Price by Brand)
    average_prices_by_brand = [np.mean(prices_by_brand[b]) for b in brands_unique]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(brands_unique, average_prices_by_brand)
    ax.set_xticklabels(brands_unique, rotation=90, ha='right')
    ax.set_xlabel('Brand')
    ax.set_ylabel('Average Price (RM)')
    ax.set_title('Average Price by Brand')
    st.pyplot(fig)
    
    # Line Graph (Trend of Prices Over Time)
    years_unique = sorted(set(manufacturing_year))
    average_price_by_year = [np.mean([price[i] for i in range(len(price)) if manufacturing_year[i] == year]) for year in years_unique]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(years_unique, average_price_by_year)
    ax.set_xticks(sorted(set(manufacturing_year)))
    ax.set_xticklabels(years_unique, rotation=90, ha='right')
    ax.set_xlabel('Manufacturing Year')
    ax.set_ylabel('Average Price (RM)')
    ax.set_title('Trend of Prices Over Time')
    st.pyplot(fig)

def create_age_mileage_plots(car_details):
    st.title('These are plots for :blue[Relationship between car age and mileage]')

    car_age = []
    car_mileage = []
    for car_detail in car_details:
        try:
            mfg_year = int(car_detail['general']['mfg_year'])
            car_mil = car_detail['general']['mileage'].replace(' ', '')
            mil_range = []
            for item in car_mil.split('-'):
                mil_range.append(int(item))
            car_mileage.append(mil_range)
            car_age.append(datetime.date.today().year - mfg_year)

        except ValueError:
            continue
    
    # Process the mileage to get a single representative value (average of the range)
    mileage_values = [np.mean(list(map(int, m))) for m in car_mileage]

    # Group mileage values by car age
    mileage_by_age = defaultdict(list)
    for age, mil in zip(car_age, mileage_values):
        mileage_by_age[age].append(mil)

    # Calculate average mileage for each car age
    average_mileage_by_age = {age: np.mean(mileages) for age, mileages in mileage_by_age.items()}

    # Sort the car ages to plot them in order
    sorted_ages = sorted(average_mileage_by_age.keys())
    sorted_average_mileage = [average_mileage_by_age[age] for age in sorted_ages]

    # Create the scatter plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(sorted_ages, sorted_average_mileage)
    # Fit a line to the data
    fit = np.polyfit(sorted_ages, sorted_average_mileage, 10)
    fit_fn = np.poly1d(fit)
    ax.plot(sorted(sorted_ages), fit_fn(sorted(sorted_ages)), color='red', label='Trend Line')

    ax.set_xticks(sorted_ages)
    ax.set_xticklabels(sorted_ages, rotation=90)
    ax.set_xlabel('Car Age (years)')
    ax.set_ylabel('Average Mileage')
    ax.set_title('Relationship between Car Age and Average Mileage')
    st.pyplot(fig)


session = requests.Session()
session.headers.update({'X-API-KEY': os.getenv("API_KEY")})
response = session.get('http://127.0.0.1:8000/car/')
car_details = json.loads(response.content)
create_price_plots(car_details)
create_age_mileage_plots(car_details)