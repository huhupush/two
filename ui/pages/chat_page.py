import streamlit as st
from datetime import datetime
from server.services.chat_service import ChatService
from ..components.message_display import render_message_list, render_thought_process

class ChatPage:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    def generate_message(self, messages):
        """生成消息的具体逻辑"""
        try:
            # 根据最后一条消息决定发送者
            last_sender = messages[-1].sender if messages else None
            sender = "female" if last_sender == "male" else "male"
            
            def update_thought(token: str):
                st.session_state.current_thought = token
                st.session_state.waiting_response = False
                st.session_state.is_generating = True
                st.session_state.is_thinking = True
                st.rerun()
                
            def update_content(token: str):
                st.session_state.current_content = token
                st.session_state.is_thinking = False
                st.rerun()
            
            # 生成消息
            message = self.chat_service.generate_message(
                sender,
                thought_callback=update_thought,
                content_callback=update_content
            )
            
            # 重置状态
            st.session_state.is_generating = False
            st.session_state.waiting_response = False
            st.session_state.current_thought = ""
            st.session_state.current_content = ""
            st.session_state.current_sender = None
            st.session_state.is_thinking = False
            st.rerun()
            
        except Exception as e:
            st.error(f"生成消息时出错: {str(e)}")
            st.session_state.is_generating = False
            st.session_state.waiting_response = False
            st.session_state.current_sender = None
            st.session_state.is_thinking = False

    def on_generate_click(self):
        """处理生成按钮点击事件"""
        st.session_state.waiting_response = True
        st.session_state.should_generate = True
        st.session_state.is_thinking = True

    def render(self):
        st.title("Two的对话")
        
        # 初始化状态
        if 'is_generating' not in st.session_state:
            st.session_state.is_generating = False
        if 'current_thought' not in st.session_state:
            st.session_state.current_thought = ""
        if 'current_content' not in st.session_state:
            st.session_state.current_content = ""
        if 'waiting_response' not in st.session_state:
            st.session_state.waiting_response = False
        if 'current_sender' not in st.session_state:
            st.session_state.current_sender = None
        if 'should_generate' not in st.session_state:
            st.session_state.should_generate = False
        if 'is_thinking' not in st.session_state:
            st.session_state.is_thinking = False
        
        # 选择日期
        selected_date = st.date_input(
            "选择日期",
            datetime.now().date()
        )
        
        # 获取并显示消息
        messages = self.chat_service.get_messages_by_date(selected_date)
        
        # 创建消息容器
        message_container = st.container()
        
        with message_container:
            # 显示历史消息
            render_message_list(messages, show_date=False)
            
            # 如果正在等待响应或生成中，显示相应状态
            if st.session_state.current_sender:
                with st.chat_message(st.session_state.current_sender):
                    if st.session_state.waiting_response:
                        with st.spinner("正在准备回复..."):
                            st.empty()
                    elif st.session_state.is_generating:
                        # 显示当前生成的内容
                        if st.session_state.current_content:
                            st.markdown(st.session_state.current_content)
                        
                        # 显示思考过程
                        with st.expander("思考过程", expanded=True):
                            if st.session_state.is_thinking:
                                col1, col2 = st.columns([1, 9])
                                with col1:
                                    st.spinner("思考中")
                                with col2:
                                    if st.session_state.current_thought:
                                        st.markdown(st.session_state.current_thought)
                            elif st.session_state.current_thought:
                                st.markdown(st.session_state.current_thought)
        
        # 手动触发消息生成
        st.button(
            "生成新消息",
            disabled=st.session_state.is_generating or st.session_state.waiting_response,
            on_click=self.on_generate_click
        )
        
        # 如果需要生成消息
        if st.session_state.should_generate and st.session_state.waiting_response:
            # 根据最后一条消息决定发送者
            last_sender = messages[-1].sender if messages else None
            sender = "female" if last_sender == "male" else "male"
            st.session_state.current_sender = sender
            
            # 开始生成
            st.session_state.should_generate = False
            self.generate_message(messages)

        # 显示提示信息
        st.sidebar.markdown("""
        ### 关于对话
        - 消息会在男生和女生之间自动交替
        - 可以查看每条消息的思维过程
        - 支持查看历史对话记录
        - 支持实时查看生成过程
        """) 