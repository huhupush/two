import streamlit as st
from datetime import datetime
from typing import List
from server.models.message import Message

def render_message(message: Message):
    """渲染单条消息"""
    with st.chat_message(message.sender):
        st.write(f"{message.timestamp.strftime('%H:%M')} - {message.content}")

def render_message_list(messages: List[Message], show_date: bool = True):
    """渲染消息列表"""
    if not messages:
        st.info("这一天还没有对话记录")
        return

    current_date = None
    for message in sorted(messages, key=lambda x: x.timestamp):
        message_date = message.timestamp.date()
        
        # 显示日期分隔符
        if show_date and current_date != message_date:
            st.markdown(f"### {message_date.strftime('%Y-%m-%d')}")
            current_date = message_date
        
        render_message(message)

def render_thought_process(message: Message):
    """渲染思维过程（仅在展开时显示）"""
    if message.thought_process:
        with st.expander("查看思维过程"):
            st.write(message.thought_process) 