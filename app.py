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

# --- APP CONFIG ---
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
        "lines_58": "6 Supreme 6/58 Matrix Lines", "lines_55": "6 Power 6/55 Matrix Lines",
        "lines_50": "6 Star 6/50 Matrix Lines", "topup": "TOP UP CREDITS",
        "buy_btn": "💰 BUY 50 CREDITS (RM 10)", "whatsapp": "WhatsApp receipt to Admin.",
        "install": "📲 INSTALL APP", "logout": "LOGOUT"
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
        "lines_58": "6组 Supreme 6/58 矩阵", "lines_55": "6组 Power 6/55 矩阵",
        "lines_50": "6组 Star 6/50 矩阵", "topup": "充值积分",
        "buy_btn": "💰 购买 50 积分 (RM 10)", "whatsapp": "请发送收据给管理员。",
        "install": "📲 安装至桌面", "logout": "退出登录"
    }
}

# 2. CSS - RED LOGO & ICON PROTECTION
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { background-color: #ffffff !important; font-family: 'Montserrat', sans-serif !important; }
    
    /* THE RED TEXT LOGO */
    .huat-logo {
        color: #FF0000 !important;
        font-weight: 900 !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 0px;
    }

    /* FIX SIDEBAR ICONS (Hamburger Menu) */
    [data-testid="stSidebarCollapsedControl"] svg, [data-testid="baseButton-headerNoPadding"] svg {
        fill: #000000 !important;
        width: 35px !important;
        height: 35px !important;
    }

    .stButton>button {
        width: 100%; border-radius: 0px !important; height: 4em;
        background-color: #ffffff !important; color: #000000 !important;
        font-weight: 900 !important; border: 4px solid #000000 !important;
    }
    .stButton>button:hover { background-color: #FF0000 !important; color: #ffffff !important; border-color: #FF0000 !important;}
    
    [data-testid="stMetricValue"] { color: #FF0000 !important; font-weight: 900 !important; }
    .live-clock { text-align: right; font-weight: 700; color: #FF0000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. VAULT DATA
VAULT_4D = "80474206710328685044035084831805444041755938586455209168453600187307197177718803120963611044"
VAULT_658 = [[18, 19, 29, 30, 36, 54], [2, 16, 20, 33, 34, 49], [8, 16, 22, 33, 53, 56], [4, 5, 13, 17, 22, 54], [7, 10, 18, 23, 26, 41], [26, 34, 39, 46, 47, 49], [5, 6, 15, 22, 40, 53], [4, 19, 29, 39, 50, 54]]
VAULT_655 = [[5, 12, 28, 33, 41, 52], [2, 18, 24, 39, 45, 55], [7, 14, 21, 30, 48, 51], [9, 13, 27, 35, 42, 53], [4, 11, 22, 36, 49, 54]]
VAULT_650 = [[6, 15, 22, 31, 40, 48], [1, 10, 19, 28, 37, 49], [8, 17, 26, 35, 44, 50], [3, 12, 21, 30, 39, 47], [5, 14, 23, 32, 41, 46]]

# 4. DATABASE
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

# 5. STATE
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'lang' not in st.session_state: st.session_state['lang'] = "English"
L = LANG_DICT[st.session_state['lang']]

# 6. UI
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
            # BALLOONS + SOUND
            st.balloons()
            components.html("""<audio autoplay><source src="https://www.soundjay.com/misc/sounds/cash-register-purchase-1.mp3"></audio>""", height=0)
            
            new_bal = user_data['credits'] - 1
            sheet.update_cell(user_data['row'], 4, new_bal)
            st.success(f"{L['generated']} {L['bal']}: {new_bal}")
            
            # LIVE DATA FOR 4D
            try:
                r = requests.get("https://www.4dmoon.com/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                live = "".join(re.findall(r'\b\d{4}\b', BeautifulSoup(r.text, 'html.parser').get_text())[:120])
            except: live = ""
            ranked = [d for d, _ in collections.Counter(VAULT_4D + live).most_common()]
            
            # 4D SECTION
            st.markdown(f"### {L['lines_4d']}")
            c4 = st.columns(2)
            for i in range(10):
                line = random.sample(ranked[:4], 3) + random.sample(ranked[4:8], 1)
                random.shuffle(line); with c4[i%2]: st.metric(f"No.{i+1}", "".join(line))
            
            # HELPERS FOR JACKPOTS
            def get_hot(v_list, count=12):
                all_n = [n for sub in v_list for n in sub]
                return [n for n, _ in collections.Counter(all_n).most_common(count)]

            # SUPREME 6/58
            st.divider(); st.markdown(f"### {L['lines_58']}")
            h58 = get_hot(VAULT_658); cs = st.columns(2)
            for i in range(6):
                with cs[i%2]: st.info(" ".join(f"{n:02d}" for n in sorted(random.sample(h58, 6))))

            # POWER 6/55
            st.divider(); st.markdown(f"### {L['lines_55']}")
            h55 = get_hot(VAULT_655); cp = st.columns(2)
            for i in range(6):
                with cp[i%2]: st.info(" ".join(f"{n:02d}" for n in sorted(random.sample(h55, 6))))

            # STAR 6/50
            st.divider(); st.markdown(f"### {L['lines_50']}")
            h50 = get_hot(VAULT_650); ct = st.columns(2)
            for i in range(6):
                with ct[i%2]: st.info(" ".join(f"{n:02d}" for n in sorted(random.sample(h50, 6))))

    elif page == L['account']:
        st.title(L['account'])
        st.link_button(L['buy_btn'], "https://buy.stripe.com/28E9AT5qh3oX9w0anIcbC02")

st.caption("© 2026 HENG ONG HUAT ANALYTICS.")
