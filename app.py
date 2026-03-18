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

# --- BRANDING & LOGO ---
LOGO_URL = "https://i.imgur.com/8kX4S7S.png" # Red background, Yellow words as requested

st.set_page_config(
    page_title="HengOngHuat Pro", 
    page_icon=LOGO_URL, 
    layout="centered"
)

# 1. LANGUAGE DICTIONARY
LANG_DICT = {
    "English": {
        "title": "HENG ONG HUAT PRO",
        "subtitle": "Professional Matrix Analytics",
        "login": "🔐 LOGIN",
        "register": "📝 REGISTER",
        "phone_id": "PHONE ID",
        "pass": "ACCESS CODE",
        "btn_login": "ENTER PORTAL",
        "name": "FULL NAME",
        "btn_reg": "CREATE ACCOUNT",
        "vip": "VIP",
        "credits": "Credits",
        "menu": "MENU",
        "engine": "Matrix Engine",
        "account": "My Account",
        "admin": "Admin Panel",
        "btn_gen": "GENERATE MASTER ANALYSIS",
        "calibrating": "CALIBRATING DATA...",
        "generated": "Generated!",
        "bal": "Balance",
        "lines_4d": "10 Calibrated 4D Lines",
        "lines_58": "6 Supreme 6/58 Matrix Lines",
        "lines_55": "6 Power 6/55 Matrix Lines",
        "lines_50": "6 Star 6/50 Matrix Lines",
        "topup": "TOP UP CREDITS",
        "buy_btn": "💰 BUY 50 CREDITS (RM 10)",
        "whatsapp": "WhatsApp receipt to Admin for activation.",
        "install": "📲 INSTALL AS APP",
        "logout": "LOGOUT"
    },
    "中文": {
        "title": "兴旺发专业版 (HENG ONG HUAT)",
        "subtitle": "专业矩阵分析平台",
        "login": "🔐 登录",
        "register": "📝 注册账号",
        "phone_id": "手机号码",
        "pass": "访问密码",
        "btn_login": "进入系统",
        "name": "真实姓名",
        "btn_reg": "立即注册",
        "vip": "会员",
        "credits": "剩余积分",
        "menu": "功能菜单",
        "engine": "矩阵引擎",
        "account": "我的账户",
        "admin": "管理后台",
        "btn_gen": "开始大师级分析",
        "calibrating": "正在校准数据...",
        "generated": "生成成功！",
        "bal": "余额",
        "lines_4d": "10组 4D 精准预测",
        "lines_58": "6组 Supreme 6/58 矩阵",
        "lines_55": "6组 Power 6/55 矩阵",
        "lines_50": "6组 Star 6/50 矩阵",
        "topup": "充值积分",
        "buy_btn": "💰 购买 50 积分 (RM 10)",
        "whatsapp": "请将付款收据发送至 WhatsApp 给管理员。",
        "install": "📲 安装至手机桌面",
        "logout": "退出登录"
    }
}

# 2. CUSTOM CSS (HengOngHuat Red & Yellow Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');
    .main, .stApp { background-color: #ffffff !important; }
    h1, h2, h3, h4, h5, h6, p, label, .stMetric, span { 
        color: #000000 !important; 
        font-family: 'Montserrat', sans-serif !important; 
    }
    /* Buttons: Yellow Text on Black or Red Background */
    .stButton>button { 
        width: 100%; border-radius: 0px !important; height: 4em; 
        background-color: #ffffff !important; color: #000000 !important; 
        font-weight: 900 !important; border: 4px solid #000000 !important; 
        text-transform: uppercase; letter-spacing: 2px; 
    }
    .stButton>button:hover { background-color: #d32f2f !important; color: #ffffff !important; border-color: #d32f2f !important;}
    .stTextInput>div>div>input { border: 2px solid #000000 !important; }
    [data-testid="stMetricValue"] { color: #d32f2f !important; font-weight: 900 !important; }
    .live-clock { text-align: right; font-weight: 700; font-size: 0.9rem; color: #d32f2f !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. DATABASE & TIME
@st.cache_resource
def init_connection():
    creds_dict = json.loads(st.secrets["gcp_json"])
    client = gspread.authorize(Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]))
    return client.open_by_url("https://docs.google.com/spreadsheets/d/1-tS2J7ud1Nu5swMo9kBPHWRtwYjH70lU1TQObnw3YWA/edit?gid=0#gid=0").worksheet("Users")

try: sheet = init_connection()
except: st.error("DB Error"); st.stop()

def get_database():
    records = sheet.get_all_records()
    return {str(r['Phone']): {'code': str(r['Code']), 'name': str(r['Name']), 'credits': int(r['Credits']), 'row': i + 2} for i, r in enumerate(records)}

def get_my_time(): return datetime.utcnow() + timedelta(hours=8)

# 4. SESSION STATE
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'lang' not in st.session_state: st.session_state['lang'] = "English"

L = LANG_DICT[st.session_state['lang']]

# 5. UI COMPONENTS
def show_login_page():
    now = get_my_time().strftime("%d %b %Y | %H:%M:%S")
    st.markdown(f'<p class="live-clock">{now}</p>', unsafe_allow_html=True)
    st.sidebar.image(LOGO_URL, use_column_width=True)
    st.session_state['lang'] = st.sidebar.selectbox("Select Language / 选择语言", ["English", "中文"])
    
    st.title(L['title'])
    st.write(L['subtitle'])
    db = get_database()
    t1, t2 = st.tabs([L['login'], L['register']])
    with t1:
        p = st.text_input(L['phone_id'], key="lp")
        c = st.text_input(L['pass'], type="password", key="lc")
        if st.button(L['btn_login']):
            if p in db and str(db[p]['code']) == c:
                st.session_state['logged_in'] = True; st.session_state['current_user'] = p; st.rerun()
            else: st.error("Error")
    with t2:
        rn, rp, rc = st.text_input(L['name']), st.text_input(L['phone_id'], key="rp"), st.text_input(L['pass'], type="password", key="rc")
        if st.button(L['btn_reg']):
            if rn and rp and rc:
                if rp in db: st.error("Exists")
                else: sheet.append_row([rp, rc, rn, 0]); st.success("Success!")

if st.session_state['logged_in']:
    db = get_database(); user_id = st.session_state['current_user']
    if user_id not in db: st.session_state['logged_in'] = False; st.rerun()
    user_data = db[user_id]
    
    st.markdown(f'<p class="live-clock">{get_my_time().strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.image(LOGO_URL, use_column_width=True)
        st.session_state['lang'] = st.selectbox("Language / 语言", ["English", "中文"], index=0 if st.session_state['lang'] == "English" else 1)
        st.markdown(f"### {L['vip']}: {user_data['name']}")
        st.markdown(f"## {L['credits']}: **{user_data['credits']}**")
        st.divider()
        nav_opts = [L['engine'], L['account']]
        if user_id == "admin": nav_opts.append(L['admin'])
        page = st.radio(L['menu'], nav_opts)
        st.divider()
        with st.expander(L['install']):
            st.write("Android: ⋮ -> Add to Home Screen")
            st.write("iPhone: ⎙ -> Add to Home Screen")
        if st.button(L['logout']): st.session_state['logged_in'] = False; st.rerun()

    if page == L['engine']:
        st.title(L['title'])
        if st.button(L['btn_gen']):
            if user_data['credits'] > 0:
                with st.spinner(L['calibrating']):
                    st.balloons()
                    components.html("""<audio autoplay style="display:none;"><source src="https://www.soundjay.com/misc/sounds/cash-register-purchase-1.mp3" type="audio/mpeg"></audio>""", height=0)
                    new_bal = user_data['credits'] - 1
                    sheet.update_cell(user_data['row'], 4, new_bal)
                    
                    st.success(f"{L['generated']} {L['bal']}: {new_bal}")
                    
                    # 4D Data Scraping
                    r = requests.get("https://www.4dmoon.com/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    live = "".join(re.findall(r'\b\d{4}\b', BeautifulSoup(r.text, 'html.parser').get_text())[:120])
                    ranked = [d for d, _ in collections.Counter("80474206710328685044035084831805444041755938586455209168453600187307197177718803120963611044" + live).most_common()]
                    
                    st.markdown(f"### {L['lines_4d']}")
                    c4 = st.columns(2)
                    for i in range(10):
                        line = random.sample(ranked[:4], 3) + random.sample(ranked[4:8], 1)
                        random.shuffle(line); with c4[i%2]: st.metric(f"No.{i+1}", "".join(line))
            else: st.error("No Credits")

    elif page == L['account']:
        st.title(L['account'])
        st.info(f"{L['credits']}: {user_data['credits']}")
        st.divider()
        st.markdown(f"### {L['topup']}")
        st.link_button(L['buy_btn'], "https://buy.stripe.com/28E9AT5qh3oX9w0anIcbC02")
        st.caption(L['whatsapp'])

else: show_login_page()
st.caption("© 2026 HENG ONG HUAT ANALYTICS.")
