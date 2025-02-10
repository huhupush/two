import streamlit as st
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.pages.prompt_config_page import PromptConfigPage

st.set_page_config(
    page_title="Two - 配置",
    page_icon="🔧",
    layout="wide"
)

config_page = PromptConfigPage()
config_page.render() 