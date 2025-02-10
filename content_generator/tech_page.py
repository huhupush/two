from .base_generator import BaseGenerator
import datetime
from typing import List

class TechArticleGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一位经验丰富的技术博主，擅长写作通俗易懂的技术文章。
你的文章特点是：
1. 结构清晰，层次分明
2. 专业术语准确，并会适当解释
3. 配有示例代码和实际应用场景
4. 文风专业但不枯燥
5. 适当使用 Markdown 格式增强可读性"""
        
    def generate_tech_article(self, topic: str, keywords: List[str] = None) -> str:
        """
        生成技术文章
        
        Args:
            topic: 文章主题
            keywords: 需要包含的关键词列表
        
        Returns:
            生成的技术文章
        """
        prompt = f"""请写一篇关于 {topic} 的技术文章，要求：
1. 包含引言、正文、总结三个部分
2. 正文部分要有清晰的小标题
3. 如果涉及代码，请使用代码块格式
4. 文章长度在 1500-2000 字之间"""
        
        if keywords:
            prompt += f"\n5. 请在文章中自然地包含以下关键词：{', '.join(keywords)}"
            
        content = self.generate_content(prompt, self.system_prompt, temperature=0.7)
        if content:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tech_{topic.replace(' ', '_')}_{timestamp}.md"
            self.save_content(content, filename)
        return content

if __name__ == "__main__":
    # 使用示例
    generator = TechArticleGenerator()
    topic = "Python异步编程实战"
    keywords = ["asyncio", "协程", "事件循环", "并发编程"]
    article = generator.generate_tech_article(topic, keywords)
    print("文章生成完成！") 