import streamlit as st
import requests
from bs4 import BeautifulSoup
import collections
import random
import re
from datetime import datetime, timedelta
import json
import gspread
from google.oauth2.service_account import Credentials
import streamlit.components.v1 as components

# 1. PREMIUM BRANDING & FONT
st.set_page_config(page_title="Lucky Number Pro", page_icon="📈", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');
    
    /* Global Styles */
    .main { background-color: #ffffff !important; }
    .stApp { background-color: #ffffff !important; }
    
    /* Target only our text, not system icons */
    .stMarkdown, .stText, .stTitle, h1, h2, h3, h4, h5, h6, p, span, label, [data-testid="stMetricValue"] { 
        color: #000000 !important; 
        font-family: 'Montserrat', sans-serif !important; 
    }
    
    /* FIX: Ensure the top-bar icons don't show as text */
    header, [data-testid="stHeader"] { background-color: rgba(255,255,255,0) !important; color: #000000 !important; }
    
    /* THE BUTTON: White Background, Black Text, Bold Border */
    .stButton>button { 
        width: 100%; border-radius: 0px !important; height: 4em; 
        background-color: #ffffff !important; color: #000000 !important; 
        font-weight: 900 !important; border: 4px solid #000000 !important; 
        text-transform: uppercase; letter-spacing: 2px; 
    }
    .stButton>button:hover { background-color: #000000 !important; color: #ffffff !important; }
    
    /* Input Fields */
    .stTextInput>div>div>input { border: 2px solid #000000 !important; color: #000000 !important; }
    
    /* Info boxes and Dividers */
    .stInfo { background-color: #f2f2f2 !important; border: 2px solid #000000 !important; color: #000000 !important; font-weight: bold;}
    hr { border-top: 2px solid #000000 !important; }
    
    /* Clock Styling */
    .live-clock { text-align: right; font-weight: 700; font-size: 0.9rem; color: #666666 !important; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# 2. MASTER VAULT DATA
VAULT_4D = "80474206710328685044035084831805444041755938586455209168453600187307197177718803120963611044"
VAULT_658 = [[18, 19, 29, 30, 36, 54], [2, 16, 20, 33, 34, 49], [8, 16, 22, 33, 53, 56], [4, 5, 13, 17, 22, 54], [7, 10, 18, 23, 26, 41], [26, 34, 39, 46, 47, 49], [5, 6, 15, 22, 40, 53], [4, 19, 29, 39, 50, 54]]
VAULT_655 = [[5, 12, 28, 33, 41, 52], [2, 18, 24, 39, 45, 55], [7, 14, 21, 30, 48, 51], [9, 13, 27, 35, 42, 53], [4, 11, 22, 36, 49, 54]] 
VAULT_650 = [[6, 15, 22, 31, 40, 48], [1, 10, 19, 28, 37, 49], [8, 17, 26, 35, 44, 50], [3, 12, 21, 30, 39, 47], [5, 14, 23, 32, 41, 46]]

# 3. DATABASE CONNECTION
@st.cache_resource
def init_connection():
    creds_dict = json.loads(st.secrets["gcp_json"])
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    sheet_url = "https://docs.google.com/spreadsheets/d/1-tS2J7ud1Nu5swMo9kBPHWRtwYjH70lU1TQObnw3YWA/edit?gid=0#gid=0"
    return client.open_by_url(sheet_url).worksheet("Users")

try:
    sheet = init_connection()
except Exception as e:
    st.error(f"DATABASE ERROR: {e}"); st.stop()

def get_database():
    records = sheet.get_all_records()
    return {str(r['Phone']): {'code': str(r['Code']), 'name': str(r['Name']), 'credits': int(r['Credits']), 'row': i + 2} for i, r in enumerate(records)}

# MALAYSIA TIME HELPER
def get_malaysia_time():
    return datetime.utcnow() + timedelta(hours=8)

# 4. LOGIN LOGIC
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = ""

def show_login_page():
    now_my = get_malaysia_time().strftime("%A, %d %b %Y | %H:%M:%S")
    st.markdown(f'<p class="live-clock">KL TIME: {now_my}</p>', unsafe_allow_html=True)
    st.title("LUCKY NUMBER PRO")
    db = get_database()
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 REGISTER"])
    with tab1:
        p = st.text_input("PHONE ID", key="l_p")
        c = st.text_input("ACCESS CODE", type="password", key="l_c")
        if st.button("ENTER PORTAL"):
            if p in db and str(db[p]['code']) == c:
                st.session_state['logged_in'] = True; st.session_state['current_user'] = p; st.rerun()
            else: st.error("Incorrect details.")
    with tab2:
        rn, rp, rc = st.text_input("NAME"), st.text_input("PHONE"), st.text_input("CREATE CODE", type="password")
        if st.button("CREATE ACCOUNT"):
            if rn and rp and rc:
                if rp in db: st.error("Exists.")
                else: sheet.append_row([rp, rc, rn, 0]); st.success("Success! Now Login.")
            else: st.error("Fill all fields.")

# 5. MAIN APP
if st.session_state['logged_in']:
    db = get_database(); user_id = st.session_state['current_user']
    if user_id not in db: st.session_state['logged_in'] = False; st.rerun()
    user_data = db[user_id]
    
    now_my = get_malaysia_time().strftime("%A, %d %b %Y | %H:%M:%S")
    st.markdown(f'<p class="live-clock">KL TIME: {now_my}</p>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"### VIP: {user_data['name']}")
        st.markdown(f"## Credits: **{user_data['credits']}**")
        st.divider()
        nav = ["Matrix Engine", "My Account"]
        if user_id == "admin": nav.append("Admin Panel")
        page = st.radio("MENU", nav)
        if st.button("LOGOUT"): st.session_state['logged_in'] = False; st.rerun()

    if page == "Matrix Engine":
        st.title("PRO MATRIX ENGINE")
        
        @st.cache_data(ttl=3600)
        def get_live_data():
            try:
                r = requests.get("https://www.4dmoon.com/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                return "".join(re.findall(r'\b\d{4}\b', BeautifulSoup(r.text, 'html.parser').get_text())[:120])
            except: return ""

        if st.button("GENERATE MASTER ANALYSIS"):
            if user_data['credits'] > 0:
                with st.spinner("CALIBRATING..."):
                    st.balloons()
                    components.html(
                        """
                        <audio autoplay style="display:none;">
                            <source src="https://www.soundjay.com/misc/sounds/cash-register-purchase-1.mp3" type="audio/mpeg">
                        </audio>
                        """, height=0
                    )
                    
                    new_bal = user_data['credits'] - 1
                    sheet.update_cell(user_data['row'], 4, new_bal)
                    live = get_live_data()
                    ranked = [d for d, _ in collections.Counter((VAULT_4D * 4) + live).most_common()]
                    
                    st.success(f"Generated! Balance: {new_bal}")
                    
                    def get_hot(v_list, total_range, count=12):
                        all_nums = [n for sub in v_list for n in sub] if v_list else list(range(1, total_range+1))
                        return [n for n, _ in collections.Counter(all_nums).most_common(count)]

                    # 4D
                    st.markdown("### 10 Calibrated 4D Lines")
                    c4 = st.columns(2)
                    for i in range(10):
                        line = random.sample(ranked[:4], 3) + random.sample(ranked[4:8], 1)
                        random.shuffle(line)
                        with c4[i % 2]: st.metric(f"4D-{i+1}", "".join(line))
                    
                    # Jackpot Sections
                    st.divider(); st.markdown("### 6 Supreme 6/58 Matrix Lines")
                    h58 = get_hot(VAULT_658, 58); cs = st.columns(2)
                    for i in range(6):
                        with cs[i % 2]: st.info(" ".join(f"{n:02d}" for n in sorted(random.sample(h58, 6))))

                    st.divider(); st.markdown("### 6 Power 6/55 Matrix Lines")
                    h55 = get_hot(VAULT_655, 55); cp = st.columns(2)
                    for i in range(6):
                        with cp[i % 2]: st.info(" ".join(f"{n:02d}" for n in sorted(random.sample(h55, 6))))

                    st.divider(); st.markdown("### 6 Star 6/50 Matrix Lines")
                    h50 = get_hot(VAULT_650, 50); ct = st.columns(2)
                    for i in range(6):
                        with ct[i % 2]: st.info(" ".join(f"{n:02d}" for n in sorted(random.sample(h50, 6))))
            else: st.error("0 Credits. Please Top Up.")

    elif page == "My Account":
        st.title("ACCOUNT STATUS"); st.info(f"**CREDITS:** {user_data['credits']}")
        st.divider(); st.markdown("### TOP UP")
        st.link_button("💰 BUY 50 CREDITS (RM 10)", "https://buy.stripe.com/28E9AT5qh3oX9w0anIcbC02")

    elif page == "Admin Panel":
        st.title("SYSTEM ADMIN")
        tp, tc = st.text_input("Phone ID"), st.number_input("Add Credits", value=50)
        if st.button("UPDATE"):
            if tp in db: sheet.update_cell(db[tp]['row'], 4, db[tp]['credits'] + tc); st.success("Done!")
            else: st.error("Not Found")
        st.dataframe(db)
else: show_login_page()
st.caption("© 2026 LUCKY NUMBER ANALYTICS.")
