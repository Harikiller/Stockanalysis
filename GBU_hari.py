import requests
from bs4 import BeautifulSoup
import textwrap
import streamlit as st

st.set_page_config(page_title="Hari's GBU Analysis", layout="wide")

def get_screener_data(stock_code):
    url = f'https://www.screener.in/company/{stock_code}/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    data = {}

    try:
        # Extract financial ratios
        ratios = soup.find('ul', {'class': 'ranges-table'}).find_all('li')
        for ratio in ratios:
            key = ratio.find('span', {'class': 'name'}).text.strip()
            value = ratio.find('span', {'class': 'value'}).text.strip()
            data[key] = value

        # Extract description
        about_section = soup.find("section", {"id": "about"})
        if about_section:
            desc = about_section.get_text(strip=True).replace("About", "")
            data["Business Description"] = textwrap.fill(desc, width=80)

    except Exception as e:
        st.error(f"Error while fetching data: {e}")

    return data

def show_gbu_report(stock_code, data):
    st.title(f"Hari's GBU Analysis: {stock_code.upper()}")

    st.subheader("1. Company Overview")
    st.write(f"**Business Description:** {data.get('Business Description', 'N/A')}")

    st.subheader("2. Fundamentals")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**ROE:** {data.get('Return on equity', 'N/A')}")
        st.write(f"**ROCE:** {data.get('Return on capital employed', 'N/A')}")
        st.write(f"**Net Margin:** {data.get('Net profit margin', 'N/A')}")
        st.write(f"**EPS:** {data.get('EPS', 'N/A')}")

    st.subheader("3. Financial Health")
    with col2:
        st.write(f"**Debt to Equity Ratio:** {data.get('Debt to equity', 'N/A')}")
        st.write(f"**Current Ratio:** {data.get('Current ratio', 'N/A')}")

    st.subheader("4. Valuation")
    st.write(f"**P/E Ratio:** {data.get('Price to earnings', 'N/A')}")
    st.write(f"**P/B Ratio:** {data.get('Price to book value', 'N/A')}")

    st.info("Additional sections like Moat, Risks, and Management must be filled manually.")

# Streamlit App Entry
st.sidebar.title("Hari's GBU Analyzer")
stock_code = st.sidebar.text_input("Enter Screener stock code", "TATAELXSI").strip().upper()
if st.sidebar.button("Analyze"):
    with st.spinner("Fetching data from Screener.in..."):
        stock_data = get_screener_data(stock_code)
    show_gbu_report(stock_code, stock_data)
