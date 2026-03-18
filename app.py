import streamlit as st
import requests
from bs4 import BeautifulSoup
import collections
import random
import re
from datetime import datetime
import json
import gspread
from google.oauth2.service_account import Credentials
import time

# 1. PREMIUM BRANDING & FONT
st.set_page_config(page_title="Lucky Number Pro", page_icon="📈", layout="centered")

# Injecting Montserrat Font and High-Contrast CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');

    .main { background-color: #ffffff !important; }
    .stApp { background-color: #ffffff !important; }
    
    /* Global Font & Text Color */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMetric { 
        color: #000000 !important; 
        font-family: 'Montserrat', sans-serif !important; 
    }

    /* THE BUTTON: White Background, Black Text, Bold Border */
    .stButton>button { 
        width: 100%; 
        border-radius: 0px !important; 
        height: 4em; 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        font-weight: 900 !important; 
        font-family: 'Montserrat', sans-serif !important;
        border: 4px solid #000000 !important; 
        text-transform: uppercase; 
        letter-spacing: 2px;
        transition: 0.2s ease-in-out;
    }
    
    .stButton>button:hover {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 4px solid #000000 !important;
    }

    /* Input Fields Customization */
    .stTextInput>div>div>input { 
        border: 2px solid #000000 !important; 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        font-family: 'Montserrat', sans-serif !important;
    }

    [data-testid="stMetricValue"] { color: #000000 !important; font-weight: 900 !important; font-size: 2.5rem !important; }
    .stInfo { background-color: #f2f2f2 !important; border: 2px solid #000000 !important; color: #000000 !important; font-weight: bold;}
    hr { border-top: 2px solid #000000 !important; }
    
    /* Tabs Style */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; 
        background-color: #ffffff; 
        color: #000000; 
        font-weight: 700;
        font-family: 'Montserrat', sans-serif !important;
    }

    /* Clock Styling */
    .live-clock {
        text-align: right;
        font-weight: 700;
        font-size: 0.9rem;
        color: #666666 !important;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. THE WINNING VAULT
VAULT_4D = "80474206710328685044035084831805444041755938586455209168453600187307197177718803120963611044"
VAULT_658 = [
    [18, 19, 29, 30, 36, 54], [2, 16, 20, 33, 34, 49], [8, 16, 22, 33, 53, 56],
    [4, 5, 13, 17, 22, 54], [7, 10, 18, 23, 26, 41], [26, 34, 39, 46, 47, 49],
    [5, 6, 15, 22, 40, 53], [4, 19, 29, 39, 50, 54]
]

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
    st.error(f"DATABASE ERROR: {e}")
    st.stop()

def get_database():
    records = sheet.get_all_records()
    db = {}
    for i, r in enumerate(records):
        db[str(r['Phone'])] = {'code': str(r['Code']), 'name': str(r['Name']), 'credits': int(r['Credits']), 'row': i + 2}
    return db

# 4. LOGIN LOGIC
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = ""

def show_login_page():
    # Live Clock on Login Page
    now = datetime.now().strftime("%A, %d %b %Y | %H:%M:%S")
    st.markdown(f'<p class="live-clock">{now}</p>', unsafe_allow_html=True)
    
    st.title("LUCKY NUMBER PRO")
    st.write("Professional Matrix Analytics")
    db = get_database()
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 REGISTER"])
    
    with tab1:
        phone_number = st.text_input("PHONE ID", placeholder="012xxxxxxx", key="l_p")
        access_code = st.text_input("ACCESS CODE", type="password", key="l_c")
        if st.button("ENTER PORTAL"):
            if phone_number in db and str(db[phone_number]['code']) == access_code:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = phone_number
                st.rerun()
            else: st.error("Incorrect details.")

    with tab2:
        reg_name = st.text_input("FULL NAME", key="r_n")
        reg_phone = st.text_input("PHONE NUMBER", key="r_p")
        reg_code = st.text_input("CREATE CODE", type="password", key="r_c")
        if st.button("CREATE ACCOUNT"):
            if not reg_name or not reg_phone or not reg_code: st.error("Fill all fields.")
            elif reg_phone in db: st.error("Account exists.")
            else:
                sheet.append_row([reg_phone, reg_code, reg_name, 0])
                st.success("Success! Now go to the Login tab.")

# 5. MAIN APP INTERFACE
if st.session_state['logged_in']:
    db = get_database()
    user_id = st.session_state['current_user']
    if user_id not in db:
        st.session_state['logged_in'] = False
        st.rerun()
    user_data = db[user_id]
    
    # Header with Live Clock
    now = datetime.now().strftime("%A, %d %b %Y | %H:%M:%S")
    st.markdown(f'<p class="live-clock">{now}</p>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(f"### VIP: {user_data['name']}")
        st.markdown(f"## Credits: **{user_data['credits']}**")
        st.divider()
        nav = ["Matrix Engine", "My Account"]
        if user_id == "admin": nav.append("Admin Panel")
        page = st.radio("MENU", nav)
        if st.button("LOGOUT"):
            st.session_state['logged_in'] = False
            st.rerun()

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
                    new_bal = user_data['credits'] - 1
                    sheet.update_cell(user_data['row'], 4, new_bal)
                    
                    live = get_live_data()
                    ranked = [d for d, _ in collections.Counter((VAULT_4D * 4) + live).most_common()]
                    
                    st.success(f"Generated! Balance: {new_bal}")
                    
                    c = st.columns(2)
                    for i in range(10):
                        line = random.sample(ranked[:4], 3) + random.sample(ranked[4:8], 1)
                        random.shuffle(line)
                        with c[i % 2]: st.metric(f"Analysis {i+1}", "".join(line))
            else: st.error("0 Credits. Please Top Up.")

    elif page == "My Account":
        st.title("ACCOUNT STATUS")
        st.info(f"**CREDITS REMAINING:** {user_data['credits']}")
        st.divider()
        st.markdown("### TOP UP CREDITS")
        st.link_button("💰 RM 10 for 50 CREDITS", "https://buy.stripe.com/28E9AT5qh3oX9w0anIcbC02")
        st.caption("WhatsApp payment screenshot to Admin for activation.")

    elif page == "Admin Panel":
        st.title("SYSTEM ADMIN")
        t_phone = st.text_input("Target Phone")
        t_creds = st.number_input("Credits to Add", min_value=1, value=50)
        if st.button("REFRESH USER WALLET"):
            if t_phone in db:
                sheet.update_cell(db[t_phone]['row'], 4, db[t_phone]['credits'] + t_creds)
                st.success("Wallet Updated!")
            else: st.error("User Not Found")
        st.dataframe(db)

else: show_login_page()

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 LUCKY NUMBER ANALYTICS.")
