import streamlit as st
from server.services.chat_service import ChatService
from server.services.storage_service import StorageService
from datetime import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def init_services():
    """初始化服务"""
    # 设置存储目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
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
    """主页面"""
    st.set_page_config(
        page_title="Two聊天",
        page_icon="🌌",
        layout="wide"
    )
    
    st.title("Two聊天")
    st.markdown("""
    欢迎来到Two聊天系统！在这里，你可以体验跨越时空的对话。
    
    ### 功能介绍
    - 🗣️ 与Two中的另一个自己对话
    - ⚙️ 自定义对话风格和个性
    - 💾 自动保存对话历史
    - 🎭 角色切换功能
    
    ### 使用说明
    1. 点击左侧边栏的"🔧 配置"页面来自定义对话设置
    2. 点击左侧边栏的"💬 聊天"页面开始对话
    3. 系统会自动保存对话历史
    """)
    
    # 初始化服务（确保数据目录存在）
    init_services()

if __name__ == "__main__":
    main() 