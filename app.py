import streamlit as st
import requests
from bs4 import BeautifulSoup
import collections
import random
import re

# 1. INK & PAPER BRANDING
st.set_page_config(page_title="Lucky Number Pro", page_icon="📈", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stApp { background-color: #ffffff; }
    h1, h2, h3 { color: #000000 !important; font-family: 'Inter', sans-serif; font-weight: 700 !important; }
    p, span, label { color: #000000 !important; }
    .stTextInput>div>div>input { border: 1px solid #000000 !important; border-radius: 4px !important; }
    .stButton>button { width: 100%; border-radius: 4px; height: 3.5em; background-color: #000000; color: #ffffff; font-weight: 600; border: none; text-transform: uppercase; }
    .stButton>button:hover { background-color: #333333; }
    [data-testid="stMetricValue"] { color: #000000 !important; font-weight: 800 !important; }
    .stMetric { border: 1px solid #eeeeee; padding: 15px; border-radius: 4px; }
    .stInfo { background-color: #ffffff; border: 1px solid #000000; color: #000000; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE WINNING VAULT (Your fed data - Priority 1)
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
    password = st.text_input("ACCESS KEY", type="password")
    if st.button("Unlock Engine"):
        if password == "eugene2026":
            st.session_state['logged_in'] = True
            st.rerun()
        else: st.error("Access Denied.")
    st.divider()
    st.markdown("### PRO MEMBERSHIP - RM 9.90")
    st.link_button("ACTIVATE SUBSCRIPTION", "https://buy.stripe.com/7sY8wPdWN7FdeQkanIcbC00")

if st.session_state['logged_in']:
    st.title("LUCKY NUMBER PRO")
    
    with st.sidebar:
        if st.button("Log Out"):
            st.session_state['logged_in'] = False
            st.rerun()

    @st.cache_data(ttl=3600)
    def get_live_data():
        try:
            url = "https://www.4dmoon.com/"
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            nums = re.findall(r'\b\d{4}\b', BeautifulSoup(r.text, 'html.parser').get_text())
            return "".join(nums[:120])
        except: return ""

    if st.button("GENERATE MASTER ANALYSIS"):
        with st.spinner("Extracting Winning Signature from Vault..."):
            live = get_live_data()
            
            # MATH RECALIBRATION: 4x weight for Winnings, 1x for Live
            final_pool = (VAULT_4D * 4) + live
            counts = collections.Counter(final_pool)
            ranked = [d for d, _ in counts.most_common()]
            
            # Tiered for variety but heavily biased toward your winnings (8, 0, 4, 7)
            top_signature = ranked[:4]
            secondary_tier = ranked[4:8]

            st.markdown("### 10 Calibrated 4D Lines")
            report_text = "LUCKY NUMBER PRO - 4D ANALYSIS\n"
            c = st.columns(2)
            for i in range(10):
                # We use the 'winning signature' as the core of every single line
                line = random.sample(top_signature, 3) + random.sample(secondary_tier, 1)
                random.shuffle(line)
                res = "".join(line)
                report_text += f"Line {i+1}: {res}\n"
                with c[i % 2]: st.metric(label=f"Analysis {i+1}", value=res)

            st.divider()
            st.markdown("### 6 Supreme 6/58 Matrix Lines")
            report_text += "\nSUPREME 6/58 ANALYSIS\n"
            l_pool = [b for d in VAULT_658 for b in d]
            l_counts = collections.Counter(l_pool)
            l_hot = [b for b, _ in l_counts.most_common(12)]
            
            lc = st.columns(2)
            for i in range(6):
                line = sorted(random.sample(l_hot, 6))
                res_lotto = " ".join(f"{n:02d}" for n in line)
                report_text += f"Lotto {i+1}: {res_lotto}\n"
                with lc[i % 2]: st.info(res_lotto)

            # DOWNLOAD FEATURE
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 DOWNLOAD RESULTS (.TXT)",
                data=report_text,
                file_name="lucky_matrix_results.txt",
                mime="text/plain"
            )

else:
    show_login_page()

st.divider()
st.caption("© 2026 LUCKY NUMBER ANALYTICS.")
