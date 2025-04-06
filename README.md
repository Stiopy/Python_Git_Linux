🛢️ Data-Scraping-Dashboard-Project :
- WTI Oil Price Scraper & Dashboard.
- This project continuously scrapes live WTI crude oil prices from a public website using a Bash script, and displays the historical data in a beautiful, interactive Python Dash dashboard.

🚀 Project Overview :

⏱️ Live Scraping :
- A Bash script scrapes WTI price data every 5 minutes and appends it to a CSV file (scraping_data.csv).

💻 Bash-only Scraper :
- Fully built using native Unix tools like curl, grep, sed, and awk/regex. No Python or external libraries used for scraping.

📊 Real-Time Dashboard :

A Python Dash app visualizes:
- A time-series graph of price evolution.
- A table with the 10 most recent price records.
- A daily report summary auto-updated after 8 PM.

🧾 Daily Financial Summary :

- During the day, the dashboard generates key metrics :
✅ Daily opening and closing prices
📈 Highest and 📉 lowest prices
📐 Mean price of the day
📊 Daily return (% change)

👨‍💻 Authors
ARSLAN Arda & ARCHAMBAULT Stepane IF1
