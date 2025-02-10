from content_generator.tech_article_about_project import ProjectArticleGenerator

def main():
    print("开始生成 Two聊天 项目介绍文章...")
    generator = ProjectArticleGenerator()
    article = generator.generate_project_article()
    print("文章生成完成！")

if __name__ == "__main__":
    main() 