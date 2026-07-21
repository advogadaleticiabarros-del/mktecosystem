from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24
    GEMINI_API_KEY: str = ""
    CORS_ORIGINS: str = "http://localhost:3000"
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "Orbit <onboarding@resend.dev>"
    RESEND_WEBHOOK_SECRET: str = ""
    PUBLIC_API_URL: str = "http://localhost:8000"
    ENABLE_SCHEDULER: bool = False
    ENCRYPTION_KEY: str = "SV3ckJiDIf0XnoXjm-CJt6qXS3Ia-6S69PKds0L8sX4="
    META_APP_ID: str = ""
    META_APP_SECRET: str = ""
    META_REDIRECT_URI: str = "http://localhost:8000/integracoes/instagram/callback"
    FRONTEND_URL: str = "http://localhost:3000"
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/integracoes/google-business/callback"


settings = Settings()
