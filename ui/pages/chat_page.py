import streamlit as st
from datetime import datetime
from server.services.chat_service import ChatService
from ..components.message_display import render_message_list, render_thought_process

class ChatPage:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    def render(self):
        st.title("Two的对话")
        
        # 初始化生成锁
        if 'is_generating' not in st.session_state:
            st.session_state.is_generating = False
        
        # 选择日期
        selected_date = st.date_input(
            "选择日期",
            datetime.now().date()
        )
        
        # 获取并显示消息
        messages = self.chat_service.get_messages_by_date(selected_date)
        render_message_list(messages, show_date=False)
        
        # 显示生成状态
        if st.session_state.is_generating:
            st.warning("正在生成消息，请稍候...")
        
        # 手动触发消息生成
        if st.button("生成新消息", disabled=st.session_state.is_generating):
            if not st.session_state.is_generating:
                try:
                    st.session_state.is_generating = True
                    # 根据最后一条消息决定发送者
                    last_sender = messages[-1].sender if messages else None
                    sender = "female" if last_sender == "male" else "male"
                    
                    with st.spinner(f"正在生成{'他' if sender == 'male' else '她'}的消息..."):
                        message = self.chat_service.generate_message(sender)
                        render_thought_process(message)
                        st.rerun()
                finally:
                    st.session_state.is_generating = False

        # 显示提示信息
        st.sidebar.markdown("""
        ### 关于对话
        - 消息会在男生和女生之间自动交替
        - 可以查看每条消息的思维过程
        - 支持查看历史对话记录
        """) 