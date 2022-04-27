from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_password: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    s3_access_key:str
    s3_secrete_access_key:str
    s3_username:str
    s3_bucketname:str

    class Config:
        env_file=".env"

settings = Settings()