import streamlit as st
from ui.chat import render_chat
from ui.config import LAYOUT, PAGE_ICON, PAGE_TITLE
from ui.sidebar import render_sidebar
from ui.state import init_session_state

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
)

init_session_state()
render_sidebar()
render_chat()
