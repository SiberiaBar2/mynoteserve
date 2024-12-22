import json
import logging
from flask import Blueprint, render_template, request, session, make_response, url_for
from common.mode_list import model_list, model_object, model_to_json
from model.article import Article
from app.config.config import config
from app.settings import env
from model.feed_back import FeedBack
from model.user import User

article = Blueprint('article', __name__)

@article.route('/articledetail')
def article_detail():
    article_id = request.args.get('article_id')
    article = Article()
    article_content = article.get_article_detail(article_id)
    print('article_content', model_object(article_content))
    # 获取文章作者信息
    user = User()
    user_info = user.get_userInfo(article_content.user_id)

    print('user_info', model_object(user_info))
    #  @todo 待办事项 评论、 文章点赞
    feed_back_list = FeedBack().get_feed_Back(article_id)
    print('feed_back_list', feed_back_list)
    # @todo 检测登录的人是否点赞了
    # return 'ok'

    return feed_back_list

@article.route('/article/new')
def article_new():
    # 我的草稿相关实现
    user_id = session.get('user_id')
    all_drafted = Article().get_all_article_drafted(user_id)
    return '文章编辑页面'

# 草稿详情接口
@article.route('/article/drafted/detail', methods=['post'])
def article_drafted_detail():
    request_data = json.loads(request.data)
    result = Article().get_all_article_drafted_detail(request_data.get('article_id'))
    # 把结果转成json 返回给前端
    article_drafted = model_to_json(request_data)
    return '草稿详情页面'

# 文章存储发布 登录权限验证
@article.before_request
def article_before_request():
    url = request.path
    is_login = session.get('is_login')
    # 走到这里就等于没有登录且到了写文章的页面
    if url.startswith('/article') and 'new' in url and is_login != 'true':
        response = make_response('登录重定向', 302)
        response.headers['Location'] = url_for('home.html')
        return response

def get_article_request_param(request_data):
    user = User.get_userInfo(session.get('user_id'))
    title = request_data.get('title')
    article_content = request_data.get('article_content')
    return user, title, article_content

# 草稿或正式文章存储 @todo 接口未测试
@article.route('/article/save', methods=['post'])
def article_save():
    request_data = json.loads(request.data)
    # 先判断有没有这个id 如果没有 就存储为草稿 有就存储为正文（文章发布）
    # 文章发布就是文章更新
    article_id = request_data.get('article_id')
    # 取出是否是草稿
    drafted = request_data.get('drafted')
    # 必须让前端传一个article_id 这个值如果是-1 就认为他是草稿
    if article_id == -1 and drafted==0:
        user,title,article_content = get_article_request_param(request_data)
        if title =="":
            return "请输入文 章头信息"
        # 存储草稿的时候一定要返回一个article_id回来
        article_id = Article().insert_article(user.user_id,title,article_content, drafted)

        # 这里返回的信息中应该把article_id一并返回给前端
        return '草稿存储成功'
    elif article_id > -1:
        user,title,article_content = get_article_request_param(request_data)
        if title =="":
            return "请输入文 章头信息"

        # 头像上传在前端点击上传完成的时候就已经到数据库了 因此这里不处理 另外的地方单独处理
        label_name = request_data.get('label_name')
        article_tag = request_data.get('article_tag')
        article_type = request_data.get('article_type')

        article_id = Article().update_article(
            article_id=article_id,
            title=title,
            article_content=article_content,
            drafted=drafted,
            label_name=label_name,
            article_tag=article_tag,
            article_type=article_type,
        )

    # 需要返回文章id
    return '文章发布成功的后端信息集合'
