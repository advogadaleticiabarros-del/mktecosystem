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


settings = Settings()
