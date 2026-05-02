import json
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./aiclass.db"
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24小时
    CORS_ORIGINS: str = '["http://localhost:3000"]'
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # ===== 视频脚本生成器（即梦AI模板）=====
    ARK_API_KEY: str = ""
    ARK_TEXT_MODEL: str = "doubao-seed-2-0-pro-260215"
    ARK_ASR_MODEL: str = "bigmodel"
    VIDEO_SCRIPT_ALLOWED_USERS: str = "admin"  # 逗号分隔的username白名单
    MAX_AUDIO_SIZE_MB: int = 10

    @property
    def cors_origins_list(self) -> list[str]:
        return json.loads(self.CORS_ORIGINS)

    @property
    def video_script_allowed_users_list(self) -> list[str]:
        """白名单用户列表(去空格、过滤空字符串)"""
        return [u.strip() for u in self.VIDEO_SCRIPT_ALLOWED_USERS.split(",") if u.strip()]

    class Config:
        env_file = ".env"


settings = Settings()
