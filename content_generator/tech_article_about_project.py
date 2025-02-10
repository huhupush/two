from .base_generator import BaseGenerator
import datetime

class ProjectArticleGenerator(BaseGenerator):
    def __init__(self):
        super().__init__()
        self.system_prompt = """你是一位技术博主，擅长写作技术分享文章。
你需要写一篇介绍开源项目的技术文章，要求：
1. 文风专业但不晦涩
2. 重点突出项目的技术特点和创新点
3. 适当使用代码示例
4. 突出实际应用价值
5. 引导读者参与和贡献"""

    def generate_project_article(self) -> str:
        """生成项目介绍文章"""
        prompt = """请写一篇介绍 Two聊天项目的技术文章，主题是《Two聊天：基于大语言模型的社会关系研究工具》，要求：

1. 文章结构：
   - 项目背景和意义
   - 核心技术特点
   - 系统架构
   - 关键功能实现
   - 应用场景
   - 未来展望

2. 重点突出以下特色：
   - 支持多种大语言模型（OpenAI API、Ollama等）
   - 灵活的角色配置系统
   - 对话历史管理
   - 实时交互体验
   - 社会关系研究价值

3. 包含以下技术要点：
   - Python + Streamlit 构建的现代化 Web 界面
   - 基于 OpenAI 兼容接口的模型调用
   - 提示词工程在角色扮演中的应用
   - 数据存储和管理方案
   - 部署和扩展建议

4. 文末加入项目地址和参与方式"""

        content = self.generate_content(prompt, self.system_prompt, temperature=0.7)
        if content:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"project_article_{timestamp}.md"
            self.save_content(content, filename)
        return content

if __name__ == "__main__":
    generator = ProjectArticleGenerator()
    article = generator.generate_project_article()
    print("项目介绍文章生成完成！") 