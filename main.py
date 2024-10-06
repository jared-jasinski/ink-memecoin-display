import os
import requests
import csv
import time
import eink
import makeBMP

# Get the API key from environment variable
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

def fetch_price(item_id):
    url = f"https://price.jup.ag/v6/price?ids={item_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('data') and item_id in data['data']:
            return data['data'][item_id]  # Return the specific item data
    else:
        eink(f"Failed to fetch data for {item_id}. Status code: {response.status_code}")
    return None

def fetch_price_24h(token_name):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_name.lower()}&vs_currencies=usd&include_24hr_change=true"
    headers = {
        'Authorization': f'Bearer {COINGECKO_API_KEY}'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data.get(token_name):
            current_price = data[token_name]['usd']
            price_change_percentage = data[token_name]['usd_24h_change']
            price_change_usd = (current_price * price_change_percentage) / 100  # Calculate the USD amount change
            return current_price, price_change_percentage, price_change_usd
    else:
        eink(f"Failed to fetch data for {token_name}. Status code: {response.status_code}")
    return None, None, None

def load_csv(filename):
    tokens = []
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            token_name = row[0]
            token_id = row[1]
            tokens.append((token_name, token_id))  # Store as (token_name, token_id)
    return tokens

def process_token(token_name, item_id):
    # Fetch price from Jupiter API
    jup_data = fetch_price(item_id)
    if jup_data:
        jup_price = jup_data['price']  # Get the price from the returned data

        # Fetch 24-hour price change from CoinGecko API
        current_price, price_change_percentage, price_change_usd = fetch_price_24h(token_name.lower())
        if current_price is not None:
            # Format the price change with proper signs
            price_change_str = f"{price_change_percentage:.2f}%"
            if price_change_percentage < 0:
                price_change_str = f"{price_change_percentage:.2f}%"  # Negative percentage will show '-' by default
            else:
                price_change_str = f"+{price_change_percentage:.2f}%"  # Positive percentage gets a '+' sign

            return f"{token_name}, ${current_price:.6f}, {price_change_str}, ${price_change_usd:.4f}"
        else:
            return f"Could not fetch price change for {token_name} from CoinGecko."
    return f"Failed to fetch price for {token_name} from Jupiter API."

def main():
    tokens = load_csv('data.csv')  # Replace with your CSV file name
    index = 0
    total_tokens = len(tokens)
    delay = 3
    
    while True:
        token_name, item_id = tokens[index]
        result = process_token(token_name, item_id)
        # print(result)
        index = (index + 1) % total_tokens  # Reset to 0 when the end is reached
        eink.show_on_display(makeBMP.create_bmp(result))
        time.sleep(delay)  # Wait for specified delay before fetching the next price

if __name__ == "__main__":
    main()