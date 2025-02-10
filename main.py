import streamlit as st
from server.services.chat_service import ChatService
from server.services.storage_service import StorageService
from datetime import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 检查必要的环境变量
def check_environment():
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
        return False
    return True

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
    
    # 获取模型类型
    model_type = os.getenv("MODEL_TYPE")
    
    if model_type == "openai":
        model_config = {
            "model": os.getenv("MODEL_NAME"),
            "temperature": float(os.getenv("TEMPERATURE", "0.7")),
            "openai_api_key": os.getenv("API_KEY"),
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
    """主页面"""
    st.set_page_config(
        page_title="Two聊天",
        page_icon="🌌",
        layout="wide"
    )
    
    if not check_environment():
        return
    
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