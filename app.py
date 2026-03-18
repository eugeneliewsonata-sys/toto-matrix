import streamlit as st
import collections
import random
import re

# 1. Setup the Webpage Style
st.set_page_config(page_title="Eugene's Toto Matrix", page_icon="🎰", layout="centered")

st.title("🎰 Eugene's Master Matrix")
st.markdown("Feed the engine with the latest results to generate highly calibrated i-Perm and Lotto lines.")

st.divider()

# 2. Build the Input Boxes (Pre-loaded with ALL historical data)
st.subheader("📊 1. Input Latest 4D Results")
# Complete March 18 board
default_4d = "8047, 4206, 7103, 2868, 5044, 0350, 8483, 1805, 4440, 4175, 5938, 5864, 5520, 9168, 4536, 0018, 7307, 1971, 7771, 8803, 1209, 6361, 1044"
input_4d = st.text_area("Paste the latest 4D numbers (separated by commas):", value=default_4d, height=100)

st.subheader("🎱 2. Input Latest Supreme 6/58 Results")
# All 8 draws from Feb 25 to Mar 15
default_lotto = """18 19 29 30 36 54
2 16 20 33 34 49
8 16 22 33 53 56
4 5 13 17 22 54
7 10 18 23 26 41
26 34 39 46 47 49
5 6 15 22 40 53
4 19 29 39 50 54"""
input_lotto = st.text_area("Paste the latest Lotto lines (one draw per line, separated by spaces):", value=default_lotto, height=200)

# 3. The Big Generate Button
if st.button("🚀 GENERATE MASTER TICKETS", type="primary"):
    
    with st.spinner("Calibrating the Matrix..."):
        
        # --- Process 4D Data ---
        draws_4d = re.findall(r'\b\d{4}\b', input_4d)
        all_digits = "".join(draws_4d)
        
        if not all_digits:
            st.error("Please enter valid 4D numbers.")
        else:
            digit_counts = collections.Counter(all_digits)
            hot_digits = [digit for digit, _ in digit_counts.most_common(4)]
            cold_digits = [digit for digit, _ in reversed(digit_counts.most_common(3))]
            
            st.success("Matrix Calibrated Successfully!")
            
            st.subheader("🎫 4D i-Perm Master Lines")
            st.caption("Strategy: 3 Hot Digits + 1 Cold Digit (Scrambled)")
            
            for i in range(5):
                line = random.sample(hot_digits, 3) + random.sample(cold_digits, 1)
                random.shuffle(line)
                st.code("".join(line), language="text")

        # --- Process Lotto Data ---
        lotto_lines = input_lotto.strip().split('\n')
        all_balls = []
        for line in lotto_lines:
            balls = [int(b) for b in re.findall(r'\b\d{1,2}\b', line)]
            all_balls.extend(balls)
            
        if not all_balls:
            st.error("Please enter valid Lotto numbers.")
        else:
            ball_counts = collections.Counter(all_balls)
            # Expanding to top 12 hot balls for a wider net since we have 8 draws of data
            hot_balls = [ball for ball, _ in ball_counts.most_common(12)]
            
            st.subheader("🔴 Supreme 6/58 Hot Lines")
            st.caption("Strategy: Pure momentum using the Top 12 hottest balls")
            
            for i in range(3):
                line = sorted(random.sample(hot_balls, 6))
                formatted_line = "  ".join(f"{n:02d}" for n in line)
                st.code(formatted_line, language="text")
