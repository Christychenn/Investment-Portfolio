import requests
import sys
import os
import re
import csv
import matplotlib.pyplot as plt
from tabulate import tabulate
from datetime import date


def main():
    if len(sys.argv) == 1:
       portfolio, sum_list = create_new_record()

    elif len(sys.argv) == 2 and sys.argv[1].endswith(".csv") == True:
       portfolio, sum_list = csv_reader(sys.argv[1])

    else:
        sys.exit("Provide at most one CSV file")

    print()
    print(tabulate(portfolio, headers = "keys", tablefmt = "fancy_grid",  floatfmt=(",.2f")))
    print(tabulate(sum_list, headers = "keys", tablefmt = "fancy_grid", floatfmt=(",.2f")))
    chart(portfolio)
    save_csv(portfolio, sum_list)


def create_new_record():
    portfolio = []
    total = 0
    while True:
        try:
            stock = get_stock()
            shares = get_shares()
            price = search_price(stock)
            if price is None:
                continue
            else:
                market_value  = stock_value(price, shares)
                portfolio.append({"Stock": stock, "Shares" : shares, "Market Value" : market_value })
                total += market_value

        except EOFError:
            sum_list = total_list(total)
            return portfolio, sum_list

def  csv_reader(file):
    portfolio = []
    total = 0
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            portfolio.append(row)
        for i in portfolio:
            if is_valid_ticker(i["Stock"]) == True and is_valid_number(int(i["Shares"])) == True:
                new_price = search_price(i["Stock"])
                if new_price is None:
                    sys.exit()
                else:
                    new_mv = stock_value(new_price, int(i["Shares"]))
                    i["Market Value"] = new_mv
                    total += new_mv
            else:
                sys.exit("Please check your csv file!")
        sum_list = total_list(total)
        return portfolio, sum_list

def search_price(p):
    try:
        params ={
            "symbol": p,
            "apikey": os.getenv("TWELVE_DATA_API_KEY"),
        }
        api = requests.get("https://api.twelvedata.com/price", params = params)

    except requests.RequestException:
        sys.exit("Failed to connect to API!")
    price = api.json()
    if "price" in price:
        latest_price = round(float(price['price']), 2)
        return latest_price
    else:
        print("Insert the valid symbol!!")
        return None


def get_stock():
    while True:
        stock = input("Stock: ").upper().strip()
        if is_valid_ticker(stock):
            return stock
        else:
            print("Please Input 1-5 letters!!")


def is_valid_ticker(stock):
    ticker = r"^[A-Z]{1,5}$"
    if re.search(ticker, stock) is None:
        return False
    else:
        return True

def get_shares():
    while True:
        try:
            shares = int(input("Shares: "))
            if is_valid_number(shares) :
                return shares
            else:
                print("Please Input Positive Numbers!")
        except ValueError:
            print("Please Input Positive Numbers!")
            continue


def is_valid_number(shares):
    if shares > 0:
        return True
    else:
        return False



def total_list(t):
    d = date.today().strftime("%Y/%m/%d")
    total_list = []
    total_list.append({"Total Asset" : t , "Date": d})
    return total_list

def stock_value(p, n):
    return round(float(p * n), 2)

def save_csv(portfolio, sum_list):
    ask = input("Saved as csv?(Y/N) ").upper().strip()
    if ask == "YES" or ask == "Y":
        with open("stockrecord.csv", "w", newline="") as f:
                writer1 = csv.DictWriter(f, fieldnames=["Stock", "Shares", "Market Value"])
                writer1.writeheader()
                writer1.writerows([record for record in portfolio])
                writer2 = csv.DictWriter(f, fieldnames=["Total Asset", "Date"])
                writer2.writeheader()
                writer2.writerow(sum_list[0])


def chart(portfolio):
    stock_list = [stock["Stock"] for stock in portfolio]
    value_list = [value["Market Value"] for value in portfolio]
    plt.pie(
    value_list,
    labels=stock_list,
    autopct="%1.1f%%",
    startangle=90,
    counterclock=False,
)

    plt.axis("equal")
    plt.title("Investment Portfolio")
    plt.savefig("pie_chart.png", dpi=300, bbox_inches="tight")

if __name__ == "__main__":
    main()
