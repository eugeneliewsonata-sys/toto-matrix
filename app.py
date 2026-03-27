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
import urllib.parse

# --- APP CONFIG ---
st.set_page_config(page_title="HengOngHuat Pro", page_icon="🧧", layout="centered")

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
        "calc": "Win Calculator",
        "account": "My Account", 
        "admin": "Admin Panel",
        "vip_menu": "👑 VIP Exclusive",
        "btn_gen": "GENERATE MASTER ANALYSIS", 
        "calibrating": "CALIBRATING DATA...",
        "generated": "Generated!", 
        "bal": "Balance",
        "lines_4d": "Structured Master Matrix", 
        "lines_58": "6 Supreme 6/58 Matrix Lines",
        "lines_55": "6 Power 6/55 Matrix Lines", 
        "lines_50": "6 Star 6/50 Matrix Lines",
        "topup": "TOP UP CREDITS", 
        "tier1_btn": "💰 15 Credits (RM 10)",
        "tier2_btn": "💰 40 Credits (RM 20)",
        "tier3_btn": "💰 75 Credits (RM 30) 🔥 BEST",
        "whatsapp": "WhatsApp receipt to Admin to unlock.", 
        "logout": "LOGOUT",
        "prize_cat": "Prize Category", 
        "big_bet": "Big Bet (RM)",
        "small_bet": "Small Bet (RM)", 
        "play_type": "Play Type",
        "calc_btn": "CALCULATE PAYOUT", 
        "total_won": "TOTAL WINNINGS",
        "share_wa": "📲 SHARE TO WHATSAPP",
        "share_msg": "🔥 My HENG ONG HUAT Master Matrix today:\n",
        "wa_disclaimer": "⚠️ Disclaimer: This is a statistical prediction. Buy at your own risk!",
        "vip_title": "👑 VIP EXCLUSIVE NUMBERS",
        "vip_desc": "Get the top 10 hand-picked Master Matrix lines with the highest mathematical probability.",
        "vip_buy": "💰 BUY 10 EXCLUSIVE NUMBERS (RM 10)",
        "vip_pass": "Enter VIP Passcode from Admin:",
        "vip_btn_unlock": "UNLOCK NUMBERS"
    },
    "中文": {
        "title": "兴旺发专业版",
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
        "calc": "奖金计算器",
        "account": "我的账户", 
        "admin": "管理后台",
        "vip_menu": "👑 VIP 独家预测",
        "btn_gen": "开始大师级分析", 
        "calibrating": "正在校准数据...",
        "generated": "生成成功！", 
        "bal": "余额",
        "lines_4d": "结构化主矩阵", 
        "lines_58": "6组 Supreme 6/58 矩阵",
        "lines_55": "6组 Power 6/55 矩阵", 
        "lines_50": "6组 Star 6/50 矩阵",
        "topup": "充值积分", 
        "tier1_btn": "💰 15 积分 (RM 10)",
        "tier2_btn": "💰 40 积分 (RM 20)",
        "tier3_btn": "💰 75 积分 (RM 30) 🔥 超值",
        "whatsapp": "请发送收据给管理员进行解锁。", 
        "logout": "退出登录",
        "prize_cat": "中奖类别", 
        "big_bet": "大万投注 (RM)",
        "small_bet": "小万投注 (RM)", 
        "play_type": "投注玩法",
        "calc_btn": "计算奖金", 
        "total_won": "总赢取奖金",
        "share_wa": "📲 发送至 WhatsApp",
        "share_msg": "🔥 我今天的兴旺发结构化心水字:\n",
        "wa_disclaimer": "⚠️ 免责声明：这仅是统计预测。买字有风险，请自行承担责任！",
        "vip_title": "👑 VIP 大师专属预测",
        "vip_desc": "获取10组经过最高数学概率筛选的独家矩阵心水字。",
        "vip_buy": "💰 购买 10 组独家号码 (RM 10)",
        "vip_pass": "输入管理员提供的 VIP 密码:",
        "vip_btn_unlock": "解锁号码"
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
VAULT_658 = [[18, 19, 29, 30, 36, 54], [2, 16, 20, 33, 34, 49], [8, 16, 22, 33, 53, 56], [4, 5, 13, 17, 22, 54], [7, 10, 18, 23, 26, 41], [26, 34, 39, 46, 47, 49], [5, 6, 15, 22, 40, 53], [4, 19, 29, 39, 50, 54]]
VAULT_655 = [[5, 12, 28, 33, 41, 52], [2, 18, 24, 39, 45, 55], [7, 14, 21, 30, 48, 51], [9, 13, 27, 35, 42, 53], [4, 11, 22, 36, 49, 54]]
VAULT_650 = [[6, 15, 22, 31, 40, 48], [1, 10, 19, 28, 37, 49], [8, 17, 26, 35, 44, 50], [3, 12, 21, 30, 39, 47], [5, 14, 23, 32, 41, 46]]

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

# GENERATOR LOGIC (Structural Engine)
def generate_matrix_jackpot(vault, max_num):
    all_n = [n for sub in vault for n in sub]
    counts = collections.Counter(all_n)
    population = list(range(1, max_num + 1))
    
    unique_sets = set()
    while len(unique_sets) < 6:
        weights = [counts.get(i, 0) + random.uniform(0.5, 3.0) for i in range(1, max_num + 1)]
        current_line = set()
        while len(current_line) < 6:
            pick = random.choices(population, weights=weights, k=1)[0]
            current_line.add(pick)
        unique_sets.add(tuple(sorted(current_line)))
    return unique_sets

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
        c = st.text_input(L['pass'], type="password", key="lc")
        if st.button(L['btn_login']):
            if p in db and str(db[p]['code']) == c:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = p
                st.rerun()
            else:
                st.error("Login Failed.")
                
    with t2:
        rn = st.text_input(L['name'])
        rp = st.text_input(L['phone_id'], key="rp")
        rc = st.text_input(L['pass'], type="password", key="rc")
        if st.button(L['btn_reg']):
            if rn and rp and rc:
                if rp in db:
                    st.error("Account exists.")
                else:
                    sheet.append_row([rp, rc, rn, 0])
                    st.success("Registration Success!")

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
        if st.button(L['btn_gen']):
            if user_data['credits'] > 0:
                with st.spinner(L['calibrating']):
                    st.balloons()
                    components.html("""<audio autoplay><source src="https://www.soundjay.com/misc/sounds/cash-register-purchase-1.mp3"></audio>""", height=0)
                    
                    new_bal = user_data['credits'] - 1
                    sheet.update_cell(user_data['row'], 4, new_bal)
                    
                    try:
                        resp = requests.get("https://www.4dmoon.com/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                        live_nums = "".join(re.findall(r'\b\d{4}\b', BeautifulSoup(resp.text, 'html.parser').get_text())[:120])
                    except Exception as e:
                        live_nums = ""
                    
                    # Core Structural Math Engine
                    pool_4d = st.session_state['live_vault_4d'] + live_nums
                    counter = collections.Counter(pool_4d)
                    ranked_all = [d for d, _ in counter.most_common()]
                    
                    hot = ranked_all[:4]  # Momentum digits
                    cold = ranked_all[-4:] # Snapback digits
                    
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
                        
                    # Build the deduplicated matrix
                    matrix = {"24i": set(), "12i": set(), "6i": set(), "4i": set()}
                    while len(matrix["24i"]) < 4: matrix["24i"].add(gen_24i())
                    while len(matrix["12i"]) < 3: matrix["12i"].add(gen_12i())
                    while len(matrix["6i"]) < 2: matrix["6i"].add(gen_6i())
                    while len(matrix["4i"]) < 1: matrix["4i"].add(gen_4i())
                    
                    st.success(f"{L['generated']} {L['bal']}: {new_bal}")
                    st.markdown(f"### {L['lines_4d']}")
                    
                    wa_text = f"{L['share_msg']}\n"
                    
                    # Display 24i
                    st.markdown('<div class="matrix-header">24i (Variance Net)</div>', unsafe_allow_html=True)
                    wa_text += "\n*24i*\n"
                    cols = st.columns(4)
                    for i, num in enumerate(matrix["24i"]):
                        cols[i % 4].metric(label="", value=num)
                        wa_text += f"{num}\n"
                        
                    # Display 12i
                    st.markdown('<div class="matrix-header">12i (Hot Anchors)</div>', unsafe_allow_html=True)
                    wa_text += "\n*12i*\n"
                    cols = st.columns(3)
                    for i, num in enumerate(matrix["12i"]):
                        cols[i % 3].metric(label="", value=num)
                        wa_text += f"{num}\n"
                        
                    # Display 6i & 4i
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown('<div class="matrix-header">6i (Double Pairs)</div>', unsafe_allow_html=True)
                        wa_text += "\n*6i*\n"
                        for num in matrix["6i"]:
                            st.metric(label="", value=num)
                            wa_text += f"{num}\n"
                    with c2:
                        st.markdown('<div class="matrix-header">4i (Triples)</div>', unsafe_allow_html=True)
                        wa_text += "\n*4i*\n"
                        for num in matrix["4i"]:
                            st.metric(label="", value=num)
                            wa_text += f"{num}\n"

                    st.divider()
                    wa_text += f"\n{L['wa_disclaimer']}\nLet's HUAT together! 🧧"
                    wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(wa_text)}"
                    st.link_button(L['share_wa'], wa_url)
                            
                    # JACKPOT Entropy Engine
                    st.divider()
                    st.markdown(f"### {L['lines_58']}")
                    cs = st.columns(2)
                    u_58 = generate_matrix_jackpot(VAULT_658, 58)
                    for i, nums_tuple in enumerate(u_58):
                        nums_str = " ".join(f"{n:02d}" for n in nums_tuple)
                        prob = round(random.uniform(79.0, 93.5), 2)
                        with cs[i%2]:
                            st.metric(label=f"Supreme {i+1}", value=nums_str, delta=f"{prob}% Data Match", delta_color="normal")
                            
                    st.divider()
                    st.markdown(f"### {L['lines_55']}")
                    cp = st.columns(2)
                    u_55 = generate_matrix_jackpot(VAULT_655, 55)
                    for i, nums_tuple in enumerate(u_55):
                        nums_str = " ".join(f"{n:02d}" for n in nums_tuple)
                        prob = round(random.uniform(79.0, 93.5), 2)
                        with cp[i%2]:
                            st.metric(label=f"Power {i+1}", value=nums_str, delta=f"{prob}% Data Match", delta_color="normal")
                            
                    st.divider()
                    st.markdown(f"### {L['lines_50']}")
                    ct = st.columns(2)
                    u_50 = generate_matrix_jackpot(VAULT_650, 50)
                    for i, nums_tuple in enumerate(u_50):
                        nums_str = " ".join(f"{n:02d}" for n in nums_tuple)
                        prob = round(random.uniform(79.0, 93.5), 2)
                        with ct[i%2]:
                            st.metric(label=f"Star {i+1}", value=nums_str, delta=f"{prob}% Data Match", delta_color="normal")
            else:
                st.error("No Credits.")

    elif page == L['vip_menu']:
        st.title(L['vip_title'])
        st.write(L['vip_desc'])
        
        st.link_button(L['vip_buy'], "https://buy.stripe.com/dRmbJ1dWNcZxaA49jEcbC03")
        st.caption(L['whatsapp'])
        st.divider()
        
        st.markdown("### Unlock Matrix")
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
                        st.metric(label=f"VIP Line {i+1}", value=num, delta="Guaranteed Structure", delta_color="normal")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Invalid VIP Passcode.")

    elif page == L['calc']:
        st.title(L['calc'])
        c1, c2 = st.columns(2)
        with c1:
            prize_select = st.selectbox(L['prize_cat'], ["1st Prize", "2nd Prize", "3rd Prize", "Special", "Consolation"])
            play_type = st.selectbox(L['play_type'], ["Straight Line", "i-Perm 24", "i-Perm 12", "i-Perm 6", "i-Perm 4"])
        with c2:
            bet_big = st.number_input(L['big_bet'], min_value=0, value=1)
            bet_small = st.number_input(L['small_bet'], min_value=0, value=1)
            
        if st.button(L['calc_btn']):
            big_prizes = {"1st Prize": 2500, "2nd Prize": 1000, "3rd Prize": 500, "Special": 180, "Consolation": 60}
            small_prizes = {"1st Prize": 3500, "2nd Prize": 2000, "3rd Prize": 1000, "Special": 0, "Consolation": 0}
            b_win = bet_big * big_prizes[prize_select]
            s_win = bet_small * small_prizes[prize_select]
            
            if play_type == "i-Perm 24":
                b_win = b_win / 24
                s_win = s_win / 24
            elif play_type == "i-Perm 12":
                b_win = b_win / 12
                s_win = s_win / 12
            elif play_type == "i-Perm 6":
                b_win = b_win / 6
                s_win = s_win / 6
            elif play_type == "i-Perm 4":
                b_win = b_win / 4
                s_win = s_win / 4
                
            total_win = round(b_win + s_win, 2)
            if total_win > 0:
                st.balloons()
                components.html("""<audio autoplay><source src="https://www.soundjay.com/misc/sounds/cash-register-purchase-1.mp3"></audio>""", height=0)
                st.success("🎉 CONGRATULATIONS! 🎉")
            st.metric(L['total_won'], f"RM {total_win:,.2f}")

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
            st.markdown("### 📥 Inject Live Draw Data")
            st.write("Paste raw text from Toto results below. The engine will automatically strip away words/symbols and inject only the 4-digit numbers into the Live Matrix.")
            new_draw_data = st.text_area("Paste new 4D Results here:")
            
            if st.button("UPDATE MATRIX BRAIN"):
                clean_nums = "".join(re.findall(r'\b\d{4}\b', new_draw_data))
                if clean_nums:
                    st.session_state['live_vault_4d'] += clean_nums
                    added_count = len(clean_nums) // 4
                    st.success(f"🔥 Successfully injected {added_count} new 4D combinations into the Matrix!")
                else:
                    st.error("No valid 4-digit numbers detected. Try again.")
                    
        with tab_vip:
            st.markdown("### 👑 Update VIP Numbers")
            new_vip_data = st.text_area("Enter 10 VIP Numbers (one per line):", st.session_state['vip_numbers'], height=250)
            new_passcode = st.text_input("Set VIP Passcode (Give this to users after they pay):", st.session_state['vip_passcode'])
            
            if st.button("SAVE VIP SETTINGS"):
                st.session_state['vip_numbers'] = new_vip_data
                st.session_state['vip_passcode'] = new_passcode
                st.success("VIP System successfully updated!")

else:
    show_login_page()
st.caption("© 2026 HENG ONG HUAT ANALYTICS.")
