import streamlit as st
from utils import load_history


def render_history_tab():
    st.subheader("📜 Analysis History")

    history = load_history()

    if not history:
        st.info("No history yet.")
        return

    for item in history:
        label = f"{item['language']} • Score: {item.get('score', 0)} • {item['time']}"
        with st.expander(label):
            st.code(item["code"], language=item["language"].lower())
            st.markdown(f"### Summary\n\n{item['summary']}")
