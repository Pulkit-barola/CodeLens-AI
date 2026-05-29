import streamlit as st
from detector import detect_local_issues
from analyzer import analyze_code
from executor import execute_python
from streamlit_ace import st_ace

import json
import os
from datetime import datetime
import re

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="CodeLens AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# SAVE HISTORY
# =========================


def save_history(code, language, mode, result, quality):

    history_file = "data/history.json"

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(history_file):

        with open(history_file, "w") as f:
            json.dump([], f)

    try:

        with open(history_file, "r") as f:
            history = json.load(f)

    except:

        history = []

    history.insert(0, {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "language": language,
        "mode": mode,
        "code": code,
        "summary": result.get("summary", ""),
        "score": quality["overall"]
    })

    with open(history_file, "w") as f:
        json.dump(history[:20], f, indent=4)
# =========================
# UPDATE STATS
# =========================

def update_stats(language):

    stats_file = "data/stats.json"

    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(stats_file):

        stats = {
            "total_analyses": 0,
            "python": 0,
            "javascript": 0,
            "java": 0,
            "cpp": 0,
            "sql": 0
        }

    else:

        try:

            with open(stats_file, "r") as f:
                stats = json.load(f)

        except:

            stats = {
                "total_analyses": 0,
                "python": 0,
                "javascript": 0,
                "java": 0,
                "cpp": 0,
                "sql": 0
            }

    stats["total_analyses"] += 1

    if language == "Python":
        stats["python"] += 1

    elif language == "JavaScript":
        stats["javascript"] += 1

    elif language == "Java":
        stats["java"] += 1

    elif language == "C++":
        stats["cpp"] += 1

    elif language == "SQL":
        stats["sql"] += 1

    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=4)

def calculate_quality_metrics(code):

    code_lower = code.lower()

    readability = 100
    maintainability = 100
    performance = 100
    security = 100

    lines = len(code.splitlines())

    # ======================
    # READABILITY
    # ======================

    if lines > 50:
        readability -= 10

    if lines > 100:
        readability -= 15

    if len(code) > 3000:
        readability -= 10

    # ======================
    # MAINTAINABILITY
    # ======================

    if code.count("if") > 5:
        maintainability -= 10

    if code.count("for") > 5:
        maintainability -= 10

    if code.count("while") > 3:
        maintainability -= 10

    if "try:" not in code and "except" not in code:
        maintainability -= 5

    # ======================
    # PERFORMANCE
    # ======================

    if "while true" in code_lower:
        performance -= 25

    if "sleep(" in code_lower:
        performance -= 5

    if "factorial(" in code_lower:
        performance -= 5

    if "fibonacci(" in code_lower:
        performance -= 5

    # ======================
    # SECURITY
    # ======================

    if "eval(" in code_lower:
        security -= 40

    if "exec(" in code_lower:
        security -= 40

    if "os.system(" in code_lower:
        security -= 25

    if "subprocess.call(" in code_lower:
        security -= 20

    # ======================
    # LIMIT VALUES
    # ======================

    readability = max(0, min(100, readability))
    maintainability = max(0, min(100, maintainability))
    performance = max(0, min(100, performance))
    security = max(0, min(100, security))

    # ======================
    # FINAL SCORE
    # ======================

    final_score = int(
        (
            readability +
            maintainability +
            performance +
            security
        ) / 4
    )

    return {
        "overall": final_score,
        "readability": readability,
        "maintainability": maintainability,
        "performance": performance,
        "security": security
    }

def analyze_complexity(code):

    code_lower = code.lower()

    time_complexity = "O(1)"
    space_complexity = "O(1)"
    level = "Easy"

    loop_count = code_lower.count("for ") + code_lower.count("while ")

    # Nested loops
    if loop_count >= 2:
        time_complexity = "O(n²)"
        level = "Hard"

    elif loop_count == 1:
        time_complexity = "O(n)"
        level = "Medium"

    # Recursion
    if "factorial(" in code_lower or "fibonacci(" in code_lower:
        time_complexity = "O(n)"
        level = "Medium"

    # Recursive Fibonacci
    if "fibonacci(" in code_lower:
        time_complexity = "O(2ⁿ)"
        level = "Very Hard"

    # Large arrays/lists
    if "[]" in code or "list(" in code_lower:
        space_complexity = "O(n)"

    return {
        "time": time_complexity,
        "space": space_complexity,
        "level": level
    }
# =========================
# CSS
# =========================

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
            
/* =========================
   DASHBOARD CARDS
========================= */

.metric-card{
    background: linear-gradient(
        135deg,
        #161b22,
        #1f2937
    );

    border:1px solid #30363d;

    border-radius:16px;

    padding:20px;

    transition:all .3s ease;

    cursor:pointer;

    margin-bottom:15px;
}

.metric-card:hover{

    transform:translateY(-5px);

    border-color:#58a6ff;

    box-shadow:
    0 0 25px rgba(88,166,255,.25);
}

.metric-title{

    color:#9ca3af;

    font-size:14px;

    font-weight:600;

    margin-bottom:10px;
}

.metric-value{

    color:#58a6ff;

    font-size:42px;

    font-weight:800;
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

/* Hover State */

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

.bug {
    border-color: #ff4d4f;
}

.warning {
    border-color: #faad14;
}

.fix {
    border-color: #52c41a;
}

.explanation {
    border-color: #1677ff;
}
            /* Sidebar Toggle Button */

button[kind="header"]{
    background: #2563eb !important;
    border: 2px solid #60a5fa !important;
    border-radius: 12px !important;

    width: 45px !important;
    height: 45px !important;

    color: white !important;

    box-shadow: 0 0 15px rgba(37,99,235,.4);
}

button[kind="header"]:hover{
    background: #3b82f6 !important;
    transform: scale(1.08);
}
            
/* Sidebar Arrow Button */

button[data-testid="stExpanderSidebarButton"]{

    position:fixed !important;

    top:90px !important;
    left:15px !important;

    width:55px !important;
    height:55px !important;

    background:linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    ) !important;

    border:2px solid #60a5fa !important;
    border-radius:14px !important;

    z-index:99999 !important;

    box-shadow:
    0 0 20px rgba(37,99,235,.5) !important;
}

button[data-testid="stExpanderSidebarButton"]:hover{

    transform:scale(1.08);

    background:#3b82f6 !important;
}

button[data-testid="stExpanderSidebarButton"] span{

    color:white !important;

    font-size:28px !important;
}

/* ===== SUMMARY ===== */

 .summary-box {
    background-color: #111827;
    border: 1px solid #30363d;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
.metric-card{
    background: linear-gradient(
        135deg,
        #161b22,
        #1f2937
    );

    border:1px solid #30363d;
    border-radius:16px;
    padding:20px;

    transition:all .3s ease;
    cursor:pointer;

    margin-bottom:15px;
}

.metric-card:hover{

    transform:translateY(-5px);

    border-color:#58a6ff;

    box-shadow:
    0 0 25px rgba(88,166,255,.25);
}

.metric-title{

    color:#9ca3af;

    font-size:14px;

    font-weight:600;

    margin-bottom:10px;
}

.metric-value{

    color:#58a6ff;

    font-size:42px;

    font-weight:800;
}
            
.lang-card{
    padding:20px;
    border-radius:16px;
    margin-bottom:15px;
    font-size:20px;
    font-weight:700;
    border:1px solid transparent;
    transition:all .3s ease;
    text-align:center;
    cursor:pointer;
}

.lang-card:hover{
    transform:translateY(-6px) scale(1.02);
    box-shadow:0 0 25px rgba(255,255,255,.15);
}

.python-card{
    background:linear-gradient(135deg,#14532d,#166534);
    color:white;
    border:1px solid #22c55e;
}

.java-card{
    background:linear-gradient(135deg,#7c2d12,#ea580c);
    color:white;
    border:1px solid #fb923c;
}

.sql-card{
    background:linear-gradient(135deg,#581c87,#9333ea);
    color:white;
    border:1px solid #c084fc;
}

.js-card{
    background:linear-gradient(135deg,#854d0e,#ca8a04);
    color:white;
    border:1px solid #facc15;
}

.cpp-card{
    background:linear-gradient(135deg,#1e3a8a,#2563eb);
    color:white;
    border:1px solid #60a5fa;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.title("🧠 CodeLens AI")
st.caption("AI-Powered Code Explainer + Debugger")

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("🧠 CodeLens AI")

    st.markdown("---")

    st.subheader("Features")
    st.subheader("System")

    st.success("🟢 Online")
    st.info("⚡ Runtime Enabled")
    st.info("🧠 AI Enabled")

    st.markdown("""
- ✅ AI Code Explanation
- ✅ AI Debugging
- ✅ Static Bug Detection
- ✅ Runtime Execution
- ✅ Multi-language Support
- ✅ Analysis History
""")

    st.markdown("---")

    st.success("System Running")
    

# =========================
# SAMPLE SNIPPETS
# =========================

samples = {

    "Factorial Recursion": """def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
""",

    "Infinite Loop": """while True:
    print("Infinite")
""",

    "Broken API Call": """fetch('/api/data')
.then(res => res.json)
.then(data => console.log(data))
""",

    "SQL Injection": """query = "SELECT * FROM users WHERE name = '" + username + "'"
"""
}

# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4 = st.tabs([
    "💻 Analyzer",
    "📊 Dashboard",
    "📜 History",
    "⚙ Settings"
])

# =========================
# ANALYZER TAB
# =========================

with tab1:

    left, right = st.columns([1,1])

    # =========================
    # LEFT PANEL
    # =========================

    with left:

        st.subheader("💻 Code Input")

        language = st.selectbox(
            "Select Language",
            ["Python", "JavaScript", "Java", "C++", "SQL"]
        )

        mode = st.pills(
            "Choose Mode",
            ["Explain", "Debug", "Both"]
        )

        sample = st.selectbox(
            "Try Sample (Optional)",
            ["Custom Code"] + list(samples.keys())
        )

        default_code = ""

        if sample != "Custom Code":
            default_code = samples[sample]

        editor_language = language.lower()

        if language == "C++":
            editor_language = "c_cpp"

        if language == "JavaScript":
            editor_language = "javascript"

        code_input = st_ace(
            value=default_code,
            language=editor_language,
            theme="monokai",
            height=400,
            font_size=16,
            tab_size=4,
            wrap=True,
            auto_update=True,
            show_gutter=True,
            show_print_margin=False
        )

        analyze_btn = st.button("🚀 Analyze Code")

    # =========================
    # RIGHT PANEL
    # =========================

    with right:

        st.subheader("🧠 AI Analysis")

        if analyze_btn:

            if code_input.strip() == "":

                st.warning("Please paste some code.")

            else:

                status = st.empty()

                status.info("🔍 Scanning code...")

                # =========================
                # LOCAL DETECTOR
                # =========================

                local_result = detect_local_issues(code_input)

                # =========================
                # RUNTIME EXECUTION
                # =========================

                runtime_result = None

                if language == "Python":

                    status.info("⚡ Executing Python code...")

                    runtime_result = execute_python(code_input)

                status.info("🧠 Running AI analysis...")

                # =========================
                # AI ANALYSIS
                # =========================

                result = analyze_code(
                    code_input,
                    mode,
                    language
                )
                quality = calculate_quality_metrics(code_input)
                complexity = analyze_complexity(code_input)
                bug_penalty = len(result.get("bugs", [])) * 12
                warning_penalty = len(result.get("warnings", [])) * 5

                quality["overall"] = max(
                            0,
                        quality["overall"] - bug_penalty - warning_penalty
)
                # =========================
                # MERGE LOCAL + AI RESULTS
                # =========================

                result["bugs"] = (
                    local_result.get("bugs", []) +
                    result.get("bugs", [])
                )

                result["warnings"] = (
                    local_result.get("warnings", []) +
                    result.get("warnings", [])
                )

                # =========================
                # Code Quality Report
                # =========================

                st.markdown("### ⭐ Code Quality Report")

                q1, q2, q3, q4, q5 = st.columns(5)

                with q1:
                    st.metric(
                        "🏆 Overall",
                        f"{quality['overall']}/100"
                    )

                with q2:
                    st.metric(
                        "📖 Readability",
                     quality['readability']
                    )

                with q3:
                    st.metric(
                        "⚡ Performance",
                        quality['performance']
                    )

                with q4:
                    st.metric(
                        "🔒 Security",
                        quality['security']
                )
                with q5:
                    st.metric(
                        "🛠 Maintainability",
                        quality['maintainability']
                )
                    
                    # =========================
                    # CODE HEALTH STATUS
                    # =========================

                if quality["overall"] >= 90:
                    st.success("🟢 Production Ready")

                elif quality["overall"] >= 75:
                    st.info("🔵 Good Quality")

                elif quality["overall"] >= 60:
                    st.warning("🟡 Needs Optimization")

                else:
                    st.error("🔴 High Risk Code")
                ##MARKET ANALYSIS##

                st.markdown("### ⏱ Complexity Analysis")

                c1, c2, c3 = st.columns(3)

                with c1:                   
                    st.metric(
                        "⏱ Time Complexity",
                        complexity["time"]
                    )

                with c2:
                    st.metric(
                        "💾 Space Complexity",
                        complexity["space"]
                    )

                with c3:
                    st.metric(
                        "🔥 Complexity Level",
                        complexity["level"]
                    )

                # =========================
                # DETAILED ANALYSIS
                # =========================

                st.markdown("### 📊 Detailed Analysis")

                st.progress(quality["readability"] / 100)
                st.caption(f"📖 Readability : {quality['readability']}%")

                st.progress(quality["maintainability"] / 100)
                st.caption(f"🛠 Maintainability : {quality['maintainability']}%")

                st.progress(quality["performance"] / 100)
                st.caption(f"⚡ Performance : {quality['performance']}%")

                st.progress(quality["security"] / 100)
                st.caption(f"🔒 Security : {quality['security']}%")
                # =========================
                # SAVE HISTORY
                # =========================

                save_history(
                    code_input,
                    language,
                    mode,
                    result,
                    quality
                )
                update_stats(language)
                
                runtime_text = ""

                if runtime_result:

                    runtime_text += "\nOUTPUT:\n"
                    runtime_text += runtime_result.get("output", "")

                    runtime_text += "\n\nERROR:\n"
                    runtime_text += runtime_result.get("error", "")

                report = f"""

                
==============================
        CODELENS AI REPORT
==============================

Date: {datetime.now()}

Language: {language}
Mode: {mode}

==============================
SUMMARY
==============================

{result.get("summary", "")}

==============================
BUGS
==============================

{chr(10).join(result.get("bugs", []))}

==============================
WARNINGS
==============================

{chr(10).join(result.get("warnings", []))}

==============================
FIXES
==============================

{chr(10).join(result.get("fixes", []))}

==============================
RUNTIME
==============================

{runtime_text}
"""

                status.success("✅ Analysis Complete")

                # =========================
                # SUMMARY
                # =========================

                st.markdown(f'''
<div class="summary-box">
<h3>📌 Summary</h3>
<p>{result.get("summary", "")}</p>
</div>
''', unsafe_allow_html=True)

                # =========================
                # BUGS
                # =========================

                if result.get("bugs"):

                    st.subheader("🔴 Bugs")

                    for item in result["bugs"]:

                        st.markdown(f'''
<div class="card bug">
{item}
</div>
''', unsafe_allow_html=True)

                # =========================
                # WARNINGS
                # =========================

                if result.get("warnings"):

                    st.subheader("🟡 Warnings")

                    for item in result["warnings"]:

                        st.markdown(f'''
<div class="card warning">
{item}
</div>
''', unsafe_allow_html=True)

                # =========================
                # FIXES
                # =========================

                if result.get("fixes"):

                    st.subheader("🟢 Fixes")

                    for item in result["fixes"]:

                        st.markdown(f'''
<div class="card fix">
{item}
</div>
''', unsafe_allow_html=True)

                # =========================
                # RUNTIME OUTPUT
                # =========================

                if runtime_result:

                    st.subheader("⚡ Runtime Output")

                    if runtime_result["output"]:
                        st.code(
                            runtime_result["output"],
                            language="text"
                        )

                    if runtime_result["error"]:
                        st.error(runtime_result["error"])

                    st.markdown("### 📊 Code Quality Score")

                    q1, q2, q3, q4 = st.columns(4)

                    with q1:
                        st.metric("🏆 Overall", f"{quality['overall']}%")

                    with q2:
                        st.metric("📖 Readability", f"{quality['readability']}%")

                    with q3:
                        st.metric("⚡ Performance", f"{quality['performance']}%")

                    with q4:
                        st.metric("🔒 Security", f"{quality['security']}%")

                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"codelens_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

# =========================
# HISTORY TAB
# =========================

with tab3:

    st.subheader("📜 Analysis History")

    history_file = "data/history.json"

    if os.path.exists(history_file):

        try:

            with open(history_file, "r") as f:
                history = json.load(f)

        except:

            history = []

        if history:

            for item in history:

                with st.expander(
                    f"{item['language']} • Score: {item.get('score',0)} • {item['time']}"
                ):

                    st.code(
                        item["code"],
                        language=item["language"].lower()
                    )

                    st.markdown(f"""
### Summary

{item['summary']}
""")

        else:

            st.info("No history yet.")


# =========================
# DASHBOARD TAB
# =========================

with tab2:

    st.markdown("""
    <div style="
    padding:25px;
    border-radius:18px;
    background:linear-gradient(
    90deg,
    #0f172a,
    #1e293b
    );
    border:1px solid #30363d;
    margin-bottom:20px;
    ">

    <h1 style="
    margin:0;
    color:#58a6ff;
    ">
    📊 Analytics Dashboard
    </h1>

    <p style="
    color:#9ca3af;
    margin-top:10px;
    ">
    Monitor usage, language trends and activity.
    </p>

    </div>
    """, unsafe_allow_html=True)

    stats_file = "data/stats.json"

    if os.path.exists(stats_file):

        try:

            with open(stats_file, "r") as f:
                stats = json.load(f)

            languages_used = sum([
                1 if stats["python"] else 0,
                1 if stats["javascript"] else 0,
                1 if stats["java"] else 0,
                1 if stats["cpp"] else 0,
                1 if stats["sql"] else 0
            ])

            col1, col2 = st.columns(2)

            with col1:

                st.markdown(
                f"""
                    <div class="metric-card">
                    <div class="metric-title">📈 Total Analyses</div>
                    <div class="metric-value">{stats['total_analyses']}</div>
                    </div>
                """,
                unsafe_allow_html=True
            )

            with col2:

                st.markdown(
                f"""
                    <div class="metric-card">
                    <div class="metric-title">🌎 Languages Used</div>
                    <div class="metric-value">{languages_used}</div>
                </div>
                 """,
                unsafe_allow_html=True
            )

            st.markdown("---")

            c1, c2 = st.columns(2)


            with c1:

                    st.markdown(
                               f"""
                                <div style="
                                    background:#166534;
                                    border:1px solid #22c55e;
                                    border-radius:16px;
                                    padding:20px;
                                    color:white;
                                    text-align:center;
                                    margin-bottom:15px;
                                ">
                                    <div style="font-size:18px;font-weight:600;">
                                        🐍 Python
                                    </div>
                                    {stats["python"]}
                                
                                </div>
                            """,
                            unsafe_allow_html=True
                        )
                    st.markdown(
                               f"""
                                <div style="
                                        background:linear-gradient(135deg,#7c2d12,#ea580c);
                                        border:1px solid #fb923c;
                                        border-radius:16px;
                                        padding:20px;
                                        color:white;
                                        text-align:center;
                                         margin-bottom:15px;
                                    ">
                                    <div style="font-size:18px;font-weight:600;">
                                        ☕ java
                                    </div>
                                    {stats["java"]}
                                
                                </div>
                            """,
                            unsafe_allow_html=True
                )

                    st.markdown(
                               f"""
                                <div style="
                                        background:linear-gradient(135deg,#581c87,#9333ea);
                                        border:1px solid #c084fc;
                                        border-radius:16px;
                                        padding:20px;
                                        color:white;
                                        text-align:center;
                                        margin-bottom:15px;
                                    ">
                                    <div style="font-size:18px;font-weight:600;">
                                         📓SQL
                                    </div>
                                    {stats["sql"]}
                                
                                </div>
                            """,
                            unsafe_allow_html=True
                    )

            with c2:

                st.markdown(
                               f"""
                                <div style="
                                    background:linear-gradient(135deg,#854d0e,#ca8a04);
                                    border:1px solid #facc15;
                                    border-radius:16px;
                                    padding:20px;
                                    color:white;
                                    text-align:center;
                                    margin-bottom:15px;
                                ">
                                    <div style="font-size:18px;font-weight:600;">
                                        🟨 JavaScript
                                    </div>
                                    {stats["javascript"]}
                                
                                </div>
                            """,
                            unsafe_allow_html=True
                    )

                st.markdown(
                               f"""
                                <div style="
                                    background:linear-gradient(135deg,#1e3a8a,#2563eb);
                                    border:1px solid #60a5fa;
                                    border-radius:16px;
                                    padding:20px;
                                    color:white;
                                    text-align:center;
                                    margin-bottom:15px;
                                ">
                                    <div style="font-size:18px;font-weight:600;">
                                        ⚙️ C++
                                    </div>
                                    {stats["cpp"]}
                                
                                </div>
                            """,
                            unsafe_allow_html=True
                    )
                st.markdown("---")
                st.subheader("📈 Language Usage Chart")
                st.markdown("---")
                st.subheader("📥 Export Analytics")

                col1, col2 = st.columns(2)

            with col1:

                    st.download_button(
                        "📥 Download JSON",
                        data=json.dumps(stats, indent=4),
                        file_name="analytics.json",
                        mime="application/json"
                    )

            with col2:

                    import pandas as pd

                    export_df = pd.DataFrame({
                 "Language": ["Python", "JavaScript", "Java", "C++", "SQL"],
                "Count": [
                     stats["python"],
                     stats["javascript"],
                     stats["java"],
                    stats["cpp"],
                    stats["sql"]
              ]
            })

            csv_data = export_df.to_csv(index=False)

            st.download_button(
                    "📥 Download CSV",
                    data=csv_data,
                 file_name="analytics.csv",
                 mime="text/csv"
            )
            import pandas as pd

            chart_data = pd.DataFrame({
                    "Language": ["Python", "JavaScript", "Java", "C++", "SQL"],
                    "Count": [
                            stats["python"],
                            stats["javascript"],
                            stats["java"],
                            stats["cpp"],
                            stats["sql"]
                        ]   
                })

            import plotly.express as px

            fig = px.bar(
                chart_data,
                x="Language",
                y="Count",
                title="Language Usage Analytics"
            )

            fig.update_layout(
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
            chart_image = fig.to_image(
                format="png"
            )

            st.download_button(
                label="📊 Download Chart PNG",
                data=chart_image,
                file_name="language_usage_chart.png",
                mime="image/png"
            )
        except:
            st.warning("Dashboard data unavailable.")
# =========================
# SETTINGS TAB
# =========================

with tab4:

    st.subheader("⚙ Settings")

    st.markdown("""
### Theme
Dark Mode Enabled

### AI Model
llama-3.3-70b-versatile

### Features
- AI Analysis
- Static Bug Detection
- Runtime Execution
- Analysis History
- Multi-language Support

### Upcoming Features
- Monaco Editor
- PDF Reports
- Team Workspace
""")
    
    st.markdown("---")

st.subheader("🗑 Reset Data")

st.warning(
    "This will permanently delete all analytics and history data."
)

confirm_reset = st.checkbox(
    "I understand this action cannot be undone"
)

if confirm_reset:

    if st.button("🚨 Reset All Data"):

        stats_file = "data/stats.json"

        with open(stats_file, "w") as f:

            json.dump({
                "total_analyses": 0,
                "python": 0,
                "javascript": 0,
                "java": 0,
                "cpp": 0,
                "sql": 0
            }, f, indent=4)

        history_file = "data/history.json"

        with open(history_file, "w") as f:

            json.dump([], f)

        st.success(
            "✅ All analytics and history data reset successfully!"
        )

        st.rerun()