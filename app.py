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
    </style>
    """, unsafe_allow_html=True)

# 2. THE WINNING VAULT
VAULT_4D = "80474206710328685044035084831805444041755938586455209168453600187307197177718803120963611044"
VAULT_658 = [
    [18, 19, 29, 30, 36, 54], [2, 16, 20, 33, 34, 49], [8, 16, 22, 33, 53, 56],
    [4, 5, 13, 17, 22, 54], [7, 10, 18, 23, 26, 41], [26, 34, 39, 46, 47, 49],
    [5, 6, 15, 22, 40, 53], [4, 19, 29, 39, 50, 54]
]

# 3. THE VIRTUAL DATABASE (Session State)
# In a real commercial app, this connects to Firebase. For now, it lives in memory.
if 'db' not in st.session_state:
    st.session_state['db'] = {
        "admin": {"code": "eugene2026", "name": "System Admin", "credits": 9999},
        "0123456789": {"code": "VIP-1234", "name": "Demo User", "credits": 5}
    }

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = ""

def show_login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("LUCKY NUMBER PRO")
    st.write("Secure Member Portal")
    
    phone_number = st.text_input("PHONE NUMBER", placeholder="e.g., 0123456789")
    access_code = st.text_input("ACCESS CODE", type="password")
    
    if st.button("Secure Login"):
        if phone_number in st.session_state['db'] and st.session_state['db'][phone_number]['code'] == access_code:
            st.session_state['logged_in'] = True
            st.session_state['current_user'] = phone_number
            st.rerun()
        else:
            st.error("Login Failed. Number or Code is incorrect.")

    st.divider()
    st.markdown("### BECOME A VIP MEMBER")
    st.write("Gain access to the Master Matrix. Account setup is manual after payment.")
    st.link_button("PURCHASE STARTER PACK (RM 10 = 50 CREDITS)", "https://buy.stripe.com/7sY8wPdWN7FdeQkanIcbC00")

# 4. APP ROUTING & UI
if st.session_state['logged_in']:
    user_id = st.session_state['current_user']
    user_data = st.session_state['db'][user_id]
    
    # NAVIGATION SIDEBAR
    with st.sidebar:
        st.markdown(f"### Welcome, {user_data['name']}")
        st.write(f"**Credits Left: {user_data['credits']}**")
        st.divider()
        page = st.radio("NAVIGATION MENU", ["Matrix Engine", "My Account"])
        
        # Admin gets an extra tab
        if user_id == "admin":
            page = st.radio("ADMIN MENU", ["Matrix Engine", "My Account", "Admin Panel"])
            
        st.divider()
        if st.button("Log Out"):
            st.session_state['logged_in'] = False
            st.session_state['current_user'] = ""
            st.rerun()

    # PAGE 1: THE MATRIX ENGINE
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

        if st.button("GENERATE MASTER ANALYSIS (Cost: 1 Credit)"):
            if user_data['credits'] > 0:
                with st.spinner("Processing..."):
                    # Deduct Credit
                    st.session_state['db'][user_id]['credits'] -= 1
                    
                    live = get_live_data()
                    final_pool = (VAULT_4D * 4) + live
                    counts = collections.Counter(final_pool)
                    ranked = [d for d, _ in counts.most_common()]
                    
                    st.success(f"Generation Complete! Credits remaining: {st.session_state['db'][user_id]['credits']}")
                    
                    st.markdown("### 10 Calibrated 4D Lines")
                    c = st.columns(2)
                    for i in range(10):
                        line = random.sample(ranked[:4], 3) + random.sample(ranked[4:8], 1)
                        random.shuffle(line)
                        with c[i % 2]: st.metric(label=f"Analysis {i+1}", value="".join(line))
            else:
                st.error("Insufficient Credits! Please top up in the 'My Account' tab.")

    # PAGE 2: MY ACCOUNT
    elif page == "My Account":
        st.title("ACCOUNT & WALLET")
        st.write("Manage your profile and credits.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**CREDIT BALANCE**\n# {user_data['credits']}")
        with col2:
            st.info(f"**PHONE ID**\n# {user_id}")
            
        st.divider()
        st.markdown("### TOP UP WALLET")
        st.write("Purchase more credits to continue using the engine.")
        # Make sure you create different Stripe links for different credit packs!
        st.link_button("💰 TOP UP 50 CREDITS (RM 10)", "https://buy.stripe.com/7sY8wPdWN7FdeQkanIcbC00")
        st.link_button("💎 TOP UP 200 CREDITS (RM 30)", "https://buy.stripe.com/7sY8wPdWN7FdeQkanIcbC00")
        
        st.divider()
        st.markdown("### EDIT PROFILE")
        new_name = st.text_input("Display Name", value=user_data['name'])
        new_password = st.text_input("Change Access Code", value=user_data['code'], type="password")
        if st.button("Save Changes"):
            st.session_state['db'][user_id]['name'] = new_name
            st.session_state['db'][user_id]['code'] = new_password
            st.success("Profile Updated Successfully!")

    # PAGE 3: ADMIN PANEL (Only visible to admin)
    elif page == "Admin Panel":
        st.title("⚙️ SYSTEM ADMIN PANEL")
        st.write("Add new paying users and issue credits.")
        
        st.markdown("### REGISTER NEW USER")
        new_phone = st.text_input("User Phone Number (ID)")
        new_code = st.text_input("Temporary Access Code")
        starting_credits = st.number_input("Starting Credits", min_value=0, value=50)
        
        if st.button("Create User Account"):
            if new_phone and new_code:
                st.session_state['db'][new_phone] = {"code": new_code, "name": "VIP User", "credits": starting_credits}
                st.success(f"User {new_phone} added with {starting_credits} credits!")
            else:
                st.error("Please fill in both Phone and Code.")
                
        st.divider()
        st.markdown("### ACTIVE USER DATABASE")
        st.write(st.session_state['db'])

else:
    show_login_page()

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 LUCKY NUMBER ANALYTICS.")
