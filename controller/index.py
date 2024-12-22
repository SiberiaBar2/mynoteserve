import logging
from flask import Blueprint, render_template, request
from common.mode_list import model_list, model_object
from model.article import Article
from app.config.config import config
from app.settings import env
index = Blueprint('index', __name__)

label_type = {
    "recommend": {"name": "推荐", "selected": "selected"},
    "auto_test": {"name": "自动化测试", "selected": "selected"},
    "python": {"name": "Python", "selected": "selected"},
    "java": {"name": "Java", "selected": "selected"},
    "pref_test": {"name": "性能测试", "selected": "selected"},
    "funny": {"name": "幽默段子", "selected": "selected"},
}
@index.route('/')
def home():
    page = request.args.get('page')
    article_type = request.args.get('article_type')

    logging.debug('page:'+str(page))
    logging.debug('article_type:'+str(article_type))

    if page is None:
        page = 1
    if article_type is None:
        article_type = 'recommend'

    # 到数据库中查询文章数据，并返回给前端页面
    article = Article()
    db_result = article.find_article(page, article_type)

    # 处理成前端展示需要的数据
    for article in db_result:
        pass
        article.label = label_type.get(article.label_name)
        # 日期的处理显示
        article.create_time = str(article.create_time.month)+'.' \
                            + str(article.create_time.day)
        # 处理图片路径
        article.article_image = config[env].article_header_image_path+\
                                str(article.article_image)
        article.article_tag = article.article_tag.replace(',', '·')
    # return render_template('home.html')

    print('article', model_object(article))
    # print('db_result', model_list(db_result) )
    return  '11'
    # return model_list(db_result)