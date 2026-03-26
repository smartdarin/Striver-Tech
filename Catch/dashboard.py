import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

st.set_page_config(page_title="AI Crowd Dashboard", layout="centered")

st.title("🚀 AI Crowd Intelligence Dashboard")

# 🔥 AUTO REFRESH
placeholder = st.empty()

while True:
    with placeholder.container():

        # ----------------------------
        # 🔹 LOAD DATA
        # ----------------------------
        try:
            df = pd.read_csv("crowd_data.csv")
        except:
            st.error("❌ Run main system first!")
            st.stop()

        if len(df) < 5:
            st.warning("Waiting for data...")
            time.sleep(2)
            continue

        # ----------------------------
        # 🔹 SMOOTH DATA
        # ----------------------------
        df["smooth"] = df["count"].rolling(window=5).mean()

        current = int(df["count"].iloc[-1])
        avg = int(df["count"].mean())
        peak = int(df["count"].max())

        # ----------------------------
        # 🔹 TREND
        # ----------------------------
        trend = np.polyfit(range(len(df)), df["count"], 1)[0]

        # ----------------------------
        # 📊 GRAPH
        # ----------------------------
        st.subheader("📊 Crowd Trend")

        fig, ax = plt.subplots()
        ax.plot(df["time"], df["count"], label="Raw Crowd")
        ax.plot(df["time"], df["smooth"], label="Smoothed", linewidth=3)

        ax.set_xlabel("Time")
        ax.set_ylabel("People")
        ax.legend()

        st.pyplot(fig)

        # ----------------------------
        # 📌 STATS
        # ----------------------------
        st.subheader("📌 Stats")

        col1, col2, col3 = st.columns(3)
        col1.metric("Current", current)
        col2.metric("Average", avg)
        col3.metric("Peak", peak)

        # ----------------------------
        # 🧠 AI INSIGHT
        # ----------------------------
        st.subheader("🧠 AI Insight")

        recent = df["count"].tail(10).values
        change = recent[-1] - recent[0]
        volatility = np.std(recent)

        if volatility > 10:
            st.error("🚨 UNSTABLE CROWD")

        elif change > 15:
            st.warning("📈 CROWD SURGE")

        elif change < -15:
            st.warning("📉 CROWD DROP")

        elif current > peak * 0.85:
            st.error("🚨 HIGH DENSITY")

        else:
            st.success("✅ STABLE FLOW")

        # ----------------------------
        # 🔥 RISK LEVEL (NEW 🔥)
        # ----------------------------
        st.subheader("⚠️ Risk Level")

        risk = current / peak

        if risk > 0.9:
            st.error("🔴 CRITICAL")

        elif risk > 0.7:
            st.warning("🟠 HIGH")

        elif risk > 0.5:
            st.info("🟡 MODERATE")

        else:
            st.success("🟢 LOW")

        # ----------------------------
        # 🔮 FUTURE
        # ----------------------------
        future = int(current + trend * 5)

       # ----------------------------
# 🚑 RESPONSE SYSTEM (NEW 🔥)
# ----------------------------
        st.subheader("🚑 Emergency Response System")

    if current > peak * 0.9:
        st.error("🚨 CRITICAL ALERT SENT")

        st.write("📡 Alert sent to:")
        st.write("• 🚓 Police Control Room")
        st.write("• 🚑 Emergency Medical Services")
        st.write("• 🏥 Nearby Hospitals")

    elif current > peak * 0.7:
        st.warning("⚠️ PREVENTIVE ACTION TRIGGERED")

        st.write("📡 Notified:")
        st.write("• 🚓 Local Security Teams")
        st.write("• 🚑 Standby Ambulance Units")

    elif trend > 2:
        st.info("📈 Crowd Increase Monitoring Active")

        st.write("📡 Monitoring team alerted for possible surge")

    else:
        st.success("✅ Situation Under Control")

        st.write("📡 No emergency action required")

    time.sleep(2)
    