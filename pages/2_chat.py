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
    # 检查环境变量
    required_vars = {
        "MODEL_TYPE": os.getenv("MODEL_TYPE"),
        "MODEL_NAME": os.getenv("MODEL_NAME"),
        "API_KEY": os.getenv("API_KEY"),
        "API_BASE_URL": os.getenv("API_BASE_URL")
    }
    
    missing_vars = [key for key, value in required_vars.items() if not value]
    if missing_vars:
        st.error(f"缺少必要的环境变量: {', '.join(missing_vars)}")
        st.info("请确保已正确设置 .env 文件")
        return None
    
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
    
    # 获取模型类型
    model_type = os.getenv("MODEL_TYPE")
    
    if model_type == "openai":
        model_config = {
            "model_name": os.getenv("MODEL_NAME"),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "api_key": os.getenv("API_KEY"),
            "base_url": os.getenv("API_BASE_URL"),
            "max_tokens": int(os.getenv("MAX_TOKENS", "1000"))
        }
    else:  # ollama
        model_config = {
            "model": os.getenv("MODEL_NAME"),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        }
    
    try:
        chat_service = ChatService(storage_service, model_config)
        return chat_service
    except Exception as e:
        st.error(f"初始化服务失败: {str(e)}")
        return None

def main():
    st.title("Two")
    
    # 初始化服务
    chat_service = init_services()
    if not chat_service:
        st.stop()
    
    # 初始化 session state
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False
    if "should_rerun" not in st.session_state:
        st.session_state.should_rerun = False
    if "current_thought" not in st.session_state:
        st.session_state.current_thought = ""
    if "current_content" not in st.session_state:
        st.session_state.current_content = ""
        
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
        st.session_state.current_thought = ""
        st.session_state.current_content = ""
        
        # 创建占位符
        with message_container:
            with st.chat_message(target_role):
                message_placeholder = st.empty()
                thought_expander = st.expander("✨正在思考...", expanded=False)
                expander_container = thought_expander.empty()
                def update_thought(token: str):
                    st.session_state.current_thought += token
                        
                def update_content(token: str):
                    expander_container.empty()
                    st.session_state.current_content += token
                    message_placeholder.markdown(st.session_state.current_content)
                
                # 生成回复
                response = chat_service.generate_message(
                    target_role,
                    thought_callback=update_thought,
                    content_callback=update_content
                )
                
                if "error" in response:
                    st.error(f"生成回复时出错: {response['error']}")
        
        # 重置生成状态
        st.session_state.is_generating = False
        st.session_state.current_thought = ""
        st.session_state.current_content = ""
        
        # 刷新页面以显示新消息
        st.rerun()
        
    # 如果需要刷新页面
    if st.session_state.should_rerun:
        st.session_state.should_rerun = False
        st.rerun()

if __name__ == "__main__":
    main() 