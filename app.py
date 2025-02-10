import json
import os
from datetime import datetime, timedelta
from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config import config
import streamlit as st
from langchain.schema import Message

class ParallelUniverseChat:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=config.API_BASE_URL,
            api_key=config.API_KEY,
            model_name=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS
        )
        
        # 创建必要的目录
        os.makedirs(config.THOUGHT_PROCESS_DIR, exist_ok=True)
        os.makedirs(config.MESSAGES_DIR, exist_ok=True)

    def _get_context(self, days: int = None) -> List[Dict]:
        if days is None:
            days = config.CONTEXT_DAYS
            
        context = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        for day in range(days):
            current_date = (end_date - timedelta(days=day)).strftime("%Y-%m-%d")
            file_path = os.path.join(config.MESSAGES_DIR, f"{current_date}.json")
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    day_messages = json.load(f)
                    context.extend(day_messages)
        
        return context[-10:]  # 只返回最近的10条消息作为上下文

    def generate_message(self, sender: str) -> Dict:
        context = self._get_context()
        
        # 构建提示
        system_prompt = config.MALE_PROMPT if sender == "male" else config.FEMALE_PROMPT
        context_text = "\n".join([
            f"{msg['sender']}: {msg['content']}" 
            for msg in context
        ])
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"这是最近的对话记录：\n{context_text}\n\n根据以上对话和你的角色，请回复一条消息：")
        ]
        
        # 生成回复
        response = self.llm.invoke(messages)
        content = response.content
        
        # 分离思考过程和实际回复
        clean_content, thought_process = Message.clean_content(content)
        
        # 保存消息
        timestamp = datetime.now()
        message = {
            "content": clean_content,
            "sender": sender,
            "timestamp": timestamp.isoformat(),
            "thought_process": thought_process
        }
        
        # 保存到当天的文件
        date_str = timestamp.strftime("%Y-%m-%d")
        message_file = os.path.join(config.MESSAGES_DIR, f"{date_str}.json")
        
        # 保存消息
        messages_list = []
        if os.path.exists(message_file):
            with open(message_file, 'r', encoding='utf-8') as f:
                messages_list = json.load(f)
        messages_list.append(message)
        
        with open(message_file, 'w', encoding='utf-8') as f:
            json.dump(messages_list, f, ensure_ascii=False, indent=2)
            
        return message

def main():
    st.title("Two")
    
    # 初始化生成锁
    if 'is_generating' not in st.session_state:
        st.session_state.is_generating = False
    
    chat = ParallelUniverseChat()
    
    # 选择日期
    selected_date = st.date_input(
        "选择日期",
        datetime.now().date()
    )
    
    # 读取并显示消息
    date_str = selected_date.strftime("%Y-%m-%d")
    message_file = os.path.join(config.MESSAGES_DIR, f"{date_str}.json")
    
    messages = []
    if os.path.exists(message_file):
        with open(message_file, 'r', encoding='utf-8') as f:
            messages = json.load(f)
            
        for msg in messages:
            with st.chat_message(msg['sender']):
                st.write(f"{datetime.fromisoformat(msg['timestamp']).strftime('%H:%M')} - {msg['content']}")
    else:
        st.info("这一天还没有对话记录")
    
    # 显示生成状态
    if st.session_state.is_generating:
        st.warning("正在生成消息，请稍候...")
        
    # 手动触发消息生成
    if st.button("生成新消息", disabled=st.session_state.is_generating):
        if not st.session_state.is_generating:
            try:
                st.session_state.is_generating = True
                # 根据最后一条消息决定发送者
                last_sender = messages[-1]['sender'] if messages else None
                sender = "female" if last_sender == "male" else "male"
                
                with st.spinner(f"正在生成{'他' if sender == 'male' else '她'}的消息..."):
                    message = chat.generate_message(sender)
                    st.rerun()
            finally:
                st.session_state.is_generating = False

if __name__ == "__main__":
    main() 