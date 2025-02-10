import json
import os
from datetime import datetime, timedelta
from typing import List, Optional
from ..models.message import Message

class StorageService:
    def __init__(self, messages_dir: str, thought_process_dir: str):
        self.messages_dir = messages_dir
        self.thought_process_dir = thought_process_dir
        self._ensure_directories()

    def _ensure_directories(self):
        """确保必要的目录存在"""
        os.makedirs(self.messages_dir, exist_ok=True)
        os.makedirs(self.thought_process_dir, exist_ok=True)

    def _get_file_path(self, date: datetime, is_thought_process: bool = False) -> str:
        """获取指定日期的文件路径"""
        directory = self.thought_process_dir if is_thought_process else self.messages_dir
        return os.path.join(directory, f"{date.strftime('%Y-%m-%d')}.json")

    def save_message(self, message: Message):
        """保存消息和思维过程"""
        # 保存消息
        message_file = self._get_file_path(message.timestamp)
        messages = self.get_messages_by_date(message.timestamp.date()) or []
        messages.append(message.to_dict())
        
        with open(message_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)

        # 如果有思维过程，单独保存
        if message.thought_process:
            thought_file = self._get_file_path(message.timestamp, True)
            thoughts = self.get_thoughts_by_date(message.timestamp.date()) or []
            thoughts.append(message.to_dict())
            
            with open(thought_file, 'w', encoding='utf-8') as f:
                json.dump(thoughts, f, ensure_ascii=False, indent=2)

    def get_messages_by_date(self, date: datetime.date) -> Optional[List[dict]]:
        """获取指定日期的消息"""
        file_path = self._get_file_path(datetime.combine(date, datetime.min.time()))
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_messages_in_range(self, start_date: datetime, end_date: datetime) -> List[Message]:
        """获取指定日期范围内的所有消息
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            List[Message]: 消息列表
        """
        messages = []
        current_date = start_date.date()
        
        while current_date <= end_date.date():
            daily_messages = self.get_messages_by_date(current_date)
            if daily_messages:
                for msg_dict in daily_messages:
                    # 转换时间戳字符串为 datetime 对象
                    msg_dict['timestamp'] = datetime.fromisoformat(msg_dict['timestamp'])
                    msg = Message.from_dict(msg_dict)
                    # 只添加在时间范围内的消息
                    if start_date <= msg.timestamp <= end_date:
                        messages.append(msg)
            current_date += timedelta(days=1)
            
        return messages

    def get_thoughts_by_date(self, date: datetime.date) -> Optional[List[dict]]:
        """获取指定日期的思维过程"""
        file_path = self._get_file_path(datetime.combine(date, datetime.min.time()), True)
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_recent_messages(self, days: int = 7) -> List[Message]:
        """获取最近几天的消息"""
        messages = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        current_date = start_date
        while current_date <= end_date:
            day_messages = self.get_messages_by_date(current_date.date())
            if day_messages:
                messages.extend([Message.from_dict(msg) for msg in day_messages])
            current_date += timedelta(days=1)
        
        return sorted(messages, key=lambda x: x.timestamp) 