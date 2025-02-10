from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable, Any
from openai import OpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.callbacks import BaseCallbackHandler
from ..models.message import Message
from ..config.prompts import Prompts
from ..config.settings import Config
from .storage_service import StorageService
import os

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

class StreamingCallbackHandler:
    """处理流式输出的回调处理器"""
    
    def __init__(self, thought_callback: Callable[[str], Any], content_callback: Callable[[str], Any]):
        self.thought_callback = thought_callback
        self.content_callback = content_callback
        
    def process_chunk(self, chunk) -> None:
        """处理新的输出chunk"""
        # 处理思维链内容
        if hasattr(chunk.choices[0].delta, 'reasoning_content'):
            if chunk.choices[0].delta.reasoning_content:
                self.thought_callback(chunk.choices[0].delta.reasoning_content)
                
        # 处理模型返回的实际内容
        if hasattr(chunk.choices[0].delta, 'content'):
            if chunk.choices[0].delta.content:
                self.content_callback(chunk.choices[0].delta.content)

class ChatService:
    def __init__(self, storage_service: StorageService, model_config: dict):
        self.storage = storage_service
        
        model_type = Config().MODEL_TYPE
        
        if model_type == "openai":
            # 初始化OpenAI客户端
            self.client = OpenAI(
                api_key=model_config.get("api_key"),
                base_url=model_config.get("base_url")
            )
            self.model_name = model_config.get("model_name", "gpt-3.5-turbo")
            self.temperature = model_config.get("temperature", 0.7)
            self.max_tokens = model_config.get("max_tokens", 1000)
        else:  # ollama
            if not all(key in model_config for key in ["base_url", "model"]):
                raise ValueError("Missing required Ollama configuration")
            
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

    def generate_message(self, sender: str, thought_callback: Callable[[str], Any] = None, 
                        content_callback: Callable[[str], Any] = None) -> Dict:
        """生成新的消息，支持流式输出
        
        Args:
            sender: 发送者角色
            thought_callback: 处理思维过程流式输出的回调函数
            content_callback: 处理内容流式输出的回调函数
            
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
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"这是最近的对话记录：\n{context_text}\n\n根据以上对话和你的角色，请回复一条消息。"}
            ]
            
            # 创建回调处理器
            callback_handler = None
            if thought_callback and content_callback:
                callback_handler = StreamingCallbackHandler(thought_callback, content_callback)
            
            # 使用流式API生成回复
            full_content = ""
            thought_content = ""
            
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
                response_format={"type": "text"}
            )
            
            # 处理流式输出
            for chunk in stream:
                if callback_handler:
                    callback_handler.process_chunk(chunk)
                    
                # 收集思维链内容
                if hasattr(chunk.choices[0].delta, 'reasoning_content'):
                    if chunk.choices[0].delta.reasoning_content:
                        thought_content += chunk.choices[0].delta.reasoning_content
                
                # 收集实际内容
                if hasattr(chunk.choices[0].delta, 'content'):
                    if chunk.choices[0].delta.content:
                        full_content += chunk.choices[0].delta.content
            
            # 创建消息对象
            timestamp = datetime.now()
            message = Message(
                content=full_content.strip(),
                sender=sender,
                timestamp=timestamp,
                thought_process=thought_content.strip()
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