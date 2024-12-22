# 全局通用配置

class Config(object):
    db_url = 'mysql+pymysql://root:12345678@0.0.0.0:3306/shouji'
    page_count = 10
    # 文章图片的存储路径
    article_header_image_path = '/images/article/'
    user_header_image_path ='/images/headers/'
# 测试环境
class TestConfig(Config):
    if_echo = True
    LOG_LEVEL = "DEBUG"

# 生产环境
class ProductConfig(Config):
    if_echo = False
    LOG_LEVEL = "INFO"

config = {
    "test": TestConfig,
    "prop": ProductConfig
}