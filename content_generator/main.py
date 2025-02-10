import os
from typing import List, Dict
from datetime import datetime
from .tech_page import TechArticleGenerator
from .xiaohongshu import XiaohongshuGenerator

def read_readme() -> str:
    """读取 README.md 文件内容作为上下文"""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"读取 README.md 时发生错误: {str(e)}")
        return ""

def generate_tech_articles(context: str) -> None:
    """生成技术文章"""
    generator = TechArticleGenerator()
    
    # 基于项目的技术主题列表
    topics = [
        {
            "topic": "Two聊天系统的技术架构设计",
            "keywords": ["Streamlit", "OpenAI API", "Ollama", "系统架构", "对话系统"]
        },
        {
            "topic": "如何实现AI角色扮演对话系统",
            "keywords": ["角色扮演", "AI对话", "提示词工程", "对话管理", "上下文控制"]
        },
        {
            "topic": "大语言模型在社会关系研究中的应用",
            "keywords": ["LLM", "社会关系", "人机交互", "行为分析", "研究方法"]
        }
    ]
    
    for topic_info in topics:
        print(f"\n生成技术文章: {topic_info['topic']}")
        generator.generate_tech_article(
            topic=topic_info["topic"],
            keywords=topic_info["keywords"]
        )

def generate_xiaohongshu_posts(context: str) -> None:
    """生成小红书文章"""
    generator = XiaohongshuGenerator()
    
    # 不同风格的小红书文章主题
    topics = [
        {
            "topic": "Two聊天：和AI的奇妙对话体验",
            "style": "体验分享",
            "tags": ["AI对话", "科技体验", "有趣分享", "社交新方式"]
        },
        {
            "topic": "AI角色扮演太有趣了",
            "style": "种草",
            "tags": ["AI互动", "科技种草", "社交体验", "科技生活"]
        },
        {
            "topic": "用AI研究社会关系是什么体验",
            "style": "经验分享",
            "tags": ["科研日常", "AI研究", "社会科学", "研究生活"]
        }
    ]
    
    for topic_info in topics:
        print(f"\n生成小红书文章: {topic_info['topic']}")
        # 先生成标题选项
        titles = generator.generate_title_options(topic_info["topic"])
        print("生成的标题选项：")
        for i, title in enumerate(titles, 1):
            print(f"{i}. {title}")
        
        # 生成文章内容
        generator.generate_post(
            topic=topic_info["topic"],
            style=topic_info["style"],
            tags=topic_info["tags"],
            length="中等"
        )

def main():
    # 创建输出目录
    output_dir = f"generated_articles_{datetime.now().strftime('%Y%m%d')}"
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取 README 作为上下文
    context = read_readme()
    if not context:
        print("无法读取 README 文件，将使用默认上下文继续生成")
    
    print("开始生成技术文章...")
    generate_tech_articles(context)
    
    print("\n开始生成小红书文章...")
    generate_xiaohongshu_posts(context)
    
    print(f"\n所有文章已生成完成，保存在 {output_dir} 目录下")

if __name__ == "__main__":
    main() 