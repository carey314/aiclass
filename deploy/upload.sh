#!/bin/bash
# ============================================
# AI不难学 - 本地打包上传脚本
# 在你的 Mac 上运行，把项目传到服务器
# 用法: bash upload.sh <服务器IP> [SSH端口]
# 示例: bash upload.sh 43.135.12.34
# 示例: bash upload.sh 43.135.12.34 22
# ============================================

set -e

SERVER_IP=${1:?"请提供服务器IP，用法: bash upload.sh <IP> [端口]"}
SSH_PORT=${2:-22}

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REMOTE_DIR="/opt/aiclass-src"

echo "=========================================="
echo "  AI不难学 - 打包上传到服务器"
echo "  服务器: $SERVER_IP:$SSH_PORT"
echo "  项目: $PROJECT_DIR"
echo "=========================================="

# 1. 本地先构建前端
echo ""
echo "[1/3] 本地构建前端..."
cd "$PROJECT_DIR/frontend"
npm install
API_BASE="http://$SERVER_IP/api/v1" npm run build
echo "  前端构建完成"

# 2. 打包项目（排除不需要的文件）
echo ""
echo "[2/3] 打包项目文件..."
cd "$PROJECT_DIR"
tar czf /tmp/aiclass-deploy.tar.gz \
  --exclude='frontend/node_modules' \
  --exclude='frontend/.nuxt' \
  --exclude='backend/.venv' \
  --exclude='backend/__pycache__' \
  --exclude='.git' \
  --exclude='research' \
  --exclude='demo.js' \
  --exclude='test-report.md' \
  .

FILESIZE=$(ls -lh /tmp/aiclass-deploy.tar.gz | awk '{print $5}')
echo "  打包完成: /tmp/aiclass-deploy.tar.gz ($FILESIZE)"

# 3. 上传到服务器
echo ""
echo "[3/3] 上传到服务器..."
echo "  (可能需要输入服务器密码)"

ssh -p "$SSH_PORT" "root@$SERVER_IP" "mkdir -p $REMOTE_DIR"
scp -P "$SSH_PORT" /tmp/aiclass-deploy.tar.gz "root@$SERVER_IP:/tmp/"
ssh -p "$SSH_PORT" "root@$SERVER_IP" "cd $REMOTE_DIR && tar xzf /tmp/aiclass-deploy.tar.gz && rm /tmp/aiclass-deploy.tar.gz"

echo ""
echo "=========================================="
echo "  上传完成!"
echo "=========================================="
echo ""
echo "  接下来 SSH 登录服务器执行部署:"
echo ""
echo "    ssh -p $SSH_PORT root@$SERVER_IP"
echo ""
echo "  首次部署（先初始化环境，再部署）:"
echo "    sudo bash $REMOTE_DIR/deploy/setup-server.sh"
echo "    sudo bash $REMOTE_DIR/deploy/deploy.sh <你的域名或IP>"
echo ""
echo "  后续更新（只需部署）:"
echo "    sudo bash $REMOTE_DIR/deploy/deploy.sh <你的域名或IP>"
echo "=========================================="

# 清理本地临时文件
rm -f /tmp/aiclass-deploy.tar.gz
