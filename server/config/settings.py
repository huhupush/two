from pydantic import BaseModel
import os
from datetime import timedelta
from dotenv import load_dotenv, find_dotenv

# 加载 .env 文件
print("当前工作目录:", os.getcwd())
dotenv_path = find_dotenv()
print(".env 文件路径:", dotenv_path)
print(".env 文件是否存在:", os.path.exists(dotenv_path))
print("环境变量加载前 API_KEY:", os.getenv("API_KEY"))
load_dotenv(dotenv_path, override=True, verbose=True)
print("环境变量加载后 API_KEY:", os.getenv("API_KEY"))

class Config(BaseModel):
    # API 配置
    API_BASE_URL: str = os.getenv("API_BASE_URL")
    API_KEY: str = os.getenv("API_KEY")
    
    @property
    def api_key(self) -> str:
        key = os.getenv("API_KEY")
        print("Config 中获取的 API_KEY:", key)
        if not key:
            raise ValueError("API_KEY 环境变量未设置")
        return key

    # 代理配置
    HTTP_PROXY: str = os.getenv("HTTP_PROXY", "")
    HTTPS_PROXY: str = os.getenv("HTTPS_PROXY", "")
    
    # 时间配置
    MESSAGE_INTERVAL: timedelta = timedelta(hours=1)
    CONTEXT_DAYS: int = 7
    MAX_HISTORY_MESSAGES: int = int(os.getenv("MAX_HISTORY_MESSAGES", "50"))  # 历史消息最大条数
    
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
                "api_key": self.api_key,
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