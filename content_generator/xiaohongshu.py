from .base_generator import BaseGenerator
import datetime
from typing import List, Optional

class XiaohongshuGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一位深谙小红书平台调性的博主，擅长创作吸引人的种草笔记。
你的文章特点是：
1. 标题吸引人，善用emoji
2. 开篇吸引眼球
3. 文风亲切自然，像朋友间分享
4. 善用排版和标签
5. 内容真实可信，有个人体验
6. 适当使用数字标记重点
7. 结尾有互动引导和标签"""

    def generate_post(
        self,
        topic: str,
        style: str = "种草",
        tags: List[str] = None,
        length: str = "中等"
    ) -> str:
        """
        生成小红书风格的文章
        
        Args:
            topic: 文章主题
            style: 文章风格，如：种草、测评、经验分享等
            tags: 文章标签
            length: 文章长度，可选：短、中等、长
        
        Returns:
            生成的小红书文章
        """
        length_guide = {
            "短": "300-500",
            "中等": "500-800",
            "长": "800-1200"
        }
        
        prompt = f"""请写一篇关于 {topic} 的小红书{style}文章，要求：
1. 文章长度在 {length_guide.get(length, "500-800")} 字之间
2. 标题要吸引人，适当使用emoji
3. 分点描述，重点突出
4. 语言要口语化，有互动感
5. 最后加上3-5个相关标签"""
        
        if tags:
            prompt += f"\n6. 请在文章中自然融入以下标签：{', '.join(tags)}"
            
        content = self.generate_content(prompt, self.system_prompt, temperature=0.8)
        if content:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"xiaohongshu_{topic.replace(' ', '_')}_{timestamp}.md"
            self.save_content(content, filename)
        return content

    def generate_title_options(self, topic: str, num_options: int = 3) -> List[str]:
        """
        为指定主题生成多个小红书风格的标题选项
        
        Args:
            topic: 文章主题
            num_options: 需要生成的标题数量
            
        Returns:
            标题列表
        """
        prompt = f"""请为主题"{topic}"生成{num_options}个小红书风格的标题，要求：
1. 每个标题都要吸引人
2. 适当使用emoji
3. 突出关键信息
4. 引发好奇心或情感共鸣"""
        
        content = self.generate_content(prompt, self.system_prompt, temperature=0.9)
        if content:
            # 简单处理返回的内容，假设每行一个标题
            titles = [t.strip() for t in content.split('\n') if t.strip()]
            return titles[:num_options]
        return []

if __name__ == "__main__":
    # 使用示例
    generator = XiaohongshuGenerator()
    
    # 生成文章
    topic = "咖啡店探店"
    tags = ["咖啡探店", "北京美食", "生活方式", "咖啡控"]
    post = generator.generate_post(
        topic=topic,
        style="探店",
        tags=tags,
        length="中等"
    )
    
    # 生成标题选项
    titles = generator.generate_title_options(topic)
    print("标题选项：")
    for i, title in enumerate(titles, 1):
        print(f"{i}. {title}")
    print("\n文章生成完成！") 