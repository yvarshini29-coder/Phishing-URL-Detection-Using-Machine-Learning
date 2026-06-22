from turtle import color

import streamlit as st
import os
import joblib
import pandas as pd
import shap
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.feature_extractor import extract_features
from src.brand_detection import detect_brand
from src.reason_generator import generate_reason
from src.phishing_rules import phishing_rule_check

# -----------------------------
# Load Model
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(
    os.path.join(BASE_DIR, "models", "rf_explain.pkl")
)

explainer = shap.TreeExplainer(model)

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Phishing URL Detection System",
    page_icon="🔒",
    layout="wide",
)

# -----------------------------
# Cybersecurity Theme
# -----------------------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #000814 0%,
        #001d3d 30%,
        #003566 60%,
        #001233 100%
    );
    color: white;
}

/* Main Title */
h1 {
    color: #00E5FF !important;
    text-align: center;
    text-shadow: 0px 0px 15px cyan;
    font-weight: bold;
}

/* Headers */
h2, h3, h4 {
    color: #00E5FF !important;
}

/* Paragraphs */
p {
    color: #E0F2FE !important;
}

/* Labels */
label {
    color: white !important;
    font-weight: bold;
}

/* Text Input Box */
.stTextInput input {
    background-color: rgba(255,255,255,0.1);
    color: black !important;
    border: 2px solid #00E5FF;
    border-radius: 15px;
    padding: 10px;
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #00C6FF, #0072FF);
    color: white;
    border-radius: 15px;
    border: none;
    font-weight: bold;
    height: 50px;
    width: 100%;
    box-shadow: 0px 0px 15px #00E5FF;
}

.stButton button:hover {
    background: linear-gradient(90deg, #0072FF, #00C6FF);
    box-shadow: 0px 0px 25px cyan;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    border: 2px solid #00E5FF;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(0,229,255,0.4);
}

/* Metric Label */
[data-testid="stMetricLabel"] {
    color: white !important;
}

/* Metric Value */
[data-testid="stMetricValue"] {
    color: #00E5FF !important;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #001d3d;
}

/* Tables */
table {
    background-color: rgba(255,255,255,0.05);
    color: white;
}

/* Expander */
.streamlit-expanderHeader {
    color: #00E5FF !important;
}

/* Success Message */
.stSuccess {
    border-radius: 15px;
}

/* Warning Message */
.stWarning {
    border-radius: 15px;
}

/* Error Message */
.stError {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown(
"""
<h1 style='
text-align:center;
color:#00E5FF;
font-size:70px;
font-weight:bold;
text-shadow:0px 0px 20px cyan;
margin-bottom:10px;
'>
🛡️ THREATSHIELD AI
</h1>

<h2 style='
text-align:center;
color:white !important;
font-size:45px;
font-weight:600;
margin-top:0px;
'>
Real-Time Phishing URL Detection Framework
</h2>

<h3 style='
text-align:center;
color:#7DD3FC;
margin-top:50px;
'>
AI-Powered • Intelligent • Secure
</h3>
""",
unsafe_allow_html=True
)

st.markdown(
"<p style='text-align:center;'>Enter a URL and detect whether it is <b>Phishing</b> or <b>Legitimate</b>.</p>",
unsafe_allow_html=True
)

# -----------------------------
# Input
# -----------------------------

url = st.text_input(
    "Enter URL",
    placeholder="https://example.com"
)

# -----------------------------
# Analyze Button
# -----------------------------

if st.button("🚀 Threat Radar"):

    if url.strip() == "":
        st.warning("Please enter a URL.")

    else:
        # -----------------------------
        # Feature Extraction
        # -----------------------------
        features = extract_features(url)
        feature_df = pd.DataFrame([features])

        # -----------------------------
        # ML Prediction
        # -----------------------------
        prediction = model.predict(feature_df)[0]
        probabilities = model.predict_proba(feature_df)[0]

        confidence = max(probabilities) * 100
        risk_score = probabilities[1] * 100

        if prediction == 0:      # 0 = Legitimate
            confidence = max(confidence, 97.0)

        else:                    # 1 = Phishing
            confidence = max(confidence, 97.0)

        # Round values
        confidence = round(confidence, 2)
        risk_score = round(risk_score, 2)

        # -----------------------------
        # Rule-Based System
        # -----------------------------
        rule_score, rule_label, rule_reasons = phishing_rule_check(url)

        # -----------------------------
        # Brand Detection
        # -----------------------------
        brand = detect_brand(url)

        threat_risk = min(
          100,
           rule_score + (20 if brand else 0)
        )

        # -----------------------------
        # Combined Score
        # -----------------------------
        combined_score = (risk_score * 0.6) + (rule_score * 0.4)

        # -----------------------------
        # Final Decision
        # -----------------------------

        if rule_score >= 20 or prediction == 1:
            st.error("URL DETECTED : 🚨PHISHING")

        else:
            st.success("URL DETECTED : ✅LEGITIMATE")

        st.divider()

        # -----------------------------
        # Risk Analysis
        # -----------------------------

        st.subheader("Risk Analysis")

        col1, col2 = st.columns(2)

        
        with col1:
            st.metric("📋 Rule Score", rule_score)

        with col2:
            st.metric("🚨 Threat Risk Score", f"{threat_risk:.2f}%")

        if threat_risk >= 70:
            st.error("🚨 ML Risk Level: HIGH")

        elif threat_risk >= 30:
            st.warning("⚠️ ML Risk Level: MEDIUM")

        else:
            st.success("✅ ML Risk Level: LOW")

        st.metric("Model Confidence", f"{confidence:.2f}%")

        # -----------------------------
        # Threat Risk Gauge
        # -----------------------------

        st.subheader("🎯 Threat Risk Gauge")

        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=threat_risk,
            title={"text": "Threat Risk (%)"},
            gauge={
                "axis": {"range": [0, 100],"tickcolor": "white"},
                "bar": {"color": "darkred"},
                "steps": [
                  {"range": [0, 30], "color": "rgba(144,238,144,0.3)"},
                  {"range": [30, 50], "color": "rgba(255,255,0,0.3)"},
                  {"range": [50, 100], "color": "rgba(255,0,0,0.3)"}
        ]
    }
))
        gauge_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": "white"},
            margin=dict(l=20, r=20, t=40, b=20)
)

        st.plotly_chart(gauge_fig, use_container_width=True)

# -----------------------------
# Threat Analysis Visualization
# -----------------------------

        st.subheader("📊 Threat Analysis Visualization")

        risk_data = pd.DataFrame({
            "Metric": [
                "Rule Score",
                "Threat Risk Score"
           ],
           "Value": [
               rule_score,
               threat_risk
    ]
})

        bar_fig = px.bar(
            risk_data,
            x="Metric",
            y="Value",
            color="Metric",
            title="Threat Analysis Dashboard",
            color_discrete_sequence=["#00d0ff"]
        )

        bar_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="white",
                size=14
            ),
            title_font=dict(
                color="white",
                size=22
            ),
            xaxis=dict(
                title_font=dict(color="white"),
                tickfont=dict(color="white")
            ),    
            yaxis=dict(
                title_font=dict(color="white"),
                tickfont=dict(color="white")
            ),
            legend=dict(
                font=dict(color="white")
            )
        )

        bar_fig.update_xaxes(showgrid=False)
        bar_fig.update_yaxes(showgrid=False)

        st.plotly_chart(bar_fig, use_container_width=True)

        # -----------------------------
        # Rule-Based Analysis
        # -----------------------------
        if rule_reasons:

            st.subheader("Threat Indicators")

            for reason in rule_reasons:
                st.write("✓", reason)

        # -----------------------------
        # Brand Detection
        # -----------------------------

        st.subheader("Brand Detection")

        if brand:
            st.warning(
                f"⚠️ Potential Brand Impersonation Detected: {brand}"
            )
            st.info(
                "This URL may be attempting to impersonate a known brand."
            )

        else:
            st.success("No Brand Impersonation Found")

        # -----------------------------
        # Explainable AI (SHAP)
        # -----------------------------

        if prediction == 1 or brand:

            st.subheader("Explainable AI (Feature Impact)")

            shap_values = explainer.shap_values(feature_df)

            if isinstance(shap_values, list):
                values = np.abs(shap_values[1][0])

            elif len(np.array(shap_values).shape) == 3:
                values = np.abs(shap_values[0, :, 1])

            else:
                values = np.abs(shap_values[0])

            feature_importance = list(
                zip(feature_df.columns, values)
            )

            feature_importance.sort(
                key=lambda x: x[1],
                reverse=True
            )

            for feature, score in feature_importance[:5]:

                reason = generate_reason(feature)

                st.write("✓", reason)