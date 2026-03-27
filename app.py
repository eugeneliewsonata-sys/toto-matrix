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
import urllib.parse

# --- APP CONFIG ---
st.set_page_config(page_title="HengOngHuat Pro", page_icon="📊", layout="centered")

# 1. LANGUAGE DICTIONARY
LANG_DICT = {
    "English": {
        "title": "HENG ONG HUAT PRO",
        "subtitle": "Professional Matrix Analytics",
        "login": "🔐 LOGIN", 
        "register": "📝 REGISTER",
        "phone_id": "USERNAME / ID", 
        "pass_login": "PASSWORD",
        "pass_reg": "CREATE NEW PASSWORD",
        "btn_login": "ENTER PORTAL", 
        "name": "USERNAME",
        "btn_reg": "CREATE ACCOUNT", 
        "vip": "VIP",
        "credits": "Credits", 
        "menu": "MENU",
        "engine": "Data Engine", 
        "calc": "Data Projections",
        "account": "My Account", 
        "admin": "Admin Panel",
        "vip_menu": "👑 VIP Exclusive",
        "btn_gen": "GENERATE DATA ANALYSIS", 
        "calibrating": "CALIBRATING DATA...",
        "generated": "Generated Successfully!", 
        "bal": "Balance",
        "lines_4d": "Structured Base Sequences", 
        "topup": "TOP UP CREDITS", 
        "tier1_btn": "💰 15 Credits (RM 10)",
        "tier2_btn": "💰 40 Credits (RM 20)",
        "tier3_btn": "💰 75 Credits (RM 30) 🔥 BEST",
        "whatsapp": "WhatsApp receipt to Admin to unlock.", 
        "logout": "LOGOUT",
        "prize_cat": "Data Category", 
        "big_bet": "Variable A (RM)",
        "small_bet": "Variable B (RM)", 
        "play_type": "Algorithm Mode",
        "calc_btn": "CALCULATE PROJECTION", 
        "total_won": "PROJECTED VALUE",
        "share_wa": "📲 SHARE TO WHATSAPP",
        "share_msg": "🔥 My HENG ONG HUAT Data Sequence today:\n",
        "wa_disclaimer": "⚠️ Disclaimer: This is a statistical projection.",
        "vip_title": "👑 VIP EXCLUSIVE SEQUENCES",
        "vip_desc": "Get the top 10 hand-picked data sequences with the highest mathematical probability.",
        "vip_buy": "💰 BUY 10 EXCLUSIVE SEQUENCES (RM 10)",
        "vip_pass": "Enter VIP Passcode from Admin:",
        "vip_btn_unlock": "UNLOCK SEQUENCES"
    },
    "中文": {
        "title": "兴旺发专业版",
        "subtitle": "专业矩阵分析平台",
        "login": "🔐 登录", 
        "register": "📝 注册账号",
        "phone_id": "用户名 / ID", 
        "pass_login": "密码",
        "pass_reg": "创建新密码",
        "btn_login": "进入系统", 
        "name": "用户名",
        "btn_reg": "立即注册", 
        "vip": "会员",
        "credits": "剩余积分", 
        "menu": "功能菜单",
        "engine": "数据引擎", 
        "calc": "数值预估",
        "account": "我的账户", 
        "admin": "管理后台",
        "vip_menu": "👑 VIP 独家序列",
        "btn_gen": "开始数据分析", 
        "calibrating": "正在校准数据...",
        "generated": "生成成功！", 
        "bal": "余额",
        "lines_4d": "结构化基础序列", 
        "topup": "充值积分", 
        "tier1_btn": "💰 15 积分 (RM 10)",
        "tier2_btn": "💰 40 积分 (RM 20)",
        "tier3_btn": "💰 75 积分 (RM 30) 🔥 超值",
        "whatsapp": "请发送收据给管理员进行解锁。", 
        "logout": "退出登录",
        "prize_cat": "数据类别", 
        "big_bet": "变量 A (RM)",
        "small_bet": "变量 B (RM)", 
        "play_type": "算法模式",
        "calc_btn": "计算预估值", 
        "total_won": "预计数值",
        "share_wa": "📲 发送至 WhatsApp",
        "share_msg": "🔥 我今天的兴旺发数据序列:\n",
        "wa_disclaimer": "⚠️ 免责声明：这仅是统计预测。",
        "vip_title": "👑 VIP 大师专属序列",
        "vip_desc": "获取10组经过最高数学概率筛选的独家矩阵序列。",
        "vip_buy": "💰 购买 10 组独家序列 (RM 10)",
        "vip_pass": "输入管理员提供的 VIP 密码:",
        "vip_btn_unlock": "解锁序列"
    }
}

# 2. CSS - RED LOGO & PROTECTION
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');
    
    .stApp { background-color: #ffffff !important; font-family: 'Montserrat', sans-serif !important; }
    
    .huat-logo {
        color: #FF0000 !important; font-weight: 900 !important; font-size: 2.5rem !important;
        text-align: center; margin-bottom: 10px;
    }

    [data-testid="stSidebarCollapsedControl"] svg, [data-testid="baseButton-headerNoPadding"] svg {
        fill: #000000 !important; width: 35px !important; height: 35px !important;
    }

    .stButton>button, a[data-testid="baseLinkButton"] {
        width: 100%; border-radius: 0px !important; height: 4em;
        background-color: #ffffff !important; color: #000000 !important;
        font-weight: 900 !important; border: 4px solid #000000 !important;
        display: flex; align-items: center; justify-content: center; text-decoration: none;
    }
    .stButton>button:hover, a[data-testid="baseLinkButton"]:hover { 
        background-color: #FF0000 !important; color: #ffffff !important; border-color: #FF0000 !important; 
    }
    
    [data-testid="stMetricValue"] { color: #FF0000 !important; font-weight: 900 !important; }
    .live-clock { text-align: right; font-weight: 700; color: #FF0000 !important; }
    .vip-box { background-color: #FFF0F0; border: 2px solid #FF0000; padding: 20px; border-radius: 10px; text-align: center;}
    .matrix-header { color: #000000; font-weight: 900; background-color: #FFD700; padding: 5px; border-radius: 5px; margin-top: 15px;}
    </style>
    """, unsafe_allow_html=True)

# 3. STATIC VAULT DATA
VAULT_4D = "804742067103286850440350848318054440417559385864552091684536001873071971777188031209636110449966266945671303607723893076690985985267993009839620435588576096605930401995893762878725360786668159018587024804533890424548553723587768971374574997571246806521958263911898855525249523"

# LIVE VAULT & VIP STATE
if 'live_vault_4d' not in st.session_state:
    st.session_state['live_vault_4d'] = VAULT_4D
if 'vip_numbers' not in st.session_state:
    st.session_state['vip_numbers'] = "8376\n8668\n1558\n8156\n3377\n6881\n6738\n7683\n3789\n1856"
if 'vip_passcode' not in st.session_state:
    st.session_state['vip_passcode'] = "HUAT88"

# 4. DATABASE
@st.cache_resource
def init_connection():
    try:
        creds_dict = json.loads(st.secrets["gcp_json"])
        scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)
        url = "https://docs.google.com/spreadsheets/d/1-tS2J7ud1Nu5swMo9kBPHWRtwYjH70lU1TQObnw3YWA/edit?gid=0#gid=0"
        return client.open_by_url(url).worksheet("Users")
    except Exception as e:
        return None

sheet = init_connection()

def get_database():
    if sheet is None:
        return {}
    records = sheet.get_all_records()
    db = {}
    for i, r in enumerate(records):
        phone = str(r['Phone'])
        db[phone] = {
            'code': str(r['Code']), 
            'name': str(r['Name']), 
            'credits': int(r['Credits']), 
            'row': i + 2
        }
    return db

def get_my_time():
    return datetime.utcnow() + timedelta(hours=8)

# 5. STATE
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'lang' not in st.session_state:
    st.session_state['lang'] = "English"

L = LANG_DICT[st.session_state['lang']]

# 6. UI
def show_login_page():
    now = get_my_time().strftime("%d %b %Y | %H:%M:%S")
    st.markdown(f'<p class="live-clock">{now}</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="huat-logo">HENG ONG HUAT</h1>', unsafe_allow_html=True)
    st.session_state['lang'] = st.sidebar.selectbox("Language / 语言", ["English", "中文"])
    
    db = get_database()
    t1, t2 = st.tabs([L['login'], L['register']])
    
    with t1:
        p = st.text_input(L['phone_id'], key="lp")
        c = st.text_input(L['pass_login'], type="password", key="lc")
        if st.button(L['btn_login']):
            clean_p = p.strip()
            clean_c = c.strip()
            
            found_user = None
            for db_phone, data in db.items():
                db_clean = str(db_phone).strip().lstrip("'").lstrip("0").lower()
                in_clean = clean_p.lstrip("'").lstrip("0").lower()
                
                if db_clean == in_clean:
                    found_user = db_phone
                    break
                    
            if found_user and str(db[found_user]['code']).strip() == clean_c:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = found_user
                st.rerun()
            else:
                st.error("Login Failed. Please check your details.")
                
    with t2:
        rn = st.text_input(L['name'])
        rp = st.text_input(L['phone_id'], key="rp")
        rc = st.text_input(L['pass_reg'], type="password", key="rc")
        if st.button(L['btn_reg']):
            if rn and rp and rc:
                clean_rp = rp.strip()
                
                user_exists = False
                for k in db.keys():
                    if str(k).strip().lstrip("'").lstrip("0").lower() == clean_rp.lstrip("0").lower():
                        user_exists = True
                        break
                
                if user_exists:
                    st.error("Account already exists.")
                else:
                    save_phone = f"'{clean_rp}" if clean_rp.isdigit() else clean_rp
                    sheet.append_row([save_phone, rc.strip(), rn.strip(), 0])
                    st.success("Registration Success! You can now log in.")

if st.session_state['logged_in']:
    db = get_database()
    user_id = st.session_state['current_user']
    if user_id not in db:
        st.session_state['logged_in'] = False
        st.rerun()
        
    user_data = db[user_id]
    st.markdown(f'<p class="live-clock">{get_my_time().strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<h1 style="color:red; font-size:25px; font-weight:900;">HENG ONG HUAT</h1>', unsafe_allow_html=True)
        st.session_state['lang'] = st.selectbox("Language", ["English", "中文"], index=0 if st.session_state['lang'] == "English" else 1)
        st.markdown(f"### {L['vip']}: {user_data['name']}")
        st.markdown(f"## {L['credits']}: **{user_data['credits']}**")
        st.divider()
        nav_opts = [L['engine'], L['vip_menu'], L['calc'], L['account']]
        if user_id == "admin":
            nav_opts.append(L['admin'])
        page = st.radio(L['menu'], nav_opts)
        st.divider()
        if st.button(L['logout']):
            st.session_state['logged_in'] = False
            st.rerun()

    if page == L['engine']:
        st.title(L['engine'])
        
        if user_data['credits'] <= 0:
            st.button(L['btn_gen'], disabled=True)
            st.error("⚠️ Insufficient Credits to generate analysis. Please top up below.")
            st.divider()
            st.markdown(f"### {L['topup']}")
            st.write("Select a package below to recharge. After payment, WhatsApp the receipt to Admin.")
            
            c_tier1, c_tier2, c_tier3 = st.columns(3)
            with c_tier1:
                st.link_button(L['tier1_btn'], "https://buy.stripe.com/28E9AT5qh3oX9w0anIcbC02")
            with c_tier2:
                st.link_button(L['tier2_btn'], "https://buy.stripe.com/5kQ00j3i95x55fKdzUcbC04")
            with c_tier3:
                st.link_button(L['tier3_btn'], "https://buy.stripe.com/3cI9AT05XgbJaA48fAcbC05")
                
        else:
            if st.button(L['btn_gen']):
                with st.spinner(L['calibrating']):
                    st.balloons()
                    
                    new_bal = user_data['credits'] - 1
                    sheet.update_cell(user_data['row'], 4, new_bal)
                    
                    try:
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            'Referer': 'https://www.google.com/',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                            'Sec-Fetch-Dest': 'document',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-Site': 'cross-site',
                            'Cache-Control': 'max-age=0'
                        }
                        resp = requests.get("https://www.4dmoon.com/", headers=headers, timeout=8)
                        resp.raise_for_status() 
                        live_nums = "".join(re.findall(r'\b\d{4}\b', BeautifulSoup(resp.text, 'html.parser').get_text())[:120])
                    except Exception as e:
                        live_nums = ""
                    
                    pool_4d = st.session_state['live_vault_4d'] + live_nums
                    counter = collections.Counter(pool_4d)
                    ranked_all = [d for d, _ in counter.most_common()]
                    
                    hot = ranked_all[:4]  
                    cold = ranked_all[-4:] 
                    
                    def gen_24i():
                        return "".join(random.sample(hot, 2) + random.sample(cold, 2))
                        
                    def gen_12i():
                        pair_d = random.choice(hot)
                        others = random.sample([d for d in hot+cold if d != pair_d], 2)
                        line = [pair_d, pair_d, others[0], others[1]]
                        random.shuffle(line)
                        return "".join(line)
                        
                    def gen_6i():
                        pairs = random.sample(hot + cold, 2)
                        line = [pairs[0], pairs[0], pairs[1], pairs[1]]
                        random.shuffle(line)
                        return "".join(line)
                        
                    def gen_4i():
                        triple = random.choice(hot)
                        single = random.choice(cold)
                        line = [triple, triple, triple, single]
                        random.shuffle(line)
                        return "".join(line)
                        
                    matrix = {"24i": set(), "12i": set(), "6i": set(), "4i": set()}
                    while len(matrix["24i"]) < 4: matrix["24i"].add(gen_24i())
                    while len(matrix["12i"]) < 3: matrix["12i"].add(gen_12i())
                    while len(matrix["6i"]) < 2: matrix["6i"].add(gen_6i())
                    while len(matrix["4i"]) < 1: matrix["4i"].add(gen_4i())
                    
                    st.success(f"{L['generated']} {L['bal']}: {new_bal}")
                    st.markdown(f"### {L['lines_4d']}")
                    
                    wa_text = f"{L['share_msg']}\n"
                    
                    st.markdown('<div class="matrix-header">Primary Cluster (A)</div>', unsafe_allow_html=True)
                    wa_text += "\n*Cluster A*\n"
                    cols = st.columns(4)
                    for i, num in enumerate(matrix["24i"]):
                        cols[i % 4].metric(label="", value=num)
                        wa_text += f"{num}\n"
                        
                    st.markdown('<div class="matrix-header">Secondary Cluster (B)</div>', unsafe_allow_html=True)
                    wa_text += "\n*Cluster B*\n"
                    cols = st.columns(3)
                    for i, num in enumerate(matrix["12i"]):
                        cols[i % 3].metric(label="", value=num)
                        wa_text += f"{num}\n"
                        
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown('<div class="matrix-header">Tertiary Cluster (C)</div>', unsafe_allow_html=True)
                        wa_text += "\n*Cluster C*\n"
                        for num in matrix["6i"]:
                            st.metric(label="", value=num)
                            wa_text += f"{num}\n"
                    with c2:
                        st.markdown('<div class="matrix-header">Quaternary Cluster (D)</div>', unsafe_allow_html=True)
                        wa_text += "\n*Cluster D*\n"
                        for num in matrix["4i"]:
                            st.metric(label="", value=num)
                            wa_text += f"{num}\n"

                    st.divider()
                    wa_text += f"\n{L['wa_disclaimer']}\nLet's HUAT together! 📊"
                    wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(wa_text)}"
                    st.link_button(L['share_wa'], wa_url)

    elif page == L['vip_menu']:
        st.title(L['vip_title'])
        st.write(L['vip_desc'])
        
        st.link_button(L['vip_buy'], "https://buy.stripe.com/dRmbJ1dWNcZxaA49jEcbC03")
        st.caption(L['whatsapp'])
        st.divider()
        
        st.markdown("### Unlock Sequences")
        vp_input = st.text_input(L['vip_pass'], type="password")
        if st.button(L['vip_btn_unlock']):
            if vp_input == st.session_state['vip_passcode']:
                st.balloons()
                st.success("VIP Unlocked Successfully!")
                
                v_nums = [n.strip() for n in st.session_state['vip_numbers'].split('\n') if n.strip()]
                st.markdown('<div class="vip-box">', unsafe_allow_html=True)
                cols = st.columns(2)
                for i, num in enumerate(v_nums):
                    with cols[i % 2]:
                        st.metric(label=f"VIP Sequence {i+1}", value=num, delta="Guaranteed Structure", delta_color="normal")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Invalid VIP Passcode.")

    elif page == L['calc']:
        st.title(L['calc'])
        c1, c2 = st.columns(2)
        with c1:
            prize_select = st.selectbox(L['prize_cat'], ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5"])
            play_type = st.selectbox(L['play_type'], ["Linear Sequence", "Matrix-24", "Matrix-12", "Matrix-6", "Matrix-4"])
        with c2:
            bet_big = st.number_input(L['big_bet'], min_value=0, value=1)
            bet_small = st.number_input(L['small_bet'], min_value=0, value=1)
            
        if st.button(L['calc_btn']):
            cat_a_vals = {"Category 1": 2500, "Category 2": 1000, "Category 3": 500, "Category 4": 180, "Category 5": 60}
            cat_b_vals = {"Category 1": 3500, "Category 2": 2000, "Category 3": 1000, "Category 4": 0, "Category 5": 0}
            
            val_a = bet_big * cat_a_vals[prize_select]
            val_b = bet_small * cat_b_vals[prize_select]
            
            if play_type == "Matrix-24":
                val_a = val_a / 24
                val_b = val_b / 24
            elif play_type == "Matrix-12":
                val_a = val_a / 12
                val_b = val_b / 12
            elif play_type == "Matrix-6":
                val_a = val_a / 6
                val_b = val_b / 6
            elif play_type == "Matrix-4":
                val_a = val_a / 4
                val_b = val_b / 4
                
            total_val = round(val_a + val_b, 2)
            if total_val > 0:
                st.balloons()
                st.success("🎉 PROJECTION COMPLETE! 🎉")
            st.metric(L['total_won'], f"RM {total_val:,.2f}")

    elif page == L['account']:
        st.title(L['account'])
        st.info(f"{L['credits']}: {user_data['credits']}")
        st.divider()
        st.markdown(f"### {L['topup']}")
        
        st.write("Select a package below. After payment, WhatsApp the receipt to Admin.")
        
        c_tier1, c_tier2, c_tier3 = st.columns(3)
        with c_tier1:
            st.link_button(L['tier1_btn'], "https://buy.stripe.com/28E9AT5qh3oX9w0anIcbC02")
        with c_tier2:
            st.link_button(L['tier2_btn'], "https://buy.stripe.com/5kQ00j3i95x55fKdzUcbC04")
        with c_tier3:
            st.link_button(L['tier3_btn'], "https://buy.stripe.com/3cI9AT05XgbJaA48fAcbC05")

    elif page == L['admin']:
        st.title("SYSTEM ADMIN")
        tab_users, tab_vault, tab_vip = st.tabs(["👥 Manage Users", "🧠 Data Vault", "👑 VIP Management"])
        
        with tab_users:
            tp = st.text_input("Phone ID")
            tc = st.number_input("Add Credits", value=15)
            if st.button("UPDATE CREDITS"):
                if tp in db:
                    sheet.update_cell(db[tp]['row'], 4, db[tp]['credits'] + tc)
                    st.success("Credits Updated!")
                else:
                    st.error("User Not Found")
            st.dataframe(db)
            
        with tab_vault:
            st.markdown("### 📥 Inject External Data Series")
            st.write("Paste raw data array below. The engine will automatically format and inject only the 4-digit sequences into the Live Matrix.")
            new_draw_data = st.text_area("Paste new data array here:")
            
            if st.button("UPDATE MATRIX BRAIN"):
                clean_nums = "".join(re.findall(r'\b\d{4}\b', new_draw_data))
                if clean_nums:
                    st.session_state['live_vault_4d'] += clean_nums
                    added_count = len(clean_nums) // 4
                    st.success(f"🔥 Successfully injected {added_count} new combinations into the Matrix!")
                else:
                    st.error("No valid sequences detected. Try again.")
                    
        with tab_vip:
            st.markdown("### 👑 Update VIP Sequences")
            new_vip_data = st.text_area("Enter 10 VIP Sequences (one per line):", st.session_state['vip_numbers'], height=250)
            new_passcode = st.text_input("Set VIP Passcode (Give this to users after they pay):", st.session_state['vip_passcode'])
            
            if st.button("SAVE VIP SETTINGS"):
                st.session_state['vip_numbers'] = new_vip_data
                st.session_state['vip_passcode'] = new_passcode
                st.success("VIP System successfully updated!")

else:
    show_login_page()
st.caption("© 2026 HENG ONG HUAT ANALYTICS.")
