import streamlit as st
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.services.chat_service import ChatService
from server.services.storage_service import StorageService
from server.models.message import Message

# 加载环境变量
load_dotenv()

st.set_page_config(
    page_title="Two - 对话",
    page_icon="💬",
    layout="wide"
)

def get_role_display_name(role: str) -> str:
    """获取角色显示名称"""
    return "男生" if role == "male" else "女生"

def init_services():
    """初始化服务"""
    # 设置存储目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    messages_dir = os.path.join(base_dir, "data", "messages")
    thought_process_dir = os.path.join(base_dir, "data", "thought_process")
    
    # 确保目录存在
    os.makedirs(messages_dir, exist_ok=True)
    os.makedirs(thought_process_dir, exist_ok=True)
    
    # 初始化服务
    storage_service = StorageService(
        messages_dir=messages_dir,
        thought_process_dir=thought_process_dir
    )
    
    model_config = {
        "model_name": os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
        "temperature": float(os.getenv("TEMPERATURE", "0.7")),
        "api_key": os.getenv("API_KEY"),
        "base_url": os.getenv("API_BASE_URL"),
    }
    
    chat_service = ChatService(storage_service, model_config)
    return chat_service

def main():
    st.title("Two")
    
    # 初始化服务
    chat_service = init_services()
    
    # 初始化 session state
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False
    if "should_rerun" not in st.session_state:
        st.session_state.should_rerun = False
        
    # 定义回调函数
    def send_message():
        if st.session_state.user_input:
            # 保存用户消息
            user_message = Message(
                content=st.session_state.user_input,
                sender=st.session_state.current_role,
                timestamp=datetime.now()
            )
            chat_service.storage.save_message(user_message)
            # 清空输入框并标记需要刷新
            st.session_state.user_input = ""
            st.session_state.should_rerun = True
            
    # 保存当前角色到 session state
    role = st.sidebar.radio(
        "选择你的角色",
        ["male", "female"],
        format_func=get_role_display_name,
        key="current_role"
    )
    
    # 添加日期选择器
    today = datetime.now().date()
    selected_date = st.sidebar.date_input(
        "选择日期",
        value=today,
        max_value=today
    )
    
    # 显示历史消息
    messages = chat_service.get_messages_by_date(selected_date)
    
    # 获取最近一条消息的发送者
    last_sender = messages[-1].sender if messages else None
    
    message_container = st.container()
    
    with message_container:
        if not messages:
            st.info("这一天还没有任何对话，开始聊天吧！", icon="💭")
        else:
            for msg in messages:
                with st.chat_message(msg.sender):
                    st.write(msg.content)
    
    # 用户输入区域
    col1, col2, col3 = st.columns([4, 1, 1])
    
    with col1:
        st.text_area(
            "输入你的消息...", 
            key="user_input",
            height=100,
            disabled=st.session_state.is_generating,
            on_change=send_message
        )
    
    # 发送消息按钮
    with col2:
        st.write("")  # 添加一些空间使按钮对齐
        st.write("")
        if st.button(
            "发送消息",
            use_container_width=True,
            disabled=st.session_state.is_generating or not st.session_state.user_input,
            on_click=send_message
        ):
            pass
    
    # 生成回复按钮
    with col3:
        st.write("")  # 添加一些空间使按钮对齐
        st.write("")
        male_button = st.button(
            "生成男生回复",
            use_container_width=True,
            disabled=st.session_state.is_generating or last_sender == "male"
        )
        female_button = st.button(
            "生成女生回复",
            use_container_width=True,
            disabled=st.session_state.is_generating or last_sender == "female"
        )
    
    # 处理生成回复
    if male_button or female_button:
        target_role = "male" if male_button else "female"
        role_name = get_role_display_name(target_role)
        
        # 设置生成状态
        st.session_state.is_generating = True
        
        # 显示生成状态
        with message_container:
            with st.chat_message(target_role):
                with st.status(f"正在生成{role_name}的回复...", expanded=True) as status:
                    st.write(f"✨ {role_name}正在思考中...")
                    # 生成回复
                    response = chat_service.generate_message(target_role)
                    st.write(f"💫 {role_name}写好了回复")
                    status.update(label=f"{role_name}的回复已生成", state="complete")
                    
                # 显示回复内容
                st.write(response.content)
        
        # 重置生成状态
        st.session_state.is_generating = False
        
        # 刷新页面以显示新消息
        st.rerun()
        
    # 如果需要刷新页面
    if st.session_state.should_rerun:
        st.session_state.should_rerun = False
        st.rerun()

if __name__ == "__main__":
    main() 