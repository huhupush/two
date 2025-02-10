from pydantic import BaseModel
from typing import Dict, List, Optional
import os
from datetime import datetime, timedelta

class AIModelConfig(BaseModel):
    """AI模型配置"""
    provider: str = os.getenv("AI_PROVIDER", "openai")  # openai 或 ollama
    api_base_url: str = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
    api_key: str = os.getenv("API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4")
    temperature: float = 0.7
    max_tokens: int = 1000

class DataStorageConfig(BaseModel):
    """数据存储配置"""
    base_dir: str = "data"
    messages_dir: str = os.path.join(base_dir, "messages")
    trajectories_dir: str = os.path.join(base_dir, "trajectories")
    config_dir: str = os.path.join(base_dir, "config")
    thought_process_dir: str = os.path.join(base_dir, "thought_process")

class ResearchConfig(BaseModel):
    """研究模块配置"""
    context_days: int = 7
    message_interval: timedelta = timedelta(hours=1)
    max_history_messages: int = 50
    trajectory_sample_rate: int = 5  # 轨迹采样率（秒）

class UIConfig(BaseModel):
    """UI配置"""
    page_title: str = "Two - AI 行为研究平台"
    theme: str = "light"
    language: str = "zh"
    enable_debug: bool = False

class Config(BaseModel):
    """全局配置"""
    ai_model: AIModelConfig = AIModelConfig()
    data_storage: DataStorageConfig = DataStorageConfig()
    research: ResearchConfig = ResearchConfig()
    ui: UIConfig = UIConfig()

    class Config:
        arbitrary_types_allowed = True

# 创建全局配置实例
config = Config()

# 确保必要的目录存在
for dir_path in [
    config.data_storage.messages_dir,
    config.data_storage.trajectories_dir,
    config.data_storage.config_dir,
    config.data_storage.thought_process_dir
]:
    os.makedirs(dir_path, exist_ok=True) 