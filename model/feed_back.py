from sqlalchemy import Table
from common.database import db_connect
from app.config.config import config
from app.settings import env
from common.mode_list import model_to_json, model_list
from model.user import User

db_session, Base, engine = db_connect()

class FeedBack(Base):
    __table__ = Table('comment', Base.metadata, autoload_with=engine)

    # 需要最终给前端返回一个完整的数据 需要设计一个数据模型
    def get_feed_Back(self, article_id):
        user = User()
        fina_feed_list = []

        # 查询一级评论
        feed_first_list = self.find_first_feedBack_by_article_id(article_id)

        print('feed_first_list', model_list(feed_first_list))
        for feedBack in feed_first_list:
            # 根据一级评论的数据 获取回复评论的数据
            all_reply = self.find_reply_by_replyid(base_reply_id=feedBack.id)
            reply_list = []
            # 获取用户信息
            feedBack_user = user.get_userInfo(feedBack.user_id)
            # 根据回复的评论 获取用户信息
            for reply in all_reply:
                # print('reply===>', model_to_json(reply))

                # 用于存储回复这条原始评论的回复评论，如果没有评论，这里值就为空
                reply_content_with_user = {}
                # 获取 谁回复的
                from_user_data = user.get_userInfo(reply.user_id)
                # 获取回复谁的用户信息
                to_user_reply_data = self.find_reply_by_id(reply.reply_id)
                to_user_data = user.get_userInfo(to_user_reply_data[0].user_id)
                print('reply===》', model_list(to_user_reply_data), 'model_to_json(reply)',model_to_json(reply))

                reply_content_with_user['from_user'] = model_to_json(from_user_data)
                reply_content_with_user['to_user'] = model_to_json(to_user_data)
                reply_content_with_user['content'] = model_to_json(reply)
                reply_list.append(reply_content_with_user)

            # 存储每一个回复下的所有数据
            every_feedBack_data = model_to_json(feedBack)
            every_feedBack_data.update(model_to_json(feedBack_user))
            every_feedBack_data['reply_list'] = reply_list
            fina_feed_list.append(every_feedBack_data)
        return fina_feed_list

    def find_first_feedBack_by_article_id(self, article_id):
        feedBack = db_session.query(FeedBack).filter_by(
            article_id=article_id,
            reply_id=0, # 回复为0
            base_reply_id=0, # 当这两个条件满足 则为一级楼层评论
        ).order_by(
            FeedBack.id.desc()
        ).all()

        return feedBack

    def find_reply_by_replyid(self,base_reply_id):
        print('base_reply_id', base_reply_id)
        result = db_session.query(FeedBack).filter_by(
            base_reply_id=base_reply_id
        ).order_by(
            FeedBack.id.desc()
        ).all()
        print('result====>', result)
        return result

    def find_reply_by_id(self, id):
        result = db_session.query(FeedBack).filter_by(
            id = id
        ).order_by(
            FeedBack.id.desc()
        ).all()

        return result
