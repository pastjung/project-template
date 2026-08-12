from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "fastapi-app"
    app_version: str = "0.1.0"
    app_env: str = "local"
    log_level: str = "INFO"
    docs_enabled: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Settings 인스턴스를 반환합니다.

    라우트와 의존성에서는 전역 변수 대신 Depends(get_settings)로 주입받습니다.
    테스트에서 app.dependency_overrides[get_settings]로 교체할 수 있습니다.
    """
    return Settings()
