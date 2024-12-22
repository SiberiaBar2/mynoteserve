import json
import logging
from flask import Blueprint, render_template, request, session
from common.mode_list import model_list, model_object
from model.article import Article
from app.config.config import config
from app.settings import env
from model.favorite import Favorite
from model.user import User

favorite = Blueprint('favorite', __name__)

@favorite.route('/favorite/update_status')
def change_favorite_status():
   request_data = request.args
   # print('request_data', request_data['user_id'])
   # user_id = session.get("user_id")
   # article_id = request_data.get("article_id")
   # canceled = request_data("canceled")


   user_id = request_data["user_id"]
   article_id = request_data["article_id"]
   canceled = request_data["canceled"]

   try:
      canceled_status = int(canceled)
      Favorite().change_favorite_status(
         article_id=article_id,
         user_id=user_id,
         canceled=canceled
      )
      if int(canceled_status) == 0:
         print('收藏成功')
      else:
         print('取消收藏成功')
   except Exception as e:
      logging.error(e)
      print('操作失败', e)

   return 'oooo'