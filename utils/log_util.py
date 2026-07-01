import logging
import os
from logging.handlers import RotatingFileHandler

# 日志文件路径
LOG_DIR = "logs"
os.makedirs(LOG_DIR,exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR,"app.log")

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger():
    # 基础配置
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(), #控制台输出
            RotatingFileHandler(
                LOG_FILE,
                maxBytes=10*1024*1024, #单个文件最大10MB
                backupCount=5, #最多保留5个备份
                encoding="utf-8"
            ) #文件输出

        ]
    )
    return logging.getLogger("fastapi-app")

# 全局logger对象,其他文件直接导入使用
logger = setup_logger() 