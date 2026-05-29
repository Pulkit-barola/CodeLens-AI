import json
import streamlit as st
from utils import load_stats


def render_dashboard_tab():
    st.markdown("""
    <div style="
        padding:25px; border-radius:18px;
        background:linear-gradient(90deg, #0f172a, #1e293b);
        border:1px solid #30363d; margin-bottom:20px;
    ">
        <h1 style="margin:0; color:#58a6ff;">📊 Analytics Dashboard</h1>
        <p style="color:#9ca3af; margin-top:10px;">Monitor usage, language trends and activity.</p>
    </div>
    """, unsafe_allow_html=True)

    stats = load_stats()

    if stats is None:
        st.info("No analytics data yet. Analyze some code first!")
        return

    try:
        _show_summary_metrics(stats)
        _show_language_cards(stats)
        _show_chart(stats)
        _show_export_buttons(stats)
    except Exception:
        st.warning("Dashboard data unavailable.")


# ─── Sub-sections ────────────────────────────────────────────────────────────

def _show_summary_metrics(stats):
    languages_used = sum([
        1 if stats["python"]     else 0,
        1 if stats["javascript"] else 0,
        1 if stats["java"]       else 0,
        1 if stats["cpp"]        else 0,
        1 if stats["sql"]        else 0,
    ])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📈 Total Analyses</div>
            <div class="metric-value">{stats['total_analyses']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🌎 Languages Used</div>
            <div class="metric-value">{languages_used}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")


def _lang_card(bg, border, emoji, label, count):
    return f"""
    <div style="
        background:{bg}; border:1px solid {border};
        border-radius:16px; padding:20px; color:white;
        text-align:center; margin-bottom:15px;
    ">
        <div style="font-size:18px; font-weight:600;">{emoji} {label}</div>
        {count}
    </div>
    """


def _show_language_cards(stats):
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(_lang_card("#166534",                         "#22c55e", "🐍", "Python",     stats["python"]),     unsafe_allow_html=True)
        st.markdown(_lang_card("linear-gradient(135deg,#7c2d12,#ea580c)", "#fb923c", "☕", "Java",       stats["java"]),       unsafe_allow_html=True)
        st.markdown(_lang_card("linear-gradient(135deg,#581c87,#9333ea)", "#c084fc", "📓", "SQL",        stats["sql"]),        unsafe_allow_html=True)

    with c2:
        st.markdown(_lang_card("linear-gradient(135deg,#854d0e,#ca8a04)", "#facc15", "🟨", "JavaScript", stats["javascript"]), unsafe_allow_html=True)
        st.markdown(_lang_card("linear-gradient(135deg,#1e3a8a,#2563eb)", "#60a5fa", "⚙️", "C++",        stats["cpp"]),        unsafe_allow_html=True)


def _show_chart(stats):
    import pandas as pd
    import plotly.express as px

    st.markdown("---")
    st.subheader("📈 Language Usage Chart")

    chart_data = pd.DataFrame({
        "Language": ["Python", "JavaScript", "Java", "C++", "SQL"],
        "Count":    [stats["python"], stats["javascript"], stats["java"], stats["cpp"], stats["sql"]]
    })

    fig = px.bar(chart_data, x="Language", y="Count", title="Language Usage Analytics")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    chart_image = fig.to_image(format="png")
    st.download_button(
        label="📊 Download Chart PNG",
        data=chart_image,
        file_name="language_usage_chart.png",
        mime="image/png"
    )


def _show_export_buttons(stats):
    import pandas as pd

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
        export_df = pd.DataFrame({
            "Language": ["Python", "JavaScript", "Java", "C++", "SQL"],
            "Count":    [stats["python"], stats["javascript"], stats["java"], stats["cpp"], stats["sql"]]
        })
        st.download_button(
            "📥 Download CSV",
            data=export_df.to_csv(index=False),
            file_name="analytics.csv",
            mime="text/csv"
        )
