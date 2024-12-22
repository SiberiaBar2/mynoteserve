from sqlalchemy import Table
from common.database import db_connect
from app.config.config import config
from app.settings import env
db_session, Base, engine = db_connect()

class Favorite(Base):
    # 表结构的反射加载
    __table__ = Table('favorite', Base.metadata, autoload_with=engine)

    def change_favorite_status(self, article_id, canceled, user_id):
        # 查询文章是否存在
        favorite_data = db_session.query(Favorite).filter(
            Favorite.article_id == article_id,
            Favorite.user_id==user_id
        ).first()

        # 代表之前没有收藏 插入一条 0 为收藏 1 取消收藏
        if favorite_data is None:
            favorite = Favorite(
                article_id=article_id,
                user_id=user_id,
                canceled=canceled
            )
            db_session.add(favorite)
        else:
            favorite_data.canceled = canceled
        db_session.commit()