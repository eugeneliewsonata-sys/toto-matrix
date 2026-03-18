import streamlit as st
import requests
from bs4 import BeautifulSoup
import collections
import random
import re

# 1. MINIMALIST "QUIET LUXURY" BRANDING
st.set_page_config(page_title="Lucky Number Pro", page_icon="✨", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0a0a0a; }
    .stApp { background-color: #0a0a0a; }
    h1, h2, h3 { color: #C0A080 !important; font-family: 'Inter', sans-serif; font-weight: 300 !important; letter-spacing: 1px; }
    p, span, label { color: #888888 !important; font-family: 'Inter', sans-serif; }
    .stTextInput>div>div>input { border: 0px !important; border-bottom: 1px solid #333333 !important; background-color: transparent !important; color: #C0A080 !important; }
    .stButton>button { width: 100%; border-radius: 4px; height: 3em; background-color: transparent; color: #C0A080; border: 1px solid #C0A080; letter-spacing: 2px; text-transform: uppercase; }
    .stButton>button:hover { background-color: #C0A080; color: #000000; }
    .sub-card { border-top: 1px solid #1a1a1a; margin-top: 40px; padding-top: 30px; text-align: center; }
    [data-testid="stMetricValue"] { color: #C0A080 !important; font-size: 1.8rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE HISTORICAL VAULT (Verified & Updated)
VAULT_4D = "80474206710328685044035084831805444041755938586455209168453600187307197177718803120963611044"
VAULT_658 = [
    [18, 19, 29, 30, 36, 54], [2, 16, 20, 33, 34, 49], [8, 16, 22, 33, 53, 56],
    [4, 5, 13, 17, 22, 54], [7, 10, 18, 23, 26, 41], [26, 34, 39, 46, 47, 49],
    [5, 6, 15, 22, 40, 53], [4, 19, 29, 39, 50, 54]
]

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def show_login_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("LUCKY NUMBER PRO")
    st.markdown("##### Matrix Analytics | Secure Access")
    password = st.text_input("ACCESS KEY", type="password", placeholder="Enter key...")
    if st.button("Unlock"):
        if password == "eugene2026":
            st.session_state['logged_in'] = True
            st.rerun()
        else: st.error("Invalid Key")

    st.markdown(f"""
        <div class="sub-card">
            <p style="font-size: 0.8em; letter-spacing: 1.5px; margin-bottom: 5px;">PRO MEMBERSHIP</p>
            <h2 style="margin: 0; color: #C0A080;">RM 9.90 / MO</h2>
            <p style="font-size: 0.8em; color: #555555; margin-top: 10px;">
                LIVE DATA ANALYTICS • HISTORICAL VAULT • PROBABILITY ENGINE
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.link_button("ACTIVATE SUBSCRIPTION", "https://buy.stripe.com/7sY8wPdWN7FdeQkanIcbC00")

if st.session_state['logged_in']:
    st.title("LUCKY NUMBER PRO")
    st.markdown("Welcome, VIP Member.")
    
    with st.sidebar:
        if st.button("Logout"):
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

    if st.button("RUN FREQUENCY ANALYSIS"):
        with st.spinner("Calibrating..."):
            live = get_live_data()
            pool = live + VAULT_4D
            counts = collections.Counter(pool)
            hot = [d for d, _ in counts.most_common(4)]
            cold = [d for d, _ in reversed(counts.most_common(3))]

            st.markdown("### Calibrated 4D Lines")
            c = st.columns(3)
            for i in range(6):
                line = random.sample(hot, 3) + random.sample(cold, 1)
                random.shuffle(line)
                with c[i % 3]: st.metric(label=f"Analysis {i+1}", value="".join(line))

            st.markdown("<br>### Supreme 6/58 Matrix", unsafe_allow_html=True)
            l_pool = [b for d in VAULT_658 for b in d]
            l_counts = collections.Counter(l_pool)
            l_hot = [b for b, _ in l_counts.most_common(12)]
            
            lc = st.columns(2)
            for i in range(4):
                line = sorted(random.sample(l_hot, 6))
                with lc[i % 2]: st.write(f"**{' '.join(f'{n:02d}' for n in line)}**")
else:
    show_login_page()

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 LUCKY NUMBER ANALYTICS.")
