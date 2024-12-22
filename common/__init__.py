import logging
from app.config.config import config
from app.settings import env
from logging.handlers import RotatingFileHandler

# 增加日志配置
def set_log():
    config_class = config[env]()
    # 设置日志的等级
    logging.basicConfig(level=config_class.LOG_LEVEL)
    # 创建日志记录器
    file_log_handel = RotatingFileHandler('log/mumulog',  # 路径
                                          maxBytes=1024*1024*300,  # 保存的文件大小
                                          backupCount=10  # 保存的文件个数
                                          )
    # 创建日志的格式
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d %(message)s')
    file_log_handel.setFormatter(formatter)
    # 为全局的日志工具添加日志记录器
    logging.getLogger().addHandler(file_log_handel)

set_log()