#!/usr/bin/env python
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
#from pmdarima import auto_arima
import sys
import requests

days_in_month = {
    "Jan": 31,
    "Feb": 28,
    "Mar": 31,
    "Apr": 30,
    "May": 31,
    "Jun": 30,
    "Jul": 31,
    "Aug": 31,
    "Sep": 30,
    "Oct": 31,
    "Nov": 30,
    "Dec": 31,
}

capacity_by_year = {
        2010: 5,
        2011: 6,
        2012: 9,
        2013: 12,
        2014: 13,
        2015: 15,
        2016: 16,
        2017: 19,
        2018: 21,
        2019: 24
}

parser = argparse.ArgumentParser(description="evaluate UK wind output for month or year")
parser.add_argument("month", help="month in mmm format, or 'all' to process an entire year")
parser.add_argument("year", type=int, help="year in YY format")
args = parser.parse_args()

month, year = args.month, args.year

if month == "all":
    grid = pd.read_csv(f"./gridwatch_20{year}.csv")
else:
    grid = pd.read_csv(f"./gridwatch_{month}{year}.csv")
grid.rename(columns = {" wind": "wind", " solar": "solar"}, inplace = True)
grid["wind"] = grid["wind"].apply(lambda x: x / 1000.0)
grid["solar"] = grid["solar"].apply(lambda x: x / 1000.0)
grid["wind+solar"] = grid["wind"] + grid["solar"]
grid["time"] = pd.to_datetime(grid[" timestamp"],  format=" %Y-%m-%d %H:%M:%S")
grid = grid.drop(" timestamp", axis=1)
# grid = grid.set_index("time")
# grid = grid.resample("h").mean()
grid = grid.resample("h", on="time").mean()

print(f"total = {grid['wind'].sum() / 1000.} TWh , mean = {grid['wind'].mean()} GW, capacity = {grid['wind'].mean() / 24}")#capacity_by_year.get(2000+int(year), 2019)} %")
x = np.linspace(0, 20., 100)
kde = gaussian_kde(grid["wind"])
if month == "all":
    y = [24 * 365 * i for i in kde(x)]
else:
    y = [24 * days_in_month[month] * i for i in kde(x)]
plt.plot(x, y)
plt.xlabel("Power (GW)")
plt.ylabel("hours")
plt.savefig(f"wind_power_{month}22.png")
plt.show()
low_hours = grid[grid["wind"] < 1]["wind"]
print(f"low hours count = {low_hours.count().item()}")

# model = auto_arima(grid["wind+solar"], seasonal=True, m=12)
# forecast = model.predict(grid.shape[0])
# x = np.arange(0, forecast.shape[0])
# plt.plot(x, forecast)
# plt.show()
