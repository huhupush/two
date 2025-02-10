#!/bin/bash

# 检查操作系统
OS="$(uname)"
case $OS in
  'Linux')
    # 检查包管理器
    if command -v apt-get >/dev/null; then
      sudo apt-get update
      sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v yum >/dev/null; then
      sudo yum update
      sudo yum install -y python3 python3-pip
    else
      echo "不支持的 Linux 发行版"
      exit 1
    fi
    ;;
  'Darwin')
    # macOS
    if ! command -v brew >/dev/null; then
      echo "安装 Homebrew..."
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install python3
    ;;
  *)
    echo "不支持的操作系统: $OS"
    exit 1
    ;;
esac

# 创建项目目录结构
mkdir -p server/models
mkdir -p server/services
mkdir -p server/config
mkdir -p ui/pages
mkdir -p ui/components
mkdir -p scripts
mkdir -p tests
mkdir -p data/messages
mkdir -p data/thought_process

# 创建 __init__.py 文件
touch server/__init__.py
touch server/models/__init__.py
touch server/services/__init__.py
touch server/config/__init__.py
touch ui/__init__.py
touch ui/pages/__init__.py
touch ui/components/__init__.py
touch tests/__init__.py

echo "项目环境搭建完成！"
echo "请运行 ./scripts/deploy.sh 来部署应用" 