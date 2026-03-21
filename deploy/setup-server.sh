#!/bin/bash
# ============================================
# AI不难学 - 服务器初始化脚本
# 在腾讯云 Ubuntu 22.04 上运行一次即可
# 用法: sudo bash setup-server.sh
# ============================================

set -e

echo "=========================================="
echo "  AI不难学 - 服务器环境初始化"
echo "=========================================="

# 检查 root 权限
if [ "$EUID" -ne 0 ]; then
  echo "请用 sudo 运行此脚本: sudo bash setup-server.sh"
  exit 1
fi

# 1. 系统更新
echo ""
echo "[1/6] 更新系统包..."
apt update && apt upgrade -y

# 2. 安装基础工具
echo ""
echo "[2/6] 安装基础工具..."
apt install -y curl wget git unzip software-properties-common

# 3. 安装 Python 3.11
echo ""
echo "[3/6] 安装 Python 3.11..."
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.11 python3.11-venv python3.11-dev
# 设置 python3 指向 3.11
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# 4. 安装 Node.js 20 (via NodeSource)
echo ""
echo "[4/6] 安装 Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
echo "Node版本: $(node -v)"
echo "NPM版本: $(npm -v)"

# 5. 安装 Nginx
echo ""
echo "[5/6] 安装 Nginx..."
apt install -y nginx
systemctl enable nginx
systemctl start nginx

# 6. 安装 Certbot (用于免费 SSL 证书)
echo ""
echo "[6/6] 安装 Certbot (Let's Encrypt SSL)..."
apt install -y certbot python3-certbot-nginx

# 7. 创建项目目录
echo ""
echo "创建项目目录..."
mkdir -p /opt/aiclass/backend
mkdir -p /opt/aiclass/frontend
mkdir -p /opt/aiclass/uploads
chown -R www-data:www-data /opt/aiclass/uploads

# 8. 开放防火墙端口
echo ""
echo "配置防火墙..."
if command -v ufw &> /dev/null; then
  ufw allow 22/tcp    # SSH
  ufw allow 80/tcp    # HTTP
  ufw allow 443/tcp   # HTTPS
  ufw --force enable
fi

echo ""
echo "=========================================="
echo "  服务器初始化完成!"
echo "=========================================="
echo ""
echo "已安装:"
echo "  - Python $(python3.11 --version 2>&1)"
echo "  - Node $(node -v)"
echo "  - Nginx $(nginx -v 2>&1)"
echo "  - Certbot (Let's Encrypt)"
echo ""
echo "项目目录: /opt/aiclass/"
echo ""
echo "下一步: 运行 deploy.sh 部署项目代码"
echo "=========================================="
