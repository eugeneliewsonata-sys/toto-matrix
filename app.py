import streamlit as st
import requests
from bs4 import BeautifulSoup
import collections
import random
import re

# 1. PREMIUM "OPTION A" BRANDING (Gold & Charcoal)
st.set_page_config(page_title="Lucky Matrix Pro", page_icon="🏆", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0f0f0f; }
    .stApp { background-color: #0f0f0f; }
    
    /* Executive Gold Buttons */
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        height: 3.8em; 
        background-color: #D4AF37; 
        color: #000000; 
        font-weight: 800; 
        border: 2px solid #C5A028;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #f1c40f;
        border: 2px solid #ffffff;
        transform: scale(1.02);
    }

    /* Input & Box Styling */
    .stTextInput>div>div>input { 
        border-radius: 10px; 
        border: 1px solid #D4AF37; 
        background-color: #1a1a1a;
        color: white;
    }
    
    .subscription-box { 
        border: 2px solid #D4AF37; 
        padding: 25px; 
        border-radius: 20px; 
        background-color: #1a1a1a; 
        text-align: center;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.2);
    }
    
    h1, h2, h3 { color: #D4AF37 !important; }
    p { color: #cccccc; }
    </style>
    """, unsafe_allow_html=True)

# 2. THE HISTORICAL DATA VAULT
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
    st.title("🏆 Lucky Matrix Pro")
    st.subheader("Premium Frequency Engine | Pro Tier")
    
    with st.container():
        st.write("### Member Secure Access")
        # ACCESS KEY IS: eugene2026
        password = st.text_input("Enter Access Key", type="password", placeholder="••••••••")
        if st.button("UNLOCK THE MATRIX"):
            if password == "eugene2026":
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Access Key Denied. Subscription required.")

    st.divider()

    st.markdown("""
        <div class="subscription-box">
            <h2 style="margin-top:0;">👑 Become a VIP Member</h2>
            <p>Unlock the Live Frequency Scraper & Master Historical Vault.</p>
            <h1 style="color:#D4AF37; margin-bottom:10px;">RM 19.00</h1>
            <p style="font-size: 0.9em;">Instant Access • Mobile Ready • Weekly Updates</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.link_button("💳 ACTIVATE VIP ACCESS (STRIPE)", "https://buy.stripe.com/7sY8wPdWN7FdeQkanIcbC00") 
    st.caption("Secured via Global Stripe Encryption")

# 4. ENGINE CORE (Post-Login)
if st.session_state['logged_in']:
    st.title("🏆 Lucky Matrix Pro")
    st.write(f"Welcome, **VIP Member**")
    
    with st.sidebar:
        st.header("Membership")
        st.success("Status: VIP ACTIVE")
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

    if st.button("🚀 EXECUTE FREQUENCY ANALYSIS"):
        with st.spinner("Processing Vault Data + Live Market Feed..."):
            live = get_live_data()
            pool = live + VAULT_4D
            counts = collections.Counter(pool)
            hot = [d for d, _ in counts.most_common(4)]
            cold = [d for d, _ in reversed(counts.most_common(3))]

            st.success("Analysis Complete. Matrix Calibrated.")
            
            st.markdown("### 🎫 Master 4D i-Perms")
            c = st.columns(3)
            for i in range(6):
                line = random.sample(hot, 3) + random.sample(cold, 1)
                random.shuffle(line)
                with c[i % 3]: 
                    st.info(f"**#{i+1}**\n\n# **{''.join(line)}**")

            st.divider()
            st.markdown("### 🔴 Supreme 6/58 Matrix")
            l_pool = [b for d in VAULT_658 for b in d]
            l_counts = collections.Counter(l_pool)
            l_hot = [b for b, _ in l_counts.most_common(12)]
            
            lc = st.columns(2)
            for i in range(4):
                line = sorted(random.sample(l_hot, 6))
                with lc[i % 2]: 
                    st.success(f"**Line {i+1}**\n\n**{' '.join(f'{n:02d}' for n in line)}**")

else:
    show_login_page()

st.divider()
st.caption("© 2026 Lucky Matrix Analytics. All Rights Reserved.")
