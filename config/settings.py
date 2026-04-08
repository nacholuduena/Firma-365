import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # DQD Database
    DQD_SERVER: str = os.getenv("DQD_SERVER", "localhost")
    DQD_DATABASE: str = os.getenv("DQD_DATABASE", "DQD")
    DQD_USERNAME: str = os.getenv("DQD_USERNAME", "sa")
    DQD_PASSWORD: str = os.getenv("DQD_PASSWORD", "")
    DQD_DRIVER: str = os.getenv("DQD_DRIVER", "ODBC Driver 17 for SQL Server")
    DQD_PORT: int = int(os.getenv("DQD_PORT", "1433"))

    # App
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"

    @property
    def database_url(self) -> str:
        return (
            f"mssql+pyodbc://{self.DQD_USERNAME}:{self.DQD_PASSWORD}"
            f"@{self.DQD_SERVER}:{self.DQD_PORT}/{self.DQD_DATABASE}"
            f"?driver={self.DQD_DRIVER.replace(' ', '+')}"
        )


settings = Settings()
