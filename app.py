import streamlit as st
import requests
from bs4 import BeautifulSoup
import collections
import random
import re

# 1. Premium App Branding & Style
st.set_page_config(page_title="Lucky Matrix Pro", page_icon="💎", layout="centered")

# Custom CSS to make it look like a "Commercial App"
# FIXED: changed unsafe_content_html to unsafe_allow_html
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #00ff41; color: black; font-weight: bold; }
    .stTextInput>div>div>input { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE GATEKEEPER (Login Logic)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def check_login():
    if st.session_state['logged_in']:
        return True
    
    st.title("💎 Lucky Matrix: Pro Access")
    st.write("Welcome, Eugene. Please enter your JH Creative credentials to unlock the engine.")
    
    # YOUR PASSWORD IS: eugene2026
    password = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock Engine"):
        if password == "eugene2026": 
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Invalid Access Key. Please contact administrator.")
    return False

# 3. THE ANALYTICS ENGINE (Only runs if logged in)
if check_login():
    st.title("🍀 Lucky Matrix Pro")
    st.subheader("JH Creative Enterprise | Frequency Engine")
    
    with st.sidebar:
        st.write(f"**Status:** Premium Member")
        if st.button("Log Out"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.divider()

    @st.cache_data(ttl=3600)
    def scrape_live_results():
        # Scrapes current board data for frequency analysis
        url = "https://check4d.com/" 
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            raw_text = soup.get_text()
            found_numbers = re.findall(r'\b\d{4}\b', raw_text)
            return "".join(found_numbers[:100]) if found_numbers else None
        except:
            return None

    if st.button("🚀 GENERATE MASTER i-PERMS"):
        with st.spinner("Analyzing live frequency shifts..."):
            live_data = scrape_live_results()
            if live_data:
                digit_counts = collections.Counter(live_data)
                hot_digits = [digit for digit, _ in digit_counts.most_common(4)]
                cold_digits = [digit for digit, _ in reversed(digit_counts.most_common(3))]
                
                st.success("Matrix Calibrated for Today's Draw.")
                
                # Show the Lucky 4D tickets in a nice grid
                cols = st.columns(2)
                for i in range(6):
                    line = random.sample(hot_digits, 3) + random.sample(cold_digits, 1)
                    random.shuffle(line)
                    with cols[i % 2]:
                        st.info(f"**Ticket {i+1}**\n\n# **{''.join(line)}**")
            else:
                st.error("Data feed interrupted. Check server status.")

    st.divider()
    st.caption("© 2026 JH Creative Enterprise. Built for high-frequency analysis.")
