# 平行宇宙聊天 (Parallel Universe Chat)

[English](#english) | [中文](#中文)

## 中文

### 项目介绍
Two聊天是一个有趣的对话系统，模拟了两个Two中的角色进行对话。系统使用大语言模型来生成对话内容，让两个角色能够进行自然、连贯的交流。

### 特点
- 🌟 支持多种大语言模型（OpenAI API、本地 Ollama 模型等）
- 💬 实时对话生成
- 📅 历史对话查看
- 🔄 角色切换功能
- 🎨 美观的用户界面
- 🛠 可配置的提示词系统

### 安装说明

1. 克隆项目
```bash
git clone https://github.com/yourusername/parallel-universe-chat.git
cd parallel-universe-chat
```

2. 创建并激活虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
cp .env.example .env
```
编辑 `.env` 文件，填入必要的配置信息：
- 如果使用 OpenAI API：设置 `API_KEY` 和其他相关配置
- 如果使用 Ollama：确保本地 Ollama 服务运行，并设置相应配置

### 使用方法

1. 启动应用
```bash
streamlit run main.py
```

2. 在浏览器中访问应用（默认地址：http://localhost:8501）

3. 使用说明：
   - 在侧边栏选择你的角色（男生/女生）
   - 选择想要查看的对话日期
   - 输入消息并发送
   - 点击生成回复按钮获取对方回应

### 自定义配置

- 在 `data/config/prompts_config.json` 中自定义角色提示词
- 在 `.env` 文件中配置模型参数
- 可以通过配置页面实时修改系统设置

### 贡献指南
欢迎提交 Pull Request 或创建 Issue！

### 许可证
MIT License

---

## English

### Project Description
Parallel Universe Chat is an interesting dialogue system that simulates conversations between characters from parallel universes. The system uses large language models to generate dialogue content, enabling natural and coherent communication between two characters.

### Features
- 🌟 Support for multiple LLMs (OpenAI API, local Ollama models, etc.)
- 💬 Real-time dialogue generation
- 📅 Historical conversation viewing
- 🔄 Character switching
- 🎨 Beautiful user interface
- 🛠 Configurable prompt system

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/parallel-universe-chat.git
cd parallel-universe-chat
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
```
Edit the `.env` file with necessary configurations:
- For OpenAI API: Set `API_KEY` and other related settings
- For Ollama: Ensure local Ollama service is running and configure accordingly

### Usage

1. Start the application
```bash
streamlit run main.py
```

2. Access the application in your browser (default: http://localhost:8501)

3. Instructions:
   - Select your role (Male/Female) in the sidebar
   - Choose the date to view conversations
   - Enter and send messages
   - Click generate reply button to get responses

### Customization

- Customize character prompts in `data/config/prompts_config.json`
- Configure model parameters in `.env` file
- Modify system settings through the configuration page

### Contributing
Pull requests and issues are welcome!

### License
MIT License 