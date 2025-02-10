from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Tuple
import re

class Message(BaseModel):
    content: str
    sender: str
    timestamp: datetime
    thought_process: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        if isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        
        # 如果content中包含思考内容，将其提取到thought_process中
        if '<think>' in data['content']:
            content = data['content']
            thought_matches = re.findall(r'<think>(.*?)</think>', content, re.DOTALL)
            if thought_matches:
                data['thought_process'] = '\n'.join(thought_matches)
                # 移除所有<think>标签及其内容
                data['content'] = re.sub(r'<think>.*?</think>\n?', '', content, flags=re.DOTALL).strip()
        
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            'content': self.content,
            'sender': self.sender,
            'timestamp': self.timestamp.isoformat(),
            'thought_process': self.thought_process
        }

    @staticmethod
    def clean_content(content: str) -> Tuple[str, Optional[str]]:
        """分离内容中的思考过程和实际回复"""
        thought_process = None
        if '<think>' in content:
            thought_matches = re.findall(r'<think>(.*?)</think>', content, re.DOTALL)
            if thought_matches:
                thought_process = '\n'.join(thought_matches)
                # 移除所有<think>标签及其内容
                content = re.sub(r'<think>.*?</think>\n?', '', content, flags=re.DOTALL).strip()
        
        return content, thought_process 