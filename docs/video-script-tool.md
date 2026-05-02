# 视频脚本生成器（即梦AI模板）

## 功能概述

为aiclass的中老年用户（首位用户：鞠姐）提供一个手机端工具，按住说话/输入主题 → 自动生成可粘贴到即梦AI的视频脚本模板。

- **入口**：`/m/video-script`（移动端优先）
- **首位用户**：admin（鞠姐用此账号 dogfood）
- **白名单控制**：`VIDEO_SCRIPT_ALLOWED_USERS` 环境变量

## 架构

```
浏览器(手机)
  │
  │ 按住录音 / 文字输入
  ▼
Nuxt前端 (pages/m/video-script.vue)
  │
  │ POST /api/v1/video_script/transcribe (音频)
  │ POST /api/v1/video_script/generate (主题, SSE流式响应)
  │
  ▼
FastAPI后端
  │ services/doubao_client.py — ARK SDK封装
  │ services/prompt_builder.py — Prompt模板
  │
  ▼
火山方舟 / 豆包Seed-2.0-Pro
```

## 部署到生产服务器

### 1. 准备 ARK API Key

去 https://console.volcengine.com/ark 创建API Key，并开通 `Doubao-Seed-2.0-pro`。

### 2. 配置环境变量

服务器 `/opt/aiclass/backend/.env` 增加：

```bash
ARK_API_KEY=ark-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
ARK_TEXT_MODEL=doubao-seed-2-0-pro-260215
ARK_ASR_MODEL=bigmodel
VIDEO_SCRIPT_ALLOWED_USERS=admin
MAX_AUDIO_SIZE_MB=10
```

### 3. 部署流程（在服务器上执行）

```bash
cd /opt/aiclass-src   # 假设git仓库在这里
git pull origin main

# 后端：安装新依赖，重启
cd backend
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart aiclass-backend

# 前端：重新build，重启
cd ../frontend
npm install
API_BASE="http://your-domain/api/v1" npm run build
cp -r .output/* /opt/aiclass/frontend/.output/
sudo systemctl restart aiclass-frontend
```

或用现成的 `deploy.sh`：
```bash
sudo bash deploy/deploy.sh your-domain.com
```

### 4. 数据库自动建表

`init_db()` 在app启动时跑 `Base.metadata.create_all`，新加的 `video_scripts` 表会自动创建。无需手动迁移。

## 本地开发

### 后端
```bash
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

### 前端
```bash
cd frontend
npm run dev   # http://localhost:3000
```

### 鞠姐dogfood使用

1. 打开手机浏览器访问 `http://your-domain/m/video-script`
2. 用 admin / admin123 登录（生产环境改密码）
3. 长按"按住说话"按钮，说一句"我想做一个讲薏米红豆水祛湿的视频"
4. 松开后看到识别文字
5. 点"生成脚本"
6. 等20-30秒，看到完整脚本
7. 点"复制即梦提示词"
8. 切到即梦APP粘贴生成视频

## 测试

```bash
cd backend
source .venv/bin/activate

# 单元+集成测试 (不调外部API，必跑)
python -m pytest tests/ --ignore=tests/eval_doubao_quality.py

# 质量eval (真调豆包，~5分钟，每次改prompt跑一次)
python tests/eval_doubao_quality.py
```

最近一次 eval 结果：10/10 通过，平均延迟26秒。

## 关键文件

### 后端
- `app/services/doubao_client.py` — ARK SDK封装，含retry/超时
- `app/services/prompt_builder.py` — System prompt（人设+格式约束）
- `app/models/video_script.py` — VideoScript SQLAlchemy模型
- `app/schemas/video_script.py` — Pydantic schemas
- `app/api/v1/video_script.py` — 5个endpoint，含白名单+权限隔离

### 前端
- `pages/m/video-script.vue` — 移动端主页面
- `components/VoiceRecorder.vue` — 按住录音组件
- `components/ScriptResultCard.vue` — 结果展示+分段复制
- `composables/useVideoScript.ts` — API调用 + SSE流式解析

### 测试
- `tests/test_prompt_builder.py` — 14个prompt测试
- `tests/test_doubao_client.py` — 5个客户端测试（含retry/限流）
- `tests/test_api_video_script.py` — 12个API测试（含安全）
- `tests/eval_doubao_quality.py` — 质量eval（10个偏方主题）

## 演进路径

当前 = 方案A（脚本生成器，用户手动复制到即梦）。

下一步 = 方案B（端到端，直接调即梦API出视频）：
- 加 `POST /api/v1/video_script/{id}/render` 调即梦API
- 加 `jimeng_video_url` 字段到 `video_scripts` 表
- 即梦视频生成异步处理，前端轮询状态

## 已知限制

1. **延迟26秒**：Seed-2.0-Pro是reasoning模型，固有特性。已用SSE流式输出缓解
2. **白名单**：MVP只允许 `admin` 一个账号使用，要扩展白名单改 `VIDEO_SCRIPT_ALLOWED_USERS` 环境变量
3. **数据库**：用SQLite，单用户够用。多用户上线前建议迁PostgreSQL
4. **ASR**：豆包语音识别在 SDK 5.0.25 中通过 `audio.transcriptions` 接口。如果未来SDK变了或不支持webm格式，可能需要后端ffmpeg转码
