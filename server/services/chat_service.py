from datetime import datetime, timedelta
from typing import List, Dict, Optional
from langchain_community.chat_models import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from ..models.message import Message
from ..config.prompts import Prompts
from ..config.settings import Config
from .storage_service import StorageService
import os
import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config import config

class MessageProcessor:
    @staticmethod
    def clean_content(content: str) -> tuple[str, str]:
        """分离思考过程和实际回复"""
        try:
            # 检查两种可能的标签
            if "<think>" in content and "</think>" in content:
                thought_start = content.find("<think>") + len("<think>")
                thought_end = content.find("</think>")
                thought_process = content[thought_start:thought_end].strip()
                clean_content = content[thought_end + len("</think>"):].strip()
            elif "<thought>" in content and "</thought>" in content:
                thought_start = content.find("<thought>") + len("<thought>")
                thought_end = content.find("</thought>")
                thought_process = content[thought_start:thought_end].strip()
                clean_content = content[thought_end + len("</thought>"):].strip()
            else:
                thought_process = ""
                clean_content = content.strip()
            return clean_content, thought_process
        except Exception as e:
            print(f"Error in clean_content: {e}")
            return content.strip(), ""

class ChatService:
    def __init__(self, storage_service: StorageService, model_config: dict):
        self.storage = storage_service
        
        model_type = Config().MODEL_TYPE
        
        if model_type == "openai":
            # 从 model_config 中移除代理设置
            openai_config = model_config.copy()
            if 'proxies' in openai_config:
                # 如果需要代理，通过环境变量设置
                os.environ['HTTP_PROXY'] = openai_config['proxies'].get('http', '')
                os.environ['HTTPS_PROXY'] = openai_config['proxies'].get('https', '')
                del openai_config['proxies']
            
            # 确保必要的参数存在
            if not openai_config.get("api_key"):
                raise ValueError("OpenAI API key is required")
            if not openai_config.get("base_url"):
                raise ValueError("API base URL is required")
            if not openai_config.get("model_name"):
                raise ValueError("Model name is required")
            
            self.llm = ChatOpenAI(**openai_config)
        else:  # ollama
            # 确保必要的参数存在
            if not model_config.get("base_url"):
                raise ValueError("Ollama base URL is required")
            if not model_config.get("model"):
                raise ValueError("Model name is required")
            
            self.llm = ChatOllama(**model_config)

    def _get_context(self, days: int = None) -> List[Dict]:
        """获取历史对话上下文
        
        Args:
            days: 获取最近几天的对话记录，默认使用配置中的值
            
        Returns:
            List[Dict]: 历史消息列表
        """
        if days is None:
            days = Config().CONTEXT_DAYS
            
        context = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取日期范围内的所有消息
        messages = self.storage.get_messages_in_range(start_date, end_date)
        
        # 按时间排序
        messages.sort(key=lambda x: x.timestamp)
        
        # 只保留最近的 N 条消息
        max_messages = Config().MAX_HISTORY_MESSAGES or 50
        if len(messages) > max_messages:
            messages = messages[-max_messages:]
            
        return messages

    def _format_context(self, messages: List[Message]) -> str:
        """格式化上下文消息"""
        return "\n".join([
            f"{msg.sender}: {msg.content}"
            for msg in messages
        ])

    def generate_message(self, sender: str) -> Dict:
        """生成新的消息
        
        Args:
            sender: 发送者角色
            
        Returns:
            Dict: 生成的消息
        """
        try:
            # 获取历史上下文
            context = self._get_context()
            context_text = self._format_context(context)
            
            # 获取角色提示词
            prompts = Prompts()
            system_prompt = prompts.get_role_prompt(sender)
            
            # 构建消息列表
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"这是最近的对话记录：\n{context_text}\n\n根据以上对话和你的角色，请回复一条消息：")
            ]
            
            # 生成回复
            response = self.llm.invoke(messages)
            content = response.content
            
            # 分离思考过程和实际回复
            clean_content, thought_process = MessageProcessor.clean_content(content)
            
            print(f"原始内容: {content}")
            print(f"思考过程: {thought_process}")
            print(f"实际回复: {clean_content}")
            
            # 创建消息对象
            timestamp = datetime.now()
            message = Message(
                content=clean_content,
                sender=sender,
                timestamp=timestamp,
                thought_process=thought_process
            )
            
            # 保存消息
            self.storage.save_message(message)
            
            return message.to_dict()
            
        except Exception as e:
            print(f"Error in generate_message: {e}")
            return {"error": str(e)}

    def get_messages_by_date(self, date: datetime.date) -> List[Message]:
        """获取指定日期的消息"""
        messages = self.storage.get_messages_by_date(date)
        if not messages:
            return []
        return [Message.from_dict(msg) for msg in messages]

    def should_generate_message(self, last_message: Optional[Message] = None) -> bool:
        """检查是否应该生成新消息"""
        if not last_message:
            return True
            
        time_diff = datetime.now() - last_message.timestamp
        return time_diff.total_seconds() >= 3600  # 1小时 