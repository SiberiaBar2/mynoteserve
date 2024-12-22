from sqlalchemy import Table
from common.database import db_connect
from app.config.config import config
from app.settings import env
from model.user import User

db_session, Base, engine = db_connect()

class Article(Base):
    # 表结构的反射加载
    __table__ = Table('article', Base.metadata, autoload_with=engine)

    # 查询所有文章 不要草稿
    # 一页显示10条
    def get_all_article(self):
        return db_session.query(Article)

    def find_article(self,page,article_type='recommend'):

        if page < 1:
            page = 1
        count = int(page) * config[env].page_count

        # 走到这等于是来到了推荐的分类下边
        # 需要获取文章的作者 需要查user表 通过文章表的user_id 获取用户表的用户信息 用来展示文章作者昵称
        if article_type == 'recommend':
            result = db_session.query(Article).join(
                User, User.user_id == Article.user_id
            ).filter(Article.drafted == 1)\
                .order_by(Article.browse_num.desc())\
                .limit(count).all()
        else:
            result = db_session.query(Article).filter(
                Article.label_name == article_type,
                Article.drafted == 1  # 不是筛选出草稿的
            ).order_by(Article.browse_num.desc())

        return result

    def get_article_detail(self, article_id):
        return db_session.query(Article).filter(
            Article.id == article_id
        ).first()

    def insert_article(self, user_id,title,article_content, drafted):
        article = Article(
            user_id=user_id,
            title=title,
            article_content=article_content,
            drafted=drafted
        )

        db_session.add(article)
        db_session.commit()
        return article.id

    def update_article(self,
            article_id,
            title,
            article_content,
            drafted,
            label_name='',
            article_tag='',
            article_type=''
            ):

        row = db_session.query(Article).filter_by(
            id=article_id,
        ).first() # first返回找到的项 而不是数组

        row.title = title
        row.article_content = article_content
        row.drafted = drafted
        row.label_name = label_name
        row.article_tag = article_tag
        row.article_type = article_type
        db_session.commit()
        # 为什么要返回article_id？
        # 文章发布之后 如果要做跳转 就可以直接跳转到文章详情页面
        return article_id

    # 获取所有我的草稿
    def get_all_article_drafted(self, user_id):
        result = db_session.query(Article).filter_by(
            user_id=user_id,
            drafted=0
        ).all()

        return  result

    def get_all_article_drafted_detail(self, article_id):
        result = db_session.query(Article).filter_by(
            id=article_id,
            drafted=0
        ).first()

        return result