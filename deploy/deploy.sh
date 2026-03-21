#!/bin/bash
# ============================================
# AI不难学 - 一键部署脚本
# 用法: sudo bash deploy.sh <域名或IP>
# 示例: sudo bash deploy.sh aibunanxue.com
# 示例: sudo bash deploy.sh 43.135.xxx.xxx
# ============================================

set -e

DOMAIN=${1:-"_"}
PROJECT_DIR="/opt/aiclass"
DEPLOY_SRC="$(cd "$(dirname "$0")" && pwd)"
PROJECT_SRC="$(dirname "$DEPLOY_SRC")"

echo "=========================================="
echo "  AI不难学 - 一键部署"
echo "  域名/IP: $DOMAIN"
echo "=========================================="

# 检查 root
if [ "$EUID" -ne 0 ]; then
  echo "请用 sudo 运行: sudo bash deploy.sh <域名>"
  exit 1
fi

# ---- 1. 部署后端 ----
echo ""
echo "[1/5] 部署后端..."

# 复制后端代码
rsync -av --delete \
  --exclude '.venv' \
  --exclude '__pycache__' \
  --exclude '.env' \
  "$PROJECT_SRC/backend/" "$PROJECT_DIR/backend/"

# 创建/更新虚拟环境
if [ ! -d "$PROJECT_DIR/backend/.venv" ]; then
  echo "  创建 Python 虚拟环境..."
  python3.11 -m venv "$PROJECT_DIR/backend/.venv"
fi

echo "  安装 Python 依赖..."
"$PROJECT_DIR/backend/.venv/bin/pip" install --upgrade pip -q
"$PROJECT_DIR/backend/.venv/bin/pip" install -r "$PROJECT_DIR/backend/requirements.txt" -q

# 生成生产环境 .env（如果不存在）
if [ ! -f "$PROJECT_DIR/backend/.env" ]; then
  SECRET=$(python3.11 -c "import secrets; print(secrets.token_urlsafe(32))")

  if [ "$DOMAIN" = "_" ]; then
    ORIGIN="http://$(curl -s ifconfig.me 2>/dev/null || echo 'localhost')"
  else
    ORIGIN="http://$DOMAIN"
  fi

  cat > "$PROJECT_DIR/backend/.env" << ENVEOF
DATABASE_URL=sqlite+aiosqlite:///./aiclass.db
SECRET_KEY=$SECRET
ACCESS_TOKEN_EXPIRE_MINUTES=1440
CORS_ORIGINS=["$ORIGIN","http://localhost:3000"]
UPLOAD_DIR=/opt/aiclass/uploads
MAX_UPLOAD_SIZE=10485760
ENVEOF
  echo "  已生成 /opt/aiclass/backend/.env"
else
  echo "  .env 已存在，跳过（如需更新请手动编辑）"
fi

# 复制现有数据库（如有）
if [ -f "$PROJECT_SRC/aiclass.db" ] && [ ! -f "$PROJECT_DIR/backend/aiclass.db" ]; then
  cp "$PROJECT_SRC/aiclass.db" "$PROJECT_DIR/backend/aiclass.db"
  echo "  已复制现有数据库"
fi

# 确保 uploads 目录存在
mkdir -p "$PROJECT_DIR/uploads"
chown -R www-data:www-data "$PROJECT_DIR/uploads"

# ---- 2. 构建并部署前端 ----
echo ""
echo "[2/5] 构建并部署前端..."

cd "$PROJECT_SRC/frontend"

# 安装依赖
echo "  安装 Node 依赖..."
npm install --production=false --silent 2>/dev/null || npm install

# 设置 API 地址：通过 Nginx 反向代理，前端直接用相对路径
if [ "$DOMAIN" = "_" ]; then
  export API_BASE="http://$(curl -s ifconfig.me 2>/dev/null || echo 'localhost')/api/v1"
else
  export API_BASE="http://$DOMAIN/api/v1"
fi

echo "  API_BASE=$API_BASE"
echo "  构建前端（这可能需要几分钟）..."
npm run build

# 复制构建产物
rsync -av --delete "$PROJECT_SRC/frontend/.output/" "$PROJECT_DIR/frontend/.output/"

# ---- 3. 配置 Nginx ----
echo ""
echo "[3/5] 配置 Nginx..."

# 从模板生成配置
sed "s/YOUR_DOMAIN/$DOMAIN/g" "$DEPLOY_SRC/nginx.conf" > /etc/nginx/sites-available/aiclass

# 启用站点
ln -sf /etc/nginx/sites-available/aiclass /etc/nginx/sites-enabled/aiclass

# 移除默认站点（避免冲突）
rm -f /etc/nginx/sites-enabled/default

# 测试配置
nginx -t
echo "  Nginx 配置 OK"

# ---- 4. 安装 systemd 服务 ----
echo ""
echo "[4/5] 安装系统服务..."

cp "$DEPLOY_SRC/aiclass-backend.service" /etc/systemd/system/
cp "$DEPLOY_SRC/aiclass-frontend.service" /etc/systemd/system/

systemctl daemon-reload
systemctl enable aiclass-backend aiclass-frontend
systemctl restart aiclass-backend
systemctl restart aiclass-frontend
systemctl reload nginx

echo "  服务已启动"

# ---- 5. 验证 ----
echo ""
echo "[5/5] 验证部署..."
sleep 3

# 检查服务状态
echo ""
echo "后端状态:"
systemctl is-active aiclass-backend && echo "  ✓ 后端运行中" || echo "  ✗ 后端启动失败，查看: journalctl -u aiclass-backend -n 20"

echo ""
echo "前端状态:"
systemctl is-active aiclass-frontend && echo "  ✓ 前端运行中" || echo "  ✗ 前端启动失败，查看: journalctl -u aiclass-frontend -n 20"

echo ""
echo "Nginx状态:"
systemctl is-active nginx && echo "  ✓ Nginx运行中" || echo "  ✗ Nginx异常"

echo ""
echo "=========================================="
echo "  部署完成!"
echo "=========================================="
echo ""
if [ "$DOMAIN" = "_" ]; then
  IP=$(curl -s ifconfig.me 2>/dev/null || echo '<你的IP>')
  echo "  访问地址: http://$IP"
  echo "  后台管理: http://$IP/admin"
else
  echo "  访问地址: http://$DOMAIN"
  echo "  后台管理: http://$DOMAIN/admin"
fi
echo "  API文档:   http://$DOMAIN/docs"
echo ""
echo "  默认管理员: admin / admin123"
echo "  ⚠ 请登录后立即修改密码!"
echo ""
echo "  常用命令:"
echo "    查看后端日志: journalctl -u aiclass-backend -f"
echo "    查看前端日志: journalctl -u aiclass-frontend -f"
echo "    重启后端:     sudo systemctl restart aiclass-backend"
echo "    重启前端:     sudo systemctl restart aiclass-frontend"
echo ""
echo "  申请 HTTPS 证书（域名备案通过后）:"
echo "    sudo certbot --nginx -d $DOMAIN"
echo "=========================================="
