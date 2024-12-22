from sqlalchemy import Table
from common.database import db_connect
from app.config.config import config
from app.settings import env
db_session, Base, engine = db_connect()

class User(Base):
    # 表结构的反射加载
    __table__ = Table('user', Base.metadata, autoload_with=engine)

    def get_one(self):
        return db_session.query(User)

    def get_userInfo(self, user_id):
        ussr_info = db_session.query(User).filter(
            User.user_id == user_id
        ).first()
        # 拼接用户头像
        ussr_info.picture = config[env].user_header_image_path + ussr_info.picture
        return ussr_info