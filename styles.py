import streamlit as st


def apply_styles():
    st.markdown("""
<style>

[data-testid="stHeader"] {
    background-color: #0d1117 !important;
}

[data-testid="stDecoration"] {
    display: none;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.stApp {
    background-color: #0d1117;
    color: #e6edf3;
}

.main .block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #30363d;
}

section[data-testid="stSidebar"] * {
    color: #e6edf3 !important;
}

/* ===== SIDEBAR TOGGLE ===== */

button[kind="header"] {
    color: #00ff88 !important;
}

button[kind="header"]:hover {
    color: #2ea043 !important;
    background-color: transparent !important;
}

/* ===== DASHBOARD CARDS ===== */

.metric-card {
    background: linear-gradient(135deg, #161b22, #1f2937);
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 20px;
    transition: all .3s ease;
    cursor: pointer;
    margin-bottom: 15px;
}

.metric-card:hover {
    transform: translateY(-5px);
    border-color: #58a6ff;
    box-shadow: 0 0 25px rgba(88,166,255,.25);
}

.metric-title {
    color: #9ca3af;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 10px;
}

.metric-value {
    color: #58a6ff;
    font-size: 42px;
    font-weight: 800;
}

/* ===== TEXT AREA ===== */

.stTextArea textarea {
    background-color: #161b22 !important;
    color: #00ff88 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    font-family: monospace !important;
    font-size: 16px !important;
    padding: 15px !important;
}

/* ===== SELECTBOX ===== */

.stSelectbox > div > div {
    background-color: #161b22 !important;
    color: #ffffff !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
}

.stSelectbox span {
    color: #ffffff !important;
    font-weight: 500 !important;
}

.stSelectbox input {
    color: #ffffff !important;
}

div[role="listbox"] {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
}

div[role="option"] {
    background-color: #161b22 !important;
    color: #ffffff !important;
    font-weight: 500 !important;
}

div[role="option"]:hover {
    background-color: #1f6feb !important;
    color: #ffffff !important;
}

div[aria-selected="true"] {
    background-color: #238636 !important;
    color: #ffffff !important;
}

/* ===== BUTTON ===== */

.stButton button {
    background-color: #238636 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: bold !important;
}

.stButton button:hover {
    background-color: #2ea043 !important;
}

/* ===== DOWNLOAD BUTTON ===== */

[data-testid="stDownloadButton"] button {
    background-color: #238636 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: bold !important;
}

[data-testid="stDownloadButton"] button:hover {
    background-color: #1f6feb !important;
    color: #ffffff !important;
}

/* ===== LABELS ===== */

label {
    color: #9ca3af !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* ===== CARDS ===== */

.card {
    background-color: #161b22;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 15px;
    border-left: 5px solid;
}

.bug       { border-color: #ff4d4f; }
.warning   { border-color: #faad14; }
.fix       { border-color: #52c41a; }
.explanation { border-color: #1677ff; }

/* ===== SIDEBAR BUTTONS ===== */

button[kind="header"] {
    background: #2563eb !important;
    border: 2px solid #60a5fa !important;
    border-radius: 12px !important;
    width: 45px !important;
    height: 45px !important;
    color: white !important;
    box-shadow: 0 0 15px rgba(37,99,235,.4);
}

button[kind="header"]:hover {
    background: #3b82f6 !important;
    transform: scale(1.08);
}

button[data-testid="stExpanderSidebarButton"] {
    position: fixed !important;
    top: 90px !important;
    left: 15px !important;
    width: 55px !important;
    height: 55px !important;
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    border: 2px solid #60a5fa !important;
    border-radius: 14px !important;
    z-index: 99999 !important;
    box-shadow: 0 0 20px rgba(37,99,235,.5) !important;
}

button[data-testid="stExpanderSidebarButton"]:hover {
    transform: scale(1.08);
    background: #3b82f6 !important;
}

button[data-testid="stExpanderSidebarButton"] span {
    color: white !important;
    font-size: 28px !important;
}

/* ===== SUMMARY BOX ===== */

.summary-box {
    background-color: #111827;
    border: 1px solid #30363d;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}

/* ===== LANGUAGE CARDS ===== */

.lang-card {
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 15px;
    font-size: 20px;
    font-weight: 700;
    border: 1px solid transparent;
    transition: all .3s ease;
    text-align: center;
    cursor: pointer;
}

.lang-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 0 25px rgba(255,255,255,.15);
}

.python-card { background: linear-gradient(135deg,#14532d,#166534); color: white; border: 1px solid #22c55e; }
.java-card   { background: linear-gradient(135deg,#7c2d12,#ea580c); color: white; border: 1px solid #fb923c; }
.sql-card    { background: linear-gradient(135deg,#581c87,#9333ea); color: white; border: 1px solid #c084fc; }
.js-card     { background: linear-gradient(135deg,#854d0e,#ca8a04); color: white; border: 1px solid #facc15; }
.cpp-card    { background: linear-gradient(135deg,#1e3a8a,#2563eb); color: white; border: 1px solid #60a5fa; }

</style>
""", unsafe_allow_html=True)