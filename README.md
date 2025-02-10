# Two - AI 行为研究平台

本项目是一个用于 AI 行为研究的综合平台，专注于研究 AI 的行为模式、社会关系及决策过程。

## 功能特点

- 🤖 模块化的 AI 行为研究系统
- 🌟 支持多种大语言模型（OpenAI、Ollama等）
- 💬 实时对话生成与分析
- 📊 数据可视化与轨迹追踪
- 🔄 交互式研究环境
- 📅 完整的历史记录系统

## 核心研究模块

### 1. 社交行为研究
- AI 角色扮演对话系统
- 支持人机交互和 AI 自主对话
- 对话历史记录与分析
- 灵活的角色切换机制

### 2. 空间决策研究
- 二维坐标系中的 AI 移动行为分析
- 实时轨迹可视化
- 基于历史数据的决策分析
- 轨迹记录与回放功能

## 项目结构

```
two/
├── app.py                    # 主应用入口
├── config.py                 # 全局配置
├── main.py                   # Streamlit主程序
├── requirements.txt          # 项目依赖
├── .env.example             # 环境变量示例
│
├── modules/                  # 核心模块
│   ├── services/            # 服务层
│   │   ├── __init__.py
│   │   ├── ai_service.py    # AI服务接口
│   │   ├── auth_service.py  # 认证服务
│   │   └── data_service.py  # 数据服务
│   │
│   └── spatial_decision/    # 空间决策模块
│       ├── __init__.py
│       ├── analysis/        # 分析组件
│       │   ├── __init__.py
│       │   ├── trajectory_analysis.py  # 轨迹分析
│       │   └── pattern_recognition.py  # 模式识别
│       │
│       ├── coordinate/      # 坐标系统
│       │   ├── __init__.py
│       │   ├── grid.py      # 网格系统
│       │   └── transform.py # 坐标转换
│       │
│       └── visualization/   # 可视化组件
│           ├── __init__.py
│           ├── trajectory_plot.py  # 轨迹绘制
│           └── heatmap.py         # 热力图
│
├── data/                    # 数据文件
│   ├── config/             # 配置文件
│   ├── trajectories/       # 轨迹数据
│   └── messages/           # 对话记录
│
├── pages/                   # Streamlit页面
├── tests/                   # 测试文件
├── utils/                   # 工具函数
└── assets/                 # 静态资源
```

### 模块详细说明

#### 1. Services 模块 (`modules/services/`)
服务层提供核心功能接口：
- **ai_service.py**: 
  - AI模型接口封装
  - 提示词管理
  - 对话上下文处理
  - 模型响应处理
- **auth_service.py**:
  - 用户认证
  - 权限管理
  - 会话控制
- **data_service.py**:
  - 数据存储接口
  - 数据格式转换
  - 数据验证

#### 2. 空间决策模块 (`modules/spatial_decision/`)

##### 2.1 分析组件 (`analysis/`)
- **trajectory_analysis.py**:
  - 轨迹数据预处理
  - 路径特征提取
  - 移动模式分析
  - 决策点识别
- **pattern_recognition.py**:
  - 行为模式识别
  - 异常检测
  - 趋势分析

##### 2.2 坐标系统 (`coordinate/`)
- **grid.py**:
  - 网格系统实现
  - 空间索引
  - 碰撞检测
- **transform.py**:
  - 坐标系转换
  - 投影变换
  - 比例尺处理

##### 2.3 可视化组件 (`visualization/`)
- **trajectory_plot.py**:
  - 轨迹实时绘制
  - 路径动画
  - 多轨迹对比
- **heatmap.py**:
  - 活动热力图
  - 密度分布
  - 时空分布可视化

## 快速开始

### 环境配置

1. 克隆项目
```bash
git clone https://github.com/yourusername/two.git
cd two
```

2. 创建虚拟环境
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

4. 环境变量配置
```bash
cp .env.example .env
# 编辑 .env 文件，配置必要的环境变量
```

### 启动应用

```bash
streamlit run main.py
```

访问 http://localhost:8501 开始使用

## 配置说明

### 模型配置
- 支持 OpenAI API 和本地 Ollama 模型
- 在 `.env` 文件中配置 API 密钥和模型参数
- 可在 `data/config/prompts_config.json` 中自定义提示词

### 系统要求
- Python 3.8+
- 稳定的网络连接（使用 OpenAI API 时）
- 充足的系统内存（使用本地模型时）

## 数据管理

### 数据存储
- 对话历史：`data/messages/`
- 轨迹数据：`data/trajectories/`
- 配置文件：`data/config/`

### 数据分析
- 内置数据分析工具
- 可视化图表生成
- 轨迹回放功能

## 开发指南

### 添加新功能
1. 在相应模块目录创建新文件
2. 遵循现有的代码结构和命名规范
3. 编写单元测试
4. 更新文档

### 代码规范
- 遵循 PEP 8 规范
- 使用类型注解
- 编写详细的文档字符串

## 常见问题

1. Q: 如何切换 AI 模型？
   A: 在配置文件中修改 model_provider 设置

2. Q: 数据如何备份？
   A: 所有数据自动保存在 data 目录，建议定期备份该目录

3. Q: 如何自定义研究场景？
   A: 修改 `data/config/prompts_config.json` 中的场景设置

## 更新日志

### v1.0.0 (2024-02-10)
- 初始版本发布
- 实现基础对话功能
- 集成 OpenAI 和 Ollama 模型
- 添加空间决策分析模块

## 许可证

MIT License

## 贡献指南

欢迎提交 Issue 和 Pull Request！

---

# Two - AI Behavior Research Platform

This project is a comprehensive platform for AI behavior research, focusing on studying AI behavioral patterns, social relationships, and decision-making processes.

## Features

- 🤖 Modular AI behavior research system
- 🌟 Support for multiple LLMs (OpenAI, Ollama, etc.)
- 💬 Real-time dialogue generation and analysis
- 📊 Data visualization and trajectory tracking
- 🔄 Interactive research environment
- 📅 Complete history recording system

## Core Research Modules

### 1. Social Behavior Research
- AI role-playing dialogue system
- Support for human-AI interaction and AI autonomous dialogue
- Dialogue history recording and analysis
- Flexible role-switching mechanism

### 2. Spatial Decision Research
- AI movement behavior analysis in 2D coordinate system
- Real-time trajectory visualization
- Decision analysis based on historical data
- Trajectory recording and playback

## Project Structure

[Same as Chinese version above]

### Detailed Module Description

#### 1. Services Module (`modules/services/`)
Service layer provides core functional interfaces:
- **ai_service.py**: 
  - AI model interface encapsulation
  - Prompt management
  - Dialogue context handling
  - Model response processing
- **auth_service.py**:
  - User authentication
  - Permission management
  - Session control
- **data_service.py**:
  - Data storage interface
  - Data format conversion
  - Data validation

#### 2. Spatial Decision Module (`modules/spatial_decision/`)

##### 2.1 Analysis Components (`analysis/`)
- **trajectory_analysis.py**:
  - Trajectory data preprocessing
  - Path feature extraction
  - Movement pattern analysis
  - Decision point identification
- **pattern_recognition.py**:
  - Behavior pattern recognition
  - Anomaly detection
  - Trend analysis

##### 2.2 Coordinate System (`coordinate/`)
- **grid.py**:
  - Grid system implementation
  - Spatial indexing
  - Collision detection
- **transform.py**:
  - Coordinate system conversion
  - Projection transformation
  - Scale handling

##### 2.3 Visualization Components (`visualization/`)
- **trajectory_plot.py**:
  - Real-time trajectory plotting
  - Path animation
  - Multi-trajectory comparison
- **heatmap.py**:
  - Activity heatmap
  - Density distribution
  - Spatiotemporal distribution visualization

## Quick Start

[... Keep the original content ...] 