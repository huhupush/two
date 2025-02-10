from pydantic import BaseModel
import os
from datetime import timedelta

class Config(BaseModel):
    # API 配置
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    API_KEY: str = os.getenv("API_KEY", "sk-ac6909c6000a469ab4170b4eafa59b07")

    # 代理配置
    HTTP_PROXY: str = os.getenv("HTTP_PROXY", "")
    HTTPS_PROXY: str = os.getenv("HTTPS_PROXY", "")
    
    # 时间配置
    MESSAGE_INTERVAL: timedelta = timedelta(hours=1)
    CONTEXT_DAYS: int = 7
    
    # 数据存储配置
    DATA_DIR: str = "data"
    THOUGHT_PROCESS_DIR: str = os.path.join(DATA_DIR, "thought_process")
    MESSAGES_DIR: str = os.path.join(DATA_DIR, "messages")
    
    # 模型配置
    MODEL_TYPE: str = os.getenv("MODEL_TYPE", "openai")  # 可选值: openai, ollama
    MODEL_NAME: str = os.getenv("MODEL_NAME", "deepseek-r1")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1000"))
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def get_model_config(self) -> dict:
        """获取模型配置"""
        if self.MODEL_TYPE == "openai":
            config = {
                "model_name": self.MODEL_NAME,
                "temperature": self.TEMPERATURE,
                "max_tokens": self.MAX_TOKENS,
                "api_key": self.API_KEY,
                "base_url": self.API_BASE_URL,
            }
            
            # 如果设置了代理，添加代理配置
            if self.HTTP_PROXY or self.HTTPS_PROXY:
                config["proxies"] = {
                    "http": self.HTTP_PROXY,
                    "https": self.HTTPS_PROXY
                }
        else:  # ollama
            config = {
                "model": self.MODEL_NAME,
                "temperature": self.TEMPERATURE,
                "base_url": self.OLLAMA_BASE_URL,
            }
            
        return config

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8" 