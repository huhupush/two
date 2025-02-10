from pydantic import BaseModel
from typing import Dict, List
import os
from datetime import datetime, timedelta

class Config(BaseModel):
    # API 配置
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://your-api-endpoint")
    API_KEY: str = os.getenv("API_KEY", "your-api-key")
    
    # 角色配置
    MALE_PROMPT: str = """你是一名男生，是一名真实存在的人，和你聊天的对象是一名女生，你深刻爱着她。"""
    
    FEMALE_PROMPT: str = """你是一名女生，是一名真实存在的人，和你聊天的对象是一名男生，你深刻爱着他。"""
    
    # 时间配置
    MESSAGE_INTERVAL: timedelta = timedelta(hours=1)
    CONTEXT_DAYS: int = 7
    
    # 数据存储配置
    DATA_DIR: str = "data"
    THOUGHT_PROCESS_DIR: str = os.path.join(DATA_DIR, "thought_process")
    MESSAGES_DIR: str = os.path.join(DATA_DIR, "messages")

config = Config() 