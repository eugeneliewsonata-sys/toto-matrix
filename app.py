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

# --- BRANDING ---
st.set_page_config(page_title="HengOngHuat Pro", page_icon="🧧", layout="centered")

# 1. LANGUAGE DICTIONARY
LANG_DICT = {
    "English": {
        "title": "HENG ONG HUAT PRO",
        "subtitle": "Professional Matrix Analytics",
        "login": "🔐 LOGIN", "register": "📝 REGISTER",
        "phone_id": "PHONE ID", "pass": "ACCESS CODE",
        "btn_login": "ENTER PORTAL", "name": "FULL NAME",
        "btn_reg": "CREATE ACCOUNT", "vip": "VIP",
        "credits": "Credits", "menu": "MENU",
        "engine": "Matrix Engine", "account": "My Account",
        "admin": "Admin Panel", "btn_gen": "GENERATE MASTER ANALYSIS",
        "calibrating": "CALIBRATING DATA...", "generated": "Generated!",
        "bal": "Balance", "lines_4d": "10 Calibrated 4D Lines",
        "topup": "TOP UP CREDITS", "buy_btn": "💰 BUY 50 CREDITS (RM 10)",
        "whatsapp": "WhatsApp receipt to Admin.", "install": "📲 INSTALL APP", "logout": "LOGOUT"
    },
    "中文": {
        "title": "兴旺发专业版",
        "subtitle": "专业矩阵分析平台",
        "login": "🔐 登录", "register": "📝 注册账号",
        "phone_id": "手机号码", "pass": "访问密码",
        "btn_login": "进入系统", "name": "真实姓名",
        "btn_reg": "立即注册", "vip": "会员",
        "credits": "剩余积分", "menu": "功能菜单",
        "engine": "矩阵引擎", "account": "我的账户",
        "admin": "管理后台", "btn_gen": "开始大师级分析",
        "calibrating": "正在校准数据...", "generated": "生成成功！",
        "bal": "余额", "lines_4d": "10组 4D 精准预测",
        "topup": "充值积分", "buy_btn": "💰 购买 50 积分 (RM 10)",
        "whatsapp": "请发送收据给管理员。", "install": "📲 安装至桌面", "logout": "退出登录"
    }
}

# 2. CSS - THE STYLE SHIELD
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { background-color: #ffffff !important; font-family: 'Montserrat', sans-serif !important; }
    
    /* THE RED TEXT LOGO */
    .huat-logo {
        color: #FF0000 !important;
        font-weight: 900 !important;
        font-size: 2.5rem !important;
        letter-spacing: -1px;
        margin-bottom: 0px;
        text-align: center;
    }

    /* PROTECT SYSTEM ICONS */
    [data-testid="stSidebarCollapsedControl"] svg, [data-testid="baseButton-headerNoPadding"] svg {
        fill: #000000 !important;
        width: 32px !important;
        height: 32px !important;
    }

    .stButton>button {
        width: 100%; border-radius: 0px !important; height: 4em;
        background-color: #ffffff !important; color: #000000 !important;
        font-weight: 900 !important; border: 4px solid #000000 !important;
    }
    .stButton>button:hover { background-color: #FF0000 !important; color: #ffffff !important; border-color: #FF0000 !important;}
    
    .stMetric { color: #FF0000 !important; }
    [data-testid="stMetricValue"] { color: #FF0000 !important; font-weight: 900 !important; }
    .live-clock { text-align: right; font-weight: 700; color: #FF0000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. DATABASE
@st.cache_resource
def init_connection():
    creds_dict = json.loads(st.secrets["gcp_json"])
    client = gspread.authorize(Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]))
    return client.open_by_url("https://docs.google.com/spreadsheets/d/1-tS2J7ud1Nu5swMo9kBPHWRtwYjH70lU1TQObnw3YWA/edit?gid=0#gid=0").worksheet("Users")

sheet = init_connection()

def get_database():
    records = sheet.get_all_records()
    return {str(r['Phone']): {'code': str(r['Code']), 'name': str(r['Name']), 'credits': int(r['Credits']), 'row': i + 2} for i, r in enumerate(records)}

def get_my_time(): return datetime.utcnow() + timedelta(hours=8)

# 4. STATE
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'lang' not in st.session_state: st.session_state['lang'] = "English"
L = LANG_DICT[st.session_state['lang']]

# 5. UI
if not st.session_state['logged_in']:
    st.markdown('<h1 class="huat-logo">HENG ONG HUAT</h1>', unsafe_allow_html=True)
    st.session_state['lang'] = st.sidebar.selectbox("Language / 语言", ["English", "中文"])
    db = get_database()
    t1, t2 = st.tabs([L['login'], L['register']])
    with t1:
        p = st.text_input(L['phone_id'], key="lp")
        c = st.text_input(L['pass'], type="password", key="lc")
        if st.button(L['btn_login']):
            if p in db and str(db[p]['code']) == c:
                st.session_state['logged_in'] = True; st.session_state['current_user'] = p; st.rerun()
    with t2:
        rn, rp, rc = st.text_input(L['name']), st.text_input(L['phone_id'], key="rp"), st.text_input(L['pass'], type="password", key="rc")
        if st.button(L['btn_reg']):
            if rn and rp and rc and rp not in db:
                sheet.append_row([rp, rc, rn, 0]); st.success("Success!")

else:
    db = get_database(); user_id = st.session_state['current_user']
    user_data = db[user_id]
    st.markdown(f'<p class="live-clock">{get_my_time().strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<h1 style="color:red; font-size:25px; font-weight:900;">HENG ONG HUAT</h1>', unsafe_allow_html=True)
        st.session_state['lang'] = st.selectbox("Language", ["English", "中文"], index=0 if st.session_state['lang'] == "English" else 1)
        st.markdown(f"### {L['vip']}: {user_data['name']}\n## {L['credits']}: **{user_data['credits']}**")
        page = st.radio(L['menu'], [L['engine'], L['account']] + ([L['admin']] if user_id == "admin" else []))
        if st.button(L['logout']): st.session_state['logged_in'] = False; st.rerun()

    if page == L['engine']:
        st.title(L['engine'])
        if st.button(L['btn_gen']) and user_data['credits'] > 0:
            # --- THE HUAT TRIGGER ---
            components.html("""
                <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
                <script>
                    confetti({
                        particleCount: 150,
                        spread: 70,
                        origin: { y: 0.6 },
                        colors: ['#FFD700', '#FFA500', '#FF0000']
                    });
                </script>
                <audio autoplay>
                    <source src="https://www.soundjay.com/misc/sounds/cash-register-purchase-1.mp3" type="audio/mpeg">
                </audio>
            """, height=1)
            
            new_bal = user_data['credits'] - 1
            sheet.update_cell(user_data['row'], 4, new_bal)
            st.success(f"{L['generated']} {L['bal']}: {new_bal}")
            
            # Simple Analysis Display
            c4 = st.columns(2)
            for i in range(10):
                line = "".join(random.sample("1234567890", 4))
                with c4[i%2]: st.metric(f"4D No.{i+1}", line)
    
    elif page == L['account']:
        st.title(L['account'])
        st.link_button(L['buy_btn'], "https://buy.stripe.com/28E9AT5qh3oX9w0anIcbC02")

st.caption("© 2026 HENG ONG HUAT ANALYTICS.")
