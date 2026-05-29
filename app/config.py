from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str
    PORT: int
    API_KEY_NAME: str
    VALID_API_KEY: str
    GRPC_HOST_LOCAL: str
    GRPC_PORT: str
    GRPC_KEY_NAME: str
    GRPC_KEY_VAL: str

    class Config:
        env_file = ".env"


settings = Settings()
