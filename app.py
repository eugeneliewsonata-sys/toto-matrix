import streamlit as st
import requests
from bs4 import BeautifulSoup
import collections
import random
import re
from datetime import datetime

# 1. HIGH-CONTRAST INK BRANDING
st.set_page_config(page_title="Lucky Number Pro", page_icon="📈", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #ffffff !important; }
    .stApp { background-color: #ffffff !important; }
    h1, h2, h3, h4, h5, h6 { color: #000000 !important; font-family: 'Inter', sans-serif; font-weight: 800 !important;}
    p, span, label, div { color: #000000 !important; }
    .stButton>button { width: 100%; border-radius: 4px !important; height: 3.5em; background-color: #000000 !important; color: #ffffff !important; font-weight: 700 !important; border: 2px solid #000000 !important; text-transform: uppercase; letter-spacing: 1px; }
    .stTextInput>div>div>input { border: 1px solid #000000 !important; background-color: #ffffff !important; color: #000000 !important; }
    [data-testid="stMetricValue"] { color: #000000 !important; font-weight: 900 !important; }
    [data-testid="stMetricLabel"] { color: #666666 !important; }
    .stInfo { background-color: #f2f2f2 !important; border: 1px solid #000000 !important; color: #000000 !important; font-weight: bold;}
    hr { border-top: 1px solid #000000 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #ffffff; border-radius: 4px; color: #000000; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# 2. THE WINNING VAULT
VAULT_4D = "80474206710328685044035084831805444041755938586455209168453600187307197177718803120963611044"
VAULT_658 = [
    [18, 19, 29, 30, 36, 54], [2, 16, 20, 33, 34, 49], [8, 16, 22, 33, 53, 56],
    [4, 5, 13, 17, 22, 54], [7, 10, 18, 23, 26, 41], [26, 34, 39, 46, 47, 49],
    [5, 6, 15, 22, 40, 53], [4, 19, 29, 39, 50, 54]
]

# 3. THE VIRTUAL DATABASE
if 'db' not in st.session_state:
    st.session_state['db'] = {
        "admin": {"code": "eugene2026", "name": "System Admin", "credits": 9999}
    }

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = ""

def show_login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("LUCKY NUMBER PRO")
    st.write("Matrix Analytics Platform")
    
    tab1, tab2 = st.tabs(["🔐 EXISTING MEMBER", "📝 CREATE ACCOUNT"])
    
    with tab1:
        st.markdown("### ACCOUNT LOGIN")
        phone_number = st.text_input("PHONE NUMBER", placeholder="e.g., 0123456789", key="login_phone")
        access_code = st.text_input("ACCESS CODE", type="password", key="login_code")
        
        if st.button("Secure Login"):
            if phone_number in st.session_state['db'] and st.session_state['db'][phone_number]['code'] == access_code:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = phone_number
                st.rerun()
            else:
                st.error("Login Failed. Number or Code is incorrect.")

    with tab2:
        st.markdown("### NEW REGISTRATION")
        st.write("Create a free account. You will need to purchase credits inside to use the Matrix.")
        reg_name = st.text_input("DISPLAY NAME", placeholder="What should we call you?")
        reg_phone = st.text_input("PHONE NUMBER", placeholder="This will be your Login ID")
        reg_code = st.text_input("CREATE ACCESS CODE", type="password", placeholder="Create a password")
        
        if st.button("Register Free Account"):
            if not reg_name or not reg_phone or not reg_code:
                st.error("Please fill in all fields.")
            elif reg_phone in st.session_state['db']:
                st.error("An account with this phone number already exists.")
            else:
                st.session_state['db'][reg_phone] = {"code": reg_code, "name": reg_name, "credits": 0}
                st.success("Account created! Please switch to the 'Existing Member' tab to log in.")

# 4. APP ROUTING & UI
if st.session_state['logged_in']:
    user_id = st.session_state['current_user']
    user_data = st.session_state['db'][user_id]
    
    with st.sidebar:
        st.markdown(f"### Welcome, {user_data['name']}")
        st.write(f"**Credits: {user_data['credits']}**")
        st.divider()
        page = st.radio("NAVIGATION", ["Matrix Engine", "My Account", "Admin Panel"] if user_id == "admin" else ["Matrix Engine", "My Account"])
        st.divider()
        if st.button("Log Out"):
            st.session_state['logged_in'] = False
            st.session_state['current_user'] = ""
            st.rerun()

    if page == "Matrix Engine":
        st.title("LUCKY NUMBER PRO")
        st.write("Live Data Frequency Engine")

        @st.cache_data(ttl=3600)
        def get_live_data():
            try:
                r = requests.get("https://www.4dmoon.com/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                nums = re.findall(r'\b\d{4}\b', BeautifulSoup(r.text, 'html.parser').get_text())
                return "".join(nums[:120])
            except: return ""

        if st.button("GENERATE MASTER ANALYSIS (1 Credit)"):
            if user_data['credits'] > 0:
                with st.spinner("Processing..."):
                    st.session_state['db'][user_id]['credits'] -= 1
                    live = get_live_data()
                    final_pool = (VAULT_4D * 4) + live
                    counts = collections.Counter(final_pool)
                    ranked = [d for d, _ in counts.most_common()]
                    
                    st.success(f"Generation Complete! Credits remaining: {st.session_state['db'][user_id]['credits']}")
                    
                    now = datetime.now().strftime("%Y-%m-%d %H:%M")
                    report = f"LUCKY NUMBER PRO REPORT\n{now}\nUser: {user_data['name']}\n\n"
                    
                    st.markdown("### 10 Calibrated 4D Lines")
                    c = st.columns(2)
                    for i in range(10):
                        line = random.sample(ranked[:4], 3) + random.sample(ranked[4:8], 1)
                        random.shuffle(line)
                        res = "".join(line)
                        report += f"4D-{i+1}: {res}\n"
                        with c[i % 2]: st.metric(label=f"Analysis {i+1}", value=res)

                    st.divider()
                    st.markdown("### 6 Supreme 6/58 Matrix Lines")
                    l_pool = [b for d in VAULT_658 for b in d]
                    l_counts = collections.Counter(l_pool)
                    l_hot = [b for b, _ in l_counts.most_common(12)]
                    
                    lc = st.columns(2)
                    for i in range(6):
                        line = sorted(random.sample(l_hot, 6))
                        res_lotto = " ".join(f"{n:02d}" for n in line)
                        report += f"L658-{i+1}: {res_lotto}\n"
                        with lc[i % 2]: st.info(res_lotto)
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.download_button(
                        label="📥 DOWNLOAD REPORT (.TXT)",
                        data=report,
                        file_name=f"Lucky_Matrix_{datetime.now().strftime('%d_%m')}.txt",
                        mime="text/plain"
                    )
            else:
                st.error("Insufficient Credits! Please go to 'My Account' to top up.")

    elif page == "My Account":
        st.title("ACCOUNT & WALLET")
        col1, col2 = st.columns(2)
        with col1: st.info(f"**CREDITS**\n# {user_data['credits']}")
        with col2: st.info(f"**PHONE ID**\n# {user_id}")
            
        st.divider()
        st.markdown("### TOP UP WALLET")
        # YOUR NEW STRIPE LINK IS ACTIVE HERE
        st.link_button("💰 BUY 50 CREDITS (RM 10)", "https://buy.stripe.com/28E9AT5qh3oX9w0anIcbC02")
        
        st.caption("Note: After payment, please WhatsApp your receipt to the Admin to have credits loaded into your account.")
        
    elif page == "Admin Panel":
        st.title("⚙️ SYSTEM ADMIN PANEL")
        st.write("Current Database:", st.session_state['db'])
        
        st.markdown("### ADD CREDITS TO USER")
        target_phone = st.text_input("User Phone Number")
        credits_to_add = st.number_input("Credits to Add", min_value=1, value=50)
        if st.button("Add Credits"):
            if target_phone in st.session_state['db']:
                st.session_state['db'][target_phone]['credits'] += credits_to_add
                st.success(f"Added {credits_to_add} credits to {target_phone}!")
            else: st.error("User not found.")

else:
    show_login_page()

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 LUCKY NUMBER ANALYTICS.")
