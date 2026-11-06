import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from datetime import date, time, datetime, timedelta
from pathlib import Path

st.set_page_config(
    page_title="Personal Commute Intelligence",
    page_icon="🚗",
    layout="wide"
)

ROOT = Path(__file__).parent
MODEL_PATH = ROOT / "commute_time_model.joblib"
DATA_PATH = ROOT / "Personal_Commute_Time_Prediction_Synthetic_Dataset.xlsx"

st.markdown("""
<style>
    .main {background-color: #0e1117;}
    [data-testid="stMetric"] {
        background: #171b24; padding: 14px; border-radius: 10px;
        border: 1px solid #303642;
    }
    .hero {
        padding: 22px 24px; border-radius: 14px;
        background: linear-gradient(115deg, #171b24, #25202a);
        border: 1px solid #6b2632; margin-bottom: 18px;
    }
    .hero h1 {margin: 0; color: #f4f4f5;}
    .hero p {color: #b9bec9; margin: 6px 0 0 0;}
    .warning-note {
        border-left: 4px solid #f59e0b; padding: 10px 14px;
        background: #282318; border-radius: 5px; color: #f4e7c6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_artifact():
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_data():
    return pd.read_excel(DATA_PATH, sheet_name="Commute_Data")

def add_features(frame):
    out = frame.copy()
    out["departure_minutes"] = out["Departure_Time"].apply(lambda t: t.hour * 60 + t.minute)
    out["departure_hour"] = out["Departure_Time"].apply(lambda t: t.hour)
    out["departure_minute"] = out["Departure_Time"].apply(lambda t: t.minute)
    out["day_of_week"] = out["Date"].dt.dayofweek
    out["month"] = out["Date"].dt.month
    out["is_saturday"] = (out["day_of_week"] == 5).astype(int)
    out["is_morning_peak"] = out["departure_minutes"].between(465, 525).astype(int)
    return out

def fmt_time(t):
    return t.strftime("%I:%M %p")

st.markdown("""
<div class="hero">
  <h1>COMMUTE INTELLIGENCE</h1>
  <p>CHEThICODE &nbsp;→&nbsp; KNOVISTA TECHNOLOGIES, KADAVANTHRA JUNCTION</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="warning-note"><b>Prototype / synthetic data:</b> '
    'The 100 trips and their weather/traffic labels are simulated. '
    'Predictions and charts demonstrate the workflow; they are not verified '
    'historical commute conditions or real-world accuracy.</div>',
    unsafe_allow_html=True
)

try:
    artifact = load_artifact()
    model = artifact["model"]
    feature_columns = artifact["feature_columns"]
    history = load_data()
except Exception as exc:
    st.error(f"Could not load the model or dataset: {exc}")
    st.info("Keep the model and Excel workbook beside app.py. Install the pinned requirements.txt.")
    st.stop()

prediction_tab, analytics_tab, compare_tab, about_tab = st.tabs([
    "🚦 Prediction", "📊 Commute Analytics", "🕒 Departure Comparison", "ℹ️ Model Details"
])

with prediction_tab:
    st.subheader("Estimate your journey")
    c1, c2 = st.columns(2)
    with c1:
        travel_date = st.date_input("Travel date", value=date.today(), key="pred_date")
        departure_time = st.time_input("Departure time", value=time(8, 10), key="pred_time")
    with c2:
        weather = st.selectbox("Weather", ["Clear", "Cloudy", "Rainy"], key="pred_weather")
        traffic = st.selectbox("Expected traffic", ["Low", "Moderate", "Heavy"], key="pred_traffic")

    if st.button("Predict commute", type="primary", use_container_width=True):
        row = pd.DataFrame([{
            "Date": pd.Timestamp(travel_date),
            "Departure_Time": departure_time,
            "Weather": weather,
            "Traffic": traffic
        }])
        row = add_features(row)
        duration = max(1.0, float(model.predict(row[feature_columns])[0]))
        arrival = datetime.combine(travel_date, departure_time) + timedelta(minutes=duration)

        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Estimated duration", f"{duration:.1f} min")
        m2.metric("Estimated arrival", fmt_time(arrival))
        m3.metric("Departure", fmt_time(departure_time))
        st.caption(f"Scenario: {travel_date:%d %b %Y} · {weather} · {traffic} traffic")
        st.info("Illustrative model output only. Do not use it as a reliable real-world travel estimate.")

with analytics_tab:
    st.subheader("Historical pattern explorer")
    st.caption("All charts below summarize the simulated workbook.")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Simulated trips", f"{len(history):,}")
    k2.metric("Average duration", f"{history['Travel_Duration_Min'].mean():.1f} min")
    k3.metric("Shortest trip", f"{history['Travel_Duration_Min'].min():.0f} min")
    k4.metric("Longest trip", f"{history['Travel_Duration_Min'].max():.0f} min")

    chart_left, chart_right = st.columns(2)
    with chart_left:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(history["Travel_Duration_Min"], bins=12, edgecolor="white")
        ax.set_title("Distribution of trip duration")
        ax.set_xlabel("Minutes")
        ax.set_ylabel("Trips")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with chart_right:
        traffic_order = ["Low", "Moderate", "Heavy"]
        traffic_avg = history.groupby("Traffic")["Travel_Duration_Min"].mean().reindex(traffic_order)
        fig, ax = plt.subplots(figsize=(7, 4))
        traffic_avg.plot(kind="bar", ax=ax)
        ax.set_title("Average duration by traffic label")
        ax.set_ylabel("Minutes")
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=0)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    weather_order = ["Clear", "Cloudy", "Rainy"]
    weather_avg = history.groupby("Weather")["Travel_Duration_Min"].mean().reindex(weather_order)
    fig, ax = plt.subplots(figsize=(9, 3.8))
    weather_avg.plot(kind="bar", ax=ax)
    ax.set_title("Average duration by weather label")
    ax.set_ylabel("Minutes")
    ax.set_xlabel("")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    history["Date"] = pd.to_datetime(history["Date"])
    daily = history.groupby("Date", as_index=False)["Travel_Duration_Min"].mean()
    fig, ax = plt.subplots(figsize=(11, 3.8))
    ax.plot(daily["Date"], daily["Travel_Duration_Min"], marker=".", linewidth=1.5)
    ax.set_title("Simulated commute duration over time")
    ax.set_ylabel("Minutes")
    ax.set_xlabel("Date")
    fig.autofmt_xdate()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("View simulated trip records"):
        st.dataframe(history, use_container_width=True, hide_index=True)

with compare_tab:
    st.subheader("Compare possible departure times")
    st.caption("Compare model outputs under the same selected date, weather and traffic. This is not a live traffic forecast.")
    compare_date = st.date_input("Date for comparison", value=date.today(), key="cmp_date")
    cc1, cc2 = st.columns(2)
    with cc1:
        compare_weather = st.selectbox("Weather condition", ["Clear", "Cloudy", "Rainy"], key="cmp_weather")
    with cc2:
        compare_traffic = st.selectbox("Traffic condition", ["Low", "Moderate", "Heavy"], key="cmp_traffic")

    slots = [time(7, 0), time(7, 15), time(7, 30), time(7, 45),
             time(8, 0), time(8, 15), time(8, 30), time(8, 45),
             time(9, 0), time(9, 15)]
    scenarios = pd.DataFrame([{
        "Date": pd.Timestamp(compare_date),
        "Departure_Time": slot,
        "Weather": compare_weather,
        "Traffic": compare_traffic
    } for slot in slots])
    scenarios = add_features(scenarios)
    scenarios["Predicted_Duration_Min"] = model.predict(scenarios[feature_columns])
    scenarios["Estimated_Arrival"] = scenarios.apply(
        lambda r: (
            datetime.combine(compare_date, r["Departure_Time"])
            + timedelta(minutes=float(r["Predicted_Duration_Min"]))
        ).strftime("%I:%M %p"),
        axis=1
    )
    scenarios["Departure"] = scenarios["Departure_Time"].apply(fmt_time)
    scenarios["Predicted_Duration_Min"] = scenarios["Predicted_Duration_Min"].round(1)

    st.dataframe(
        scenarios[["Departure", "Predicted_Duration_Min", "Estimated_Arrival"]]
        .rename(columns={
            "Departure": "Departure time",
            "Predicted_Duration_Min": "Predicted duration (min)",
            "Estimated_Arrival": "Estimated arrival"
        }),
        use_container_width=True,
        hide_index=True
    )
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.plot(scenarios["Departure"], scenarios["Predicted_Duration_Min"], marker="o")
    ax.set_title("Predicted duration by departure slot")
    ax.set_ylabel("Minutes")
    ax.set_xlabel("Departure")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with about_tab:
    st.subheader("Model and dataset information")
    st.write("**Selected model:**", artifact.get("model_name", "Saved regression model"))
    st.write("**Route context:** Chethicode → Knovista Technologies, Kadavanthra Junction.")
    st.write("**Dataset:** 100 simulated trips, July–October 2026.")
    st.write("**Model inputs:** departure date/time, weather category and traffic category.")
    st.write("**Prediction target:** trip duration in minutes.")
    st.write("**Evaluation from the notebook's synthetic chronological holdout:** MAE 3.35 min · RMSE 4.47 min · R² 0.774.")
    st.warning("These metrics describe only the synthetic test split. They do not establish accuracy on actual journeys.")
    st.markdown("**Data provenance:** The workbook was generated for this prototype. Weather and traffic labels are illustrative, not fetched from historical sources.")
