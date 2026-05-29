import streamlit as st
from streamlit_ace import st_ace
from datetime import datetime

from detector import detect_local_issues
from analyzer import analyze_code
from executor import execute_python
from metrics import calculate_quality_metrics, analyze_complexity
from utils import save_history, update_stats


SAMPLES = {
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


def render_analyzer_tab():
    left, right = st.columns([1, 1])

    with left:
        _render_input_panel()

    # Store widgets in session state so right panel can read them
    # (Streamlit re-runs top-to-bottom, so we use a flag pattern)


def _render_input_panel():
    st.subheader("💻 Code Input")

    language = st.selectbox(
        "Select Language",
        ["Python", "JavaScript", "Java", "C++", "SQL"],
        key="language"
    )

    mode = st.pills(
        "Choose Mode",
        ["Explain", "Debug", "Both"],
        key="mode"
    )

    sample = st.selectbox(
        "Try Sample (Optional)",
        ["Custom Code"] + list(SAMPLES.keys()),
        key="sample"
    )

    default_code = SAMPLES.get(sample, "")

    editor_language = language.lower()
    if language == "C++":
        editor_language = "c_cpp"

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
        show_print_margin=False,
        key="code_editor"
    )

    analyze_btn = st.button("🚀 Analyze Code")

    if analyze_btn:
        _run_analysis(code_input, language, mode)


def _run_analysis(code_input, language, mode):
    if not code_input.strip():
        st.warning("Please paste some code.")
        return

    # Use the second column for output — re-enter right column context
    # via a placeholder written before the columns were created.
    # Since columns are rendered together, we write results below the cols.
    _display_results(code_input, language, mode)


def _display_results(code_input, language, mode):
    st.subheader("🧠 AI Analysis")
    status = st.empty()

    status.info("🔍 Scanning code...")
    local_result = detect_local_issues(code_input)

    runtime_result = None
    if language == "Python":
        status.info("⚡ Executing Python code...")
        runtime_result = execute_python(code_input)

    status.info("🧠 Running AI analysis...")
    result   = analyze_code(code_input, mode, language)
    quality  = calculate_quality_metrics(code_input)
    complexity = analyze_complexity(code_input)

    # Penalise quality score by bugs/warnings
    bug_penalty     = len(result.get("bugs", [])) * 12
    warning_penalty = len(result.get("warnings", [])) * 5
    quality["overall"] = max(0, quality["overall"] - bug_penalty - warning_penalty)

    # Merge local detector results with AI results
    result["bugs"]     = local_result.get("bugs", [])     + result.get("bugs", [])
    result["warnings"] = local_result.get("warnings", []) + result.get("warnings", [])

    save_history(code_input, language, mode, result, quality)
    update_stats(language)

    status.success("✅ Analysis Complete")

    _show_quality_report(quality)
    _show_complexity_report(complexity)
    _show_detailed_progress(quality)
    _show_analysis_cards(result)
    _show_runtime_output(runtime_result, quality)
    _show_download_report(result, runtime_result, language, mode, quality)


# ─── Sub-sections ────────────────────────────────────────────────────────────

def _show_quality_report(quality):
    st.markdown("### ⭐ Code Quality Report")

    q1, q2, q3, q4, q5 = st.columns(5)
    q1.metric("🏆 Overall",         f"{quality['overall']}/100")
    q2.metric("📖 Readability",      quality['readability'])
    q3.metric("⚡ Performance",      quality['performance'])
    q4.metric("🔒 Security",         quality['security'])
    q5.metric("🛠 Maintainability",  quality['maintainability'])

    score = quality["overall"]
    if score >= 90:
        st.success("🟢 Production Ready")
    elif score >= 75:
        st.info("🔵 Good Quality")
    elif score >= 60:
        st.warning("🟡 Needs Optimization")
    else:
        st.error("🔴 High Risk Code")


def _show_complexity_report(complexity):
    st.markdown("### ⏱ Complexity Analysis")

    c1, c2, c3 = st.columns(3)
    c1.metric("⏱ Time Complexity",  complexity["time"])
    c2.metric("💾 Space Complexity", complexity["space"])
    c3.metric("🔥 Complexity Level", complexity["level"])


def _show_detailed_progress(quality):
    st.markdown("### 📊 Detailed Analysis")

    st.progress(quality["readability"] / 100)
    st.caption(f"📖 Readability : {quality['readability']}%")

    st.progress(quality["maintainability"] / 100)
    st.caption(f"🛠 Maintainability : {quality['maintainability']}%")

    st.progress(quality["performance"] / 100)
    st.caption(f"⚡ Performance : {quality['performance']}%")

    st.progress(quality["security"] / 100)
    st.caption(f"🔒 Security : {quality['security']}%")


def _show_analysis_cards(result):
    st.markdown(f'''
<div class="summary-box">
<h3>📌 Summary</h3>
<p>{result.get("summary", "")}</p>
</div>
''', unsafe_allow_html=True)

    if result.get("bugs"):
        st.subheader("🔴 Bugs")
        for item in result["bugs"]:
            st.markdown(f'<div class="card bug">{item}</div>', unsafe_allow_html=True)

    if result.get("warnings"):
        st.subheader("🟡 Warnings")
        for item in result["warnings"]:
            st.markdown(f'<div class="card warning">{item}</div>', unsafe_allow_html=True)

    if result.get("fixes"):
        st.subheader("🟢 Fixes")
        for item in result["fixes"]:
            st.markdown(f'<div class="card fix">{item}</div>', unsafe_allow_html=True)


def _show_runtime_output(runtime_result, quality):
    if not runtime_result:
        return

    st.subheader("⚡ Runtime Output")

    if runtime_result["output"]:
        st.code(runtime_result["output"], language="text")

    if runtime_result["error"]:
        st.error(runtime_result["error"])

    st.markdown("### 📊 Code Quality Score")
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("🏆 Overall",     f"{quality['overall']}%")
    q2.metric("📖 Readability", f"{quality['readability']}%")
    q3.metric("⚡ Performance", f"{quality['performance']}%")
    q4.metric("🔒 Security",    f"{quality['security']}%")


def _show_download_report(result, runtime_result, language, mode, quality):
    runtime_text = ""
    if runtime_result:
        runtime_text = (
            f"\nOUTPUT:\n{runtime_result.get('output', '')}"
            f"\n\nERROR:\n{runtime_result.get('error', '')}"
        )

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

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name=f"codelens_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )
