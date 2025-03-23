import requests
import csv
from datetime import datetime, timedelta

# Define the start and end dates for the previous year
end_date = datetime.now().replace(year=datetime.now().year - 1, month=12, day=31)
start_date = end_date.replace(year=end_date.year - 1)

# Define the list of dates to fetch
date_list = [(start_date + timedelta(days=x)).strftime('%Y-%m-%d') for x in range((end_date - start_date).days + 1)]
coin_pair = 'BTC-USD'
# Prepare CSV file
with open('btc_historical_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["Date", "Amount", "Base", "Currency"])
    
    for date in date_list:
        # Make API request for each date
        response = requests.get(f'https://api.coinbase.com/v2/prices/{coin_pair}/spot?date={date}')
        data = response.json()

        # Extract necessary information
        amount = data['data']['amount']
        writer.writerow([date, amount, 'BTC', 'USD'])

print("CSV file has been created successfully.")