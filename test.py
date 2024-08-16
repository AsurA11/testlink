#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import streamlit as st

def fetch_announcements(ticker):
    url = f"https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false"
    response = requests.get(url)
    
    # Check for non-200 status codes
    if response.status_code != 200:
        st.error(f"Error: Received status code {response.status_code} for ticker {ticker}")
        return []
    
    try:
        # Print the raw response for debugging
        st.write(response.text)
        return response.json()
    except requests.exceptions.JSONDecodeError:
        st.error(f"Error: Unable to parse JSON response for ticker {ticker}")
        return []

def process_announcements(data):
    if not data:
        return pd.DataFrame(columns=["Title", "Date", "URL"])
    announcements = [
        {
            "Title": item["header"],
            "Date": item["time"],
            "URL": f"https://www.asx.com.au/asxpdf/{item['id']}/{item['document']}.pdf"
        }
        for item in data
    ]
    return pd.DataFrame(announcements)

def identify_trading_halt(df):
    return df[df["Title"].str.contains("Trading Halt", case=False)]

def main():
    st.title("ASX Company Announcements")
    tickers = ["AEE", "REZ", "1AE", "1MC", "NRZ"]

    # Select Ticker Symbol
    selected_ticker = st.selectbox("Select Ticker", tickers)

    # Fetch and Display Announcements
    announcements = fetch_announcements(selected_ticker)
    df = process_announcements(announcements)

    st.subheader(f"Recent Announcements for {selected_ticker}")
    st.dataframe(df)

    # Check for Trading Halt
    trading_halt_df = identify_trading_halt(df)
    if not trading_halt_df.empty:
        st.warning(f"Trading Halt found for {selected_ticker}!")
        st.dataframe(trading_halt_df)
    else:
        st.success(f"No Trading Halt found for {selected_ticker}.")

    # Option to View All Announcements Across Tickers
    st.subheader("View All Announcements Across Tickers")
    all_announcements = pd.DataFrame()
    for ticker in tickers:
        announcements = fetch_announcements(ticker)
        df = process_announcements(announcements)
        df["Ticker"] = ticker
        all_announcements = pd.concat([all_announcements, df])

    st.dataframe(all_announcements)
    trading_halt_all = identify_trading_halt(all_announcements)
    if not trading_halt_all.empty:
        st.warning("Trading Halt found in the following tickers:")
        st.dataframe(trading_halt_all)

if __name__ == "__main__":
    main()


# In[ ]:




