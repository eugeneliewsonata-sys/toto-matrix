import streamlit as st
import requests
from bs4 import BeautifulSoup
import collections
import random
import re

# 1. COMMERCIAL BRANDING & THEME
st.set_page_config(page_title="Lucky Matrix Pro", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #00ff41; color: black; font-weight: bold; border: none; }
    .stTextInput>div>div>input { border-radius: 10px; }
    .subscription-box { border: 1px solid #00ff41; padding: 20px; border-radius: 15px; background-color: #1a1c24; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE HISTORICAL DATA VAULT (Eugene's Fed Data)
VAULT_4D = "80474206710328685044035084831805444041755938586455209168453600187307197177718803120963611044"
VAULT_658 = [
    [18, 19, 29, 30, 36, 54], [2, 16, 20, 33, 34, 49], [8, 16, 22, 33, 53, 56],
    [4, 5, 13, 17, 22, 54], [7, 10, 18, 23, 26, 41], [26, 34, 39, 46, 47, 49],
    [5, 6, 15, 22, 40, 53], [4, 19, 29, 39, 50, 54]
]

# 3. LOGIN & PAYMENT GATEWAY
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def show_login_page():
    st.title("💎 Lucky Matrix Pro")
    st.subheader("JH Creative Enterprise | Intelligence Portal")
    
    # Login Section
    with st.container():
        st.write("### Member Login")
        # ACCESS KEY IS: eugene2026
        password = st.text_input("Enter Access Key", type="password")
        if st.button("Unlock Pro Engine"):
            if password == "eugene2026":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Access Key Invalid. Please subscribe below.")

    st.divider()

    # Subscription Section (Commercial Feature)
    st.markdown("""
        <div class="subscription-box">
            <h3>🚀 No Access? Get Pro Today</h3>
            <p>Unlock the High-Frequency Matrix & Live Data Scraper.</p>
            <p><b>RM 19.00 / Month</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    # YOUR ACTUAL STRIPE LINK INTEGRATED HERE
    st.link_button("💳 SUBSCRIBE VIA GRABPAY / TNG / CARD", "https://buy.stripe.com/7sY8wPdWN7FdeQkanIcbC00") 
    st.caption("Transactions secured via JH Creative Enterprise & Stripe")

# 4. ENGINE CORE (Runs after login)
if st.session_state['logged_in']:
    st.title("🍀 Lucky Matrix Pro")
    st.write(f"Logged in as: **JH Creative Admin**")
    
    with st.sidebar:
        st.header("Admin Controls")
        if st.button("Log Out"):
            st.session_state['logged_in'] = False
            st.rerun()

    @st.cache_data(ttl=3600)
    def get_live_data():
        try:
            url = "https://check4d.com/"
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            nums = re.findall(r'\b\d{4}\b', BeautifulSoup(r.text, 'html.parser').get_text())
            return "".join(nums[:100])
        except: return ""

    if st.button("🚀 RUN FREQUENCY ANALYSIS"):
        with st.spinner("Analyzing Vault + Live Feed..."):
            live = get_live_data()
            pool = live + VAULT_4D
            counts = collections.Counter(pool)
            hot = [d for d, _ in counts.most_common(4)]
            cold = [d for d, _ in reversed(counts.most_common(3))]

            st.success("Analysis Complete.")
            
            st.markdown("### 🎫 Premium 4D i-Perms")
            c = st.columns(3)
            for i in range(6):
                line = random.sample(hot, 3) + random.sample(cold, 1)
                random.shuffle(line)
                with c[i % 3]: st.info(f"**#{i+1}**\n\n# **{''.join(line)}**")

            st.divider()
            st.markdown("### 🔴 Supreme 6/58 Master Lines")
            l_pool = [b for d in VAULT_658 for b in d]
            l_counts = collections.Counter(l_pool)
            l_hot = [b for b, _ in l_counts.most_common(12)]
            
            lc = st.columns(2)
            for i in range(4):
                line = sorted(random.sample(l_hot, 6))
                with lc[i % 2]: st.success(f"**Line {i+1}**\n\n**{' '.join(f'{n:02d}' for n in line)}**")

else:
    show_login_page()

st.divider()
st.caption("© 2026 JH Creative Enterprise. All Rights Reserved.")
