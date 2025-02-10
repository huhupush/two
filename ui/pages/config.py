import streamlit as st
from .prompt_config_page import PromptConfigPage

def show():
    """显示配置页面"""
    st.set_page_config(
        page_title="Two聊天 - 配置",
        page_icon="⚙️",
        layout="wide"
    )
    
    config_page = PromptConfigPage()
    config_page.render() 