#!/usr/bin/env python
import argparse
import requests
from datetime import datetime

URL = "https://gridwatch.org.uk/do_download.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/120.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en;q=0.5",
    "Referer": "http://gridwatch.org.uk/download.php",
}
ERROR_MSG = "All your bases are belong to us"
MONTH_NUMS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
DAYS_IN_MONTH = {
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

parser = argparse.ArgumentParser(
    description="evaluate UK wind output for month or year"
)
parser.add_argument(
    "month", help="month in mmm format, or 'all' to process an entire year"
)
parser.add_argument("year", type=int, help="year in YY format")

args = parser.parse_args()
month, year = args.month, args.year

if month == "all":
    start_month = 1
    end_month = datetime.now().month
    end_day = datetime.now().day
else:
    start_month = MONTH_NUMS.index(month)
    end_month = start_month + 1
    end_day = DAYS_IN_MONTH[month]
params = f"none=off&demand=on&frequency=on&coal=on&nuclear=on&ccgt=on&wind=on&pumped=on&hydro=on&biomass=on&oil=on&solar=on&ocgt=on&french_ict=on&dutch_ict=on&irish_ict=on&ew_ict=on&nemo=on&other=on&north_south=on&scotland_england=on&ifa2=on&intelec_ict=on&nsl=on&all=off&starthour=0&startminute=0&startday=1&startmonth={start_month}&startyear=20{year}&endhour=23&endminute=55&endday={end_day}&endmonth={end_month}&endyear=20{year}"
data = {q.split("=")[0]: q.split("=")[1] for q in params.split("&")}

r = requests.post(URL, headers=HEADERS, data=data).content.decode("utf-8")

try:
    assert r != ERROR_MSG
except AssertionError:
    print(
        """
Something went wrong: the endpoint (www.gridwatch.org.uk/download.php) returned a custom error, most likely designed to frustrate scraping.

You may want to consider changing User Agent, and also donating at www.gridwatch.templar.co.uk/donate.html
"""
    )
    exit(1)

with open(f"gridwatch_{month}{year}.csv", "w") as f:
    f.write(r)
