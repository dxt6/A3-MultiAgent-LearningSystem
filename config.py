"""
配置管理模块
从 .env 文件读取环境变量，支持模拟模式
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 加载 .env 文件
load_dotenv(BASE_DIR / ".env")


class Config:
    """应用配置类"""

    # 讯飞星火 API 配置
    SPARK_APP_ID = os.getenv("SPARK_APP_ID", "")
    SPARK_API_KEY = os.getenv("SPARK_API_KEY", "")
    SPARK_API_SECRET = os.getenv("SPARK_API_SECRET", "")

    # 模拟模式（设为 True 时无需真实 API，使用模拟数据）
    MOCK_MODE = os.getenv("MOCK_MODE", "True").lower() in ("true", "1", "yes")

    # 星火 API 端点
    SPARK_API_URL = "https://spark-api.xf-yun.com/v1/chat/completions"

    # WebSocket 域名（星火大模型）
    SPARK_WS_HOST = "spark-api.xf-yun.com"

    # 应用配置
    APP_TITLE = "A3 多智能体学习系统"
    APP_VERSION = "1.0.0"

    # 数据目录
    DATA_DIR = BASE_DIR / "data"
    EXPORTS_DIR = BASE_DIR / "exports"
    SAMPLE_PROFILES_DIR = BASE_DIR / "sample_profiles"

    @classmethod
    def validate(cls) -> tuple[bool, str]:
        """
        验证配置是否完整
        返回: (是否合法, 错误信息)
        """
        if cls.MOCK_MODE:
            return True, "模拟模式已启用，跳过 API 配置校验"

        missing = []
        if not cls.SPARK_APP_ID:
            missing.append("SPARK_APP_ID")
        if not cls.SPARK_API_KEY:
            missing.append("SPARK_API_KEY")
        if not cls.SPARK_API_SECRET:
            missing.append("SPARK_API_SECRET")

        if missing:
            return False, f"缺少必要的环境变量: {', '.join(missing)}"
        return True, "配置校验通过"

    @classmethod
    def to_dict(cls) -> dict:
        """以字典形式返回当前配置（隐藏敏感信息）"""
        return {
            "MOCK_MODE": cls.MOCK_MODE,
            "SPARK_APP_ID": "***" if cls.SPARK_APP_ID else "",
            "SPARK_API_KEY": "***" if cls.SPARK_API_KEY else "",
            "SPARK_API_SECRET": "***" if cls.SPARK_API_SECRET else "",
            "APP_TITLE": cls.APP_TITLE,
            "APP_VERSION": cls.APP_VERSION,
        }


# 全局配置实例
config = Config()
