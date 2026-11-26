# Investment Portfolio

#### Video Demo:  <https://youtu.be/cjCBwqkeRaI>

#### Description:
This is a program that tracks the current market value of your stock portfolio, especially for people who have several brokerage accounts!

You can look up the latest stocks prices, calculate your total assets, create a pie chart, and save the result as a CSV file.

## How To Use
1. Install the required packages listed in [requirements.txt](requirements.txt)

    ```
    pip install -r requirements.txt
    ```

2. Sign up for a free API key at [Twelve data](https://twelvedata.com/)

3. Set your API key as an environment variable named `TWELVE_DATA_API_KEY`
- GitHub Codespaces : Add a new secret in your codespace.
Follow the [GitHub Codespaces secrets guide](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces) to add your key.

- Mac or Linux : Run the following command in your terminal:
    ```
    export TWELVE_DATA_API_KEY=your_api_key_here
    ```

4. There are two modes in this program:

- (1) If you already have a csv file, this program can read the data in your file.
    This file must use this format:
    ```
    Stock,Shares
    AAPL,10
    MSFT,5
    NVDA,8
    ```

    Run the following command in your terminal:

    ```
    python project.py yourfilename.csv
    ```

- (2) You can enter each stock and its number of shares manually.

    ```
    python project.py
    ```
    Enter a stock symbol and the number of shares when prompted. When you're done, press Ctrl+D to stop entering stocks.


5. The program will print two tables and save a pie chart as `pie_chart.png`

6. You can decide whether to save the results as a csv file `stockrecord.csv`.


## Code Overview

### project.py

#### Getting the holdings through a CSV file or user input.

`main()`: Decides the mode user select by the length of sys.argv. Prints the `portfolio` and `sum_list` as two tables. Calls `chart()` and `save_csv()`

`csv_reader()`: Takes a CSV file name from `main()` and reads each row of the file into a list called `portfolio`. It uses `is_valid_ticker()` and `is_valid_number()` to check that each stock symbol and number of shares are valid. It then calls `search_price()` to look up the latest price for each stock. If a price cannot be found, the program exits. Otherwise, the stock's market value is added to the total. Finally, it returns `portfolio` and `sum_list` to `main()`.

`create_new_record()`: Calls `get_stock()` to get the stock symbol and calls `get_shares()` to get the number of shares. It then calls `search_price()` to look up the latest price for each stock. If a price cannot be found, the user is asked to enter the stock again. Otherwise, the stock's market value is added to the total. Finally, it returns `portfolio` and `sum_list` to `main()`.

#### Validating input

`get_stock()`: Prompts the user for a stock symbol. If `is_valid_ticker()` returns `True`, it returns the stock symbol. Otherwise, it asks again.

`is_valid_ticker()`: Returns True if the symbol has 1 to 5 uppercase letters.

`get_shares()`: Prompts the user for the number of shares. If `is_valid_number()` returns `True`, it returns the number. Otherwise, it asks again.

`is_valid_number()`: Returns `True` if the number of shares is greater than 0, and `False` otherwise.

#### Fetching prices

`search_price()`: Requests the latest price from the Twelve Data API. If the price cannot be found, it asks for a valid symbol and returns None.



#### Calculating

`stock_value()`: Multiples the stock price by the number of shares.

`total_list()`: Creates `sum_list`, which stores the total asset value and date.

#### Output

`save_csv()`: Asks whether the user wants to save the result as a CSV file named `stockrecord.csv`.

`chart()`: Draws a pie chart of the portfolio and saves it as `pie_chart.png`.


### test_project.py

This file contains unit tests for four functions in `project.py`.

`test_search_price()`: Checks that a valid stock symbol such as `NVDA` returns a price greater than 0, and that a symbol in a valid format but with no matching stock, such as `APPLE`, returns `None`. This test needs an internet connection and a valid API key.

`test_is_valid_ticker()`: Checks that symbols with 1 to 5 uppercase letters, such as `A` and `GOOGL`, return `True`. It also checks that invalid symbols return `False`, including a symbol that is too long (`GOOGLE`), one that contains numbers (`AA50`), and one in lowercase (`aapl`).

`test_is_valid_number()`: Checks that negative numbers and 0 return `False`, and that a positive number such as 1 returns `True`.

`test_stock_value()`: Checks that `stock_value()` returns the correct market value.

I did not write tests for `get_stock()`, `get_shares()`, `save_csv()`, and `chart()` because they depend on user input or create files.

Run the tests with:

````
pytest test_project.py
````

### requirements.txt

You should install requests, matplotlib, tabulate to make this program work!


## Design Choices

**1. API choice**

I use Twelve Data as my source of price data. Its free plan allows 800 requests per day.

**2. Instant price lookup**

In manual mode, the program looks up the price as soon as the user enters a stock symbol, so the user can fix a wrong symbol right away. Another option was to collect all the stocks first and look up the prices at the end, but then the user would only find out about a wrong symbol after entering everything. The trade-off is that the input step depends on the internet connection.

**3. Separate validation functions**

`is_valid_ticker()` and `is_valid_number()` check for invalid input, so they can be tested on their own without user input. Functions that call `input()` are hard to test with pytest, so I kept the validation rules out of `get_stock()` and `get_shares()`.

**4. Table format**

I use the `fancy_grid` format instead of `pretty`. While testing, I found that the `pretty` format ignores `floatfmt`, so it cannot display thousands separators or two decimal places.
