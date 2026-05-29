import streamlit as st
from utils import reset_all_data


def render_settings_tab():
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
    _render_reset_section()


def _render_reset_section():
    st.subheader("🗑 Reset Data")
    st.warning("This will permanently delete all analytics and history data.")

    confirm = st.checkbox("I understand this action cannot be undone")

    if confirm:
        if st.button("🚨 Reset All Data"):
            reset_all_data()
            st.success("✅ All analytics and history data reset successfully!")
            st.rerun()
