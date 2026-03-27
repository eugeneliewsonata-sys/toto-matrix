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
        "phone_id": "PHONE ID / USERNAME", 
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
        "phone_id": "手机号码 / 用户名", 
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
        scopes = ["https://www
