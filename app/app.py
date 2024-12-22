from flask import Flask

def create_app():
    app = Flask(__name__,
                template_folder='../template',
                static_url_path='/',
                static_folder='../resourse')
    # 注册蓝图
    init_blueprint(app)
    return app

# 注册蓝图模块
def init_blueprint(app):
    from controller.user import user
    app.register_blueprint(user)

    from controller.index import index
    app.register_blueprint(index)

    from controller.article import article
    app.register_blueprint(article)

    from controller.favorite import favorite
    app.register_blueprint(favorite)