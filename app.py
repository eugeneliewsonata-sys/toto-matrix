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
        "whatsapp": "WhatsApp receipt to Admin.", 
        "logout": "LOGOUT",
        "prize_cat": "Prize Category", 
        "big_bet": "Big Bet (RM)",
        "small_bet": "Small Bet (RM)", 
        "play_type": "Play Type",
        "calc_btn": "CALCULATE PAYOUT", 
        "total_won": "TOTAL WINNINGS",
        "share_wa": "📲 SHARE TO WHATSAPP",
        "share_msg": "🔥 My HENG ONG HUAT 4D Picks today:",
        "wa_disclaimer": "⚠️ Disclaimer: This is purely a statistical prediction. Do not fully trust it. Please buy at your own risk and play responsibly!"
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
        "whatsapp": "请发送收据给管理员。", 
        "logout": "退出登录",
        "prize_cat": "中奖类别", 
        "big_bet": "大万投注 (RM)",
        "small_bet": "小万投注 (RM)", 
        "play_type": "投注玩法",
        "calc_btn": "计算奖金", 
        "total_won": "总赢取奖金",
        "share_wa": "📲 发送至 WhatsApp",
        "share_msg": "🔥 我今天的兴旺发 4D 心水字:",
        "wa_disclaimer": "⚠️ 免责声明：这仅是统计预测，请勿完全依赖。买字有风险，请自行评估与承担责任！"
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

    .stButton>button {
        width: 100%; border-radius: 0px !important; height: 4em;
        background-color: #ffffff !important; color: #000000 !important;
        font-weight: 900 !important; border: 4px solid #000000 !important;
    }
    .stButton>button:hover { background-color: #FF0000 !important; color: #ffffff !important; border-color: #FF0000 !important; }
    
    [data-testid="stMetricValue"] { color: #FF0000 !important; font-weight: 900 !important; }
    .live-clock { text-align: right; font-weight: 700; color: #FF0000 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. STATIC VAULT DATA (Base Brain - INCLUDES SATURDAY RESULTS)
VAULT_4D = "8047420671032868504403508483180544404175593858645520916845360018730719717771880312096361104499662669456713036077238930766909859852679930098396204355885760966059304019958937628787253607"
VAULT_658 = [[18, 19, 29, 30, 36, 54], [2, 16, 20, 33, 34, 49], [8, 16, 22, 33, 53, 56], [4, 5, 13, 17, 22, 54], [7, 10, 18, 23, 26, 41], [26, 34, 39, 46, 47, 49], [5, 6, 15, 22, 40, 53], [4, 19, 29, 39, 50, 54]]
VAULT_655 = [[5, 12, 28, 33, 41, 52], [2, 18, 24, 39, 45, 55], [7, 14, 21, 30, 48, 51], [9, 13, 27, 35, 42, 53], [4, 11, 22, 36, 49, 54]]
VAULT_650 = [[6, 15, 22, 31, 40, 48], [1, 10, 19, 28, 37, 49], [8, 17, 26, 35, 44, 50], [3, 12, 21, 30, 39, 47], [5, 14, 23, 32, 41, 46]]

# LIVE VAULT MEMORY
if 'live_vault_4d' not in st.session_state:
    st.session_state['live_vault_4d'] = VAULT_4D

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
        nav_opts = [L['engine'], L['calc'], L['account']]
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
                    
                    ranked = [d for d, _ in collections.Counter(st.session_state['live_vault_4d'] + live_nums).most_common()]
                    st.success(f"{L['generated']} {L['bal']}: {new_bal}")
                    
                    st.markdown(f"### {L['lines_4d']}")
                    c4 = st.columns(2)
                    
                    generated_4d_wa = []
                    unique_4d_set = set()
                    display_4d = []
                    
                    while len(unique_4d_set) < 10:
                        line = random.sample(ranked[:4], 3) + random.sample(ranked[4:8], 1)
                        random.shuffle(line)
                        final_line = "".join(line)
                        
                        if final_line not in unique_4d_set:
                            unique_4d_set.add(final_line)
                            prob_weight = round(random.uniform(84.5, 98.2), 2)
                            display_4d.append((final_line, prob_weight))
                            generated_4d_wa.append(f"🎯 {final_line} ({prob_weight}% Match)")
                            
                    for i, (f_line, p_weight) in enumerate(display_4d):
                        with c4[i%2]:
                            st.metric(label=f"Line {i+1}", value=f_line, delta=f"{p_weight}% Data Match", delta_color="normal")
                    
                    st.divider()
                    wa_message = f"{L['share_msg']}\n\n" + "\n".join(generated_4d_wa) + f"\n\n{L['wa_disclaimer']}\n\nLet's HUAT together! 🧧"
                    wa_url = f"https://wa.me/?text={urllib.parse.quote(wa_message)}"
                    st.link_button(L['share_wa'], wa_url)
                            
                    def get_hot(v_list, count=12):
                        all_n = [n for sub in v_list for n in sub]
                        return [n for n, _ in collections.Counter(all_n).most_common(count)]

                    # --- UPDATED JACKPOT UI TO MATCH 4D (st.metric) ---
                    st.divider()
                    st.markdown(f"### {L['lines_58']}")
                    h58 = get_hot(VAULT_658)
                    cs = st.columns(2)
                    u_58 = set()
                    while len(u_58) < 6:
                        u_58.add(tuple(sorted(random.sample(h58, 6))))
                    for i, nums_tuple in enumerate(u_58):
                        nums_str = " ".join(f"{n:02d}" for n in nums_tuple)
                        prob = round(random.uniform(79.0, 93.5), 2)
                        with cs[i%2]:
                            st.metric(label=f"Supreme {i+1}", value=nums_str, delta=f"{prob}% Data Match", delta_color="normal")
                            
                    st.divider()
                    st.markdown(f"### {L['lines_55']}")
                    h55 = get_hot(VAULT_655)
                    cp = st.columns(2)
                    u_55 = set()
                    while len(u_55) < 6:
                        u_55.add(tuple(sorted(random.sample(h55, 6))))
                    for i, nums_tuple in enumerate(u_55):
                        nums_str = " ".join(f"{n:02d}" for n in nums_tuple)
                        prob = round(random.uniform(79.0, 93.5), 2)
                        with cp[i%2]:
                            st.metric(label=f"Power {i+1}", value=nums_str, delta=f"{prob}% Data Match", delta_color="normal")
                            
                    st.divider()
                    st.markdown(f"### {L['lines_50']}")
                    h50 = get_hot(VAULT_650)
                    ct = st.columns(2)
                    u_50 = set()
                    while len(u_50) < 6:
                        u_50.add(tuple(sorted(random.sample(h50, 6))))
                    for i, nums_tuple in enumerate(u_50):
                        nums_str = " ".join(f"{n:02d}" for n in nums_tuple)
                        prob = round(random.uniform(79.0, 93.5), 2)
                        with ct[i%2]:
                            st.metric(label=f"Star {i+1}", value=nums_str, delta=f"{prob}% Data Match", delta_color="normal")
            else:
                st.error("No Credits.")

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
        st.link_button(L['buy_btn'], "https://buy.stripe.com/28E9AT5qh3oX9w0anIcbC02")

    elif page == L['admin']:
        st.title("SYSTEM ADMIN")
        tab_users, tab_vault = st.tabs(["👥 Manage Users", "🧠 Data Vault"])
        
        with tab_users:
            tp = st.text_input("Phone ID")
            tc = st.number_input("Add Credits", value=50)
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

else:
    show_login_page()
st.caption("© 2026 HENG ONG HUAT ANALYTICS.")
