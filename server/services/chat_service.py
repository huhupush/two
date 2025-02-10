from datetime import datetime
from typing import List, Optional
from langchain_community.chat_models import ChatOpenAI, ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from ..models.message import Message
from ..config.prompts import Prompts
from ..config.settings import Config
from .storage_service import StorageService
import os

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
                
            self.llm = ChatOpenAI(**openai_config)
        else:  # ollama
            self.llm = ChatOllama(**model_config)

    def _format_context(self, messages: List[Message]) -> str:
        """格式化上下文消息"""
        return "\n".join([
            f"{msg.sender}: {msg.content}"
            for msg in messages
        ])

    def generate_message(self, sender: str) -> Message:
        """生成新消息"""
        # 获取历史消息作为上下文
        context_messages = self.storage.get_recent_messages()
        context_text = self._format_context(context_messages)
        
        # 构建提示
        system_prompt = Prompts.get_role_prompt(sender)
        context_prompt = Prompts.get_context_prompt(sender, context_text)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=context_prompt)
        ]
        
        # 生成回复
        response = self.llm.invoke(messages)
        
        # 创建消息对象
        message = Message(
            content=response.content,
            sender=sender,
            timestamp=datetime.now(),
            thought_process=response.additional_kwargs.get('thought_process', '')
        )
        
        # 保存消息
        self.storage.save_message(message)
        
        return message

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