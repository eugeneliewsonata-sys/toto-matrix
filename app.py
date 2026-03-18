import streamlit as st
import requests
from bs4 import BeautifulSoup
import collections
import random
import re

# 1. INK & PAPER BRANDING (Strict Black & White)
st.set_page_config(page_title="Lucky Number Pro", page_icon="📈", layout="centered")

st.markdown("""
    <style>
    /* Pure White Background */
    .main { background-color: #ffffff; }
    .stApp { background-color: #ffffff; }
    
    /* Ink Black Text */
    h1, h2, h3 { 
        color: #000000 !important; 
        font-family: 'Inter', sans-serif;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    p, span, label { 
        color: #000000 !important; 
        font-family: 'Inter', sans-serif;
    }

    /* Minimalist Black Inputs */
    .stTextInput>div>div>input { 
        border: 1px solid #000000 !important;
        background-color: #ffffff !important;
        border-radius: 4px !important;
        color: #000000 !important;
    }

    /* Solid Black Buttons */
    .stButton>button { 
        width: 100%; 
        border-radius: 4px; 
        height: 3.5em; 
        background-color: #000000; 
        color: #ffffff; 
        font-weight: 600; 
        border: none;
        text-transform: uppercase;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #333333;
        color: #ffffff;
    }

    /* Clean Dividers and Metrics */
    hr { border-top: 1px solid #000000 !important; }
    [data-testid="stMetricValue"] { color: #000000 !important; font-weight: 800 !important; }
    .stMetric { border: 1px solid #eeeeee; padding: 15px; border-radius: 4px; }
    .stInfo { background-color: #f9f9f9; border: 1px solid #000000; color: #000000; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE HISTORICAL VAULT (Your fed data remains here)
VAULT_4D = "80474206710328685044035084831805444041755938586455209168453600187307197177718803120963611044"
VAULT_658 = [
    [18, 19, 29, 30, 36, 54], [2, 16, 20, 33, 34, 49], [8, 16, 22, 33, 53, 56],
    [4, 5, 13, 17, 22, 54], [7, 10, 18, 23, 26, 41], [26, 34, 39, 46, 47, 49],
    [5, 6, 15, 22, 40, 53], [4, 19, 29, 39, 50, 54]
]

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def show_login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("LUCKY NUMBER PRO")
    st.markdown("Matrix Analytics | Secure Member Access")
    
    # Login Section
    password = st.text_input("ACCESS KEY", type="password")
    if st.button("Unlock Engine"):
        if password == "eugene2026":
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("Access Denied.")

    # Minimalist Paywall
    st.divider()
    st.markdown("### PRO MEMBERSHIP")
    st.markdown("**RM 9.90 / MONTH**")
    st.write("Direct integration with 4DMoon live results and historical frequency vault.")
    
    st.link_button("ACTIVATE SUBSCRIPTION", "https://buy.stripe.com/7sY8wPdWN7FdeQkanIcbC00")

if st.session_state['logged_in']:
    st.title("LUCKY NUMBER PRO")
    st.markdown("Status: **Verified VIP Access**")
    
    with st.sidebar:
        if st.button("Log Out"):
            st.session_state['logged_in'] = False
            st.rerun()

    @st.cache_data(ttl=3600)
    def get_live_data():
        try:
            # EXCLUSIVE CONNECTION: 4DMoon
            url = "https://www.4dmoon.com/"
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            # Scrape 4-digit numbers from 4DMoon
            nums = re.findall(r'\b\d{4}\b', BeautifulSoup(r.text, 'html.parser').get_text())
            return "".join(nums[:120])
        except: return ""

    if st.button("GENERATE MASTER ANALYSIS"):
        with st.spinner("Syncing with 4DMoon Database..."):
            live = get_live_data()
            pool = live + VAULT_4D
            counts = collections.Counter(pool)
            hot = [d for d, _ in counts.most_common(4)]
            cold = [d for d, _ in reversed(counts.most_common(3))]

            st.markdown("### 10 Calibrated 4D Lines")
            c = st.columns(2)
            for i in range(10):
                line = random.sample(hot, 3) + random.sample(cold, 1)
                random.shuffle(line)
                with c[i % 2]: 
                    st.metric(label=f"Analysis {i+1}", value="".join(line))

            st.divider()
            st.markdown("### 6 Supreme 6/58 Matrix Lines")
            l_pool = [b for d in VAULT_658 for b in d]
            l_counts = collections.Counter(l_pool)
            l_hot = [b for b, _ in l_counts.most_common(12)]
            
            lc = st.columns(2)
            for i in range(6):
                line = sorted(random.sample(l_hot, 6))
                with lc[i % 2]: 
                    st.info(f"**{' '.join(f'{n:02d}' for n in line)}**")

else:
    show_login_page()

st.divider()
st.caption("© 2026 LUCKY NUMBER ANALYTICS.")
