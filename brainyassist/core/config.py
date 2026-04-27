import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Config:
    # API 配置
    BASE_URL = os.getenv("BASE_URL", "http://192.168.1.2:8000/v1")
    API_KEY = os.getenv("API_KEY", "sk-local-llama-123456")
    MODEL_ID = os.getenv("MODEL_ID", "gemma-4-31b-abliterated-Q8_0.gguf")
    
    # Web 服务器配置
    APP_PORT = int(os.getenv("APP_PORT", 8100))

    # 基础路径
    ROOT_DIR = Path(__file__).parent.parent.parent.absolute()
    DATA_DIR = ROOT_DIR / "data"
    
    # 认知空间路径
    COGNITIVE_SPACE_DIR = DATA_DIR / "cognitive_space"
    PERMANENT_COG_FILE = COGNITIVE_SPACE_DIR / "permanent_cognition.md"
    TEMPORARY_COG_FILE = COGNITIVE_SPACE_DIR / "temporary_context.md"
    
    # 长期记忆归档文件 (自动记录)
    SESSIONS_MEMORY_FILE = DATA_DIR / "sessionsMemory.md"
    # 用户手动维护的压缩索引层 (地图)
    USER_MEMORY_INDEX_FILE = ROOT_DIR / "MEMORY.md"

# 确保必要目录存在
Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
Config.COGNITIVE_SPACE_DIR.mkdir(parents=True, exist_ok=True)
