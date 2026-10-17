from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "mysql+pymysql://vicerrectorado:vicerrectorado@localhost:3306/"
        "vicerrectorado?charset=utf8mb4"
    )
    JWT_SECRET: str = "dev-secret-change-me"
    JWT_EXP_HOURS: int = 8
    PORT: int = 8080
    CORS_ORIGINS: str = "http://localhost:5173,tauri://localhost,http://tauri.localhost"
    ADMIN_EMAIL: str = "admin@unap.edu.pe"
    ADMIN_PASSWORD: str = "admin123"

    class Config:
        env_file = ".env"


settings = Settings()