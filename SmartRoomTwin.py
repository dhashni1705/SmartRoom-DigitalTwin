import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time, random

st.set_page_config(page_title="Smart Room", page_icon="💡", layout="wide")

if "chart_data" not in st.session_state:
    st.session_state.chart_data = pd.DataFrame(columns=["Time", "Temperature", "Humidity"])
if "light_status" not in st.session_state:
    st.session_state.light_status = "OFF"
if "temperature" not in st.session_state:
    st.session_state.temperature = 25
if "humidity" not in st.session_state:
    st.session_state.humidity = 50

st.title("💡 Smart Room Digital Twin Dashboard")

# Sidebar controls
st.session_state.light_status = st.sidebar.selectbox(
    "💡 Light State", ["OFF", "ON"], 
    index=0 if st.session_state.light_status=="OFF" else 1
)
temp_control = st.sidebar.slider("🌡 Desired Temperature", 16, 30, 24)

placeholder = st.empty()

while True:
    # Smooth random change
    st.session_state.temperature += random.choice([-1, 0, 1])
    st.session_state.humidity += random.choice([-2, -1, 0, 1, 2])

    st.session_state.temperature = max(18, min(32, st.session_state.temperature))
    st.session_state.humidity = max(35, min(75, st.session_state.humidity))

    temperature = st.session_state.temperature
    humidity = st.session_state.humidity
    current_time = datetime.now().strftime("%H:%M:%S")

    new_row = pd.DataFrame({"Time": [current_time], "Temperature": [temperature], "Humidity": [humidity]})
    st.session_state.chart_data = pd.concat([st.session_state.chart_data, new_row], ignore_index=True)

    with placeholder.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡 Temperature", f"{temperature}°C")
        col2.metric("💧 Humidity", f"{humidity}%")
        col3.metric("💡 Light", st.session_state.light_status)

        fig = px.line(st.session_state.chart_data, x="Time", y=["Temperature", "Humidity"],
                      title="Real-Time Room Conditions", markers=True)
        fig.update_layout(yaxis=dict(range=[15, 80]))
        st.plotly_chart(fig, use_container_width=True)

    time.sleep(2)
