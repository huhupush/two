import os
from typing import Dict, Any, List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("API_KEY"))
class BaseGenerator:
    def __init__(self, output_dir: str = "generated_content"):
        self.api_key = os.getenv("API_KEY")
        self.api_base = os.getenv("API_BASE_URL")
        self.model_name = os.getenv("MODEL_NAME")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )
        self.output_dir = output_dir
        
    def generate_content(self, prompt: str, system_prompt: str = None, temperature: float = 0.7) -> str:
        """
        使用 OpenAI API 生成内容
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词，用于设定角色和风格
            temperature: 生成的随机性，0-1之间
            
        Returns:
            生成的内容
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=float(os.getenv("TEMPERATURE", temperature))
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"生成内容时发生错误: {str(e)}")
            return None
            
    def save_content(self, content: str, filename: str, directory: str = None):
        """
        保存生成的内容到文件
        
        Args:
            content: 生成的内容
            filename: 文件名
            directory: 保存目录，如果为None则使用默认目录
        """
        save_dir = directory or self.output_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        file_path = os.path.join(save_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"内容已保存到: {file_path}") 