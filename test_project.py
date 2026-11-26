import pytest
from project import search_price, is_valid_ticker, is_valid_number, stock_value

def test_search_price():
    assert search_price("NVDA") > 0
    assert search_price("APPLE") is None

def test_is_valid_ticker():
    assert is_valid_ticker("GOOGLE") == False
    assert is_valid_ticker("GOOGL") == True
    assert is_valid_ticker("AA50") == False
    assert is_valid_ticker("A") == True
    assert is_valid_ticker("aapl") == False

def test_is_valid_number():
    assert is_valid_number(-10) == False
    assert is_valid_number(0) == False
    assert is_valid_number(1) == True

def test_stock_value():
    assert stock_value(165.05, 5) == 825.25



