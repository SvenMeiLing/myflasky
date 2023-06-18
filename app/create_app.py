# -*- coding: utf-8 -*-
# FileName: __init__.py
# Time : 2023/4/29 17:12
# Author: zzy
import datetime
import logging
import os
import redis

from flask_mail import Mail
from flask_cors import CORS
from flask_caching import Cache
from flask_session import Session
from flask_jwt_extended import JWTManager
from flask import Flask, Blueprint, g

from .scripts.load_config import load_configure
from .db.redis_session import get_redis_session
from .db.database import get_db_session, init_db, init_data

session = Session()  # 创建会话对象
mail = Mail()
jwt = JWTManager()
cache = Cache()

user_bp = Blueprint("user", __name__, url_prefix="/user")  # 创建有关user操作的蓝图
fileupload_bp = Blueprint("file", __name__, url_prefix="/file")
confirm_bp = Blueprint("confirm", __name__, url_prefix="/confirm")
data = Blueprint("data", __name__, url_prefix="/data")
crops = Blueprint("crops", __name__)
plant_bp = Blueprint("plant", __name__)
other_bp = Blueprint("other", __name__)

redis_config = load_configure().get("REDIS_CONFIG")  # 读取redis配置
TEMPLATE_HOLDER = load_configure().get("TEMPLATE_HOLDER")  # 模板文件所在目录
INSTANCE_PATH = load_configure().get("INSTANCE_PATH")
STATIC_FOLDER = load_configure().get("STATIC_FOLDER")


def create_app(test_config=None):
    # 创建和配置app程序
    app = Flask(__name__, instance_path=INSTANCE_PATH, template_folder=TEMPLATE_HOLDER, static_folder=STATIC_FOLDER)
    app.config.from_mapping(  # 更新配置也称设置

        **load_configure("REDIS_CONFIG"),  # 加载所有配置, 仅排除redis, 因为需要单独设置
        SESSION_REDIS=redis.Redis(
            redis_config.get("REDIS_HOST"),
            redis_config.get("REDIS_PORT"),
            redis_config.get("REDIS_SELECT_DB")
        ),
    )

    if test_config is None:
        # 非测试环境的加载
        app.config.from_pyfile('config.py', silent=True)  # 从文件中加载配置项
    else:
        # 是测试环境时, 加载以下方案
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)  # .../instance确保此目录存在, 不存在则创建(递归方式) 否则抛出异常
    except OSError:  # 截取异常并不做处理
        pass

    # app.logger.setLevel(logging.INFO)
    #
    # handler = RotatingFileHandler('app/logs/access.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)

    @app.before_request  # 每次请求前建立好数据库连接
    def open_db_session():
        g.db_session = get_db_session()
        g.redis_session = get_redis_session()

        g.mail = mail.init_app(app)  # 初始化mail服务


    # @app.before_request  # 每次请求前记录时间 , path ipaddr Method
    # def recording_log():
    #     g.request_start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     app.logger.info(
    #         'Request %s from %s, method is %s', request.path, request.remote_addr, request.method
    #     )

    # @app.after_request  # 请求结束后记录时间
    # def after_request(response):
    #     app.logger.info(
    #         'Request %s from %s took %s seconds', request.path, request.remote_addr,
    #         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     )
    #     return response

    with app.app_context():
        open_db_session()  # 把会话存储到全局变量
        init_db()  # 初始化数据库
        init_data()  # 初始化用户
        cache.init_app(app)  # 创建缓存

        from .views.other import tips_active

    session.init_app(app)  # 设置session拓展
    jwt.init_app(app)
    CORS(app, origins="*")  # 设置跨域请求为允许所有url访问

    @app.teardown_appcontext  # 注册一个 响应结束自动执行的一个函数
    def close_db_session(error):
        """在请求结束时关闭数据库会话"""
        db_session = g.pop('db_session', None)
        if db_session is not None:
            db_session.close()

        """关闭redis会话"""
        redis_session = g.pop('redis_session', None)
        if redis_session is not None:
            redis_session.close()

    from .views.user import User
    from .views.uploadfile import UpLoadFile
    from .views.confirmation import Confirmation
    from .views.data import DataShow
    from .views.crops_data import Crops
    from .views.plant_detail import PlantDetail

    user_bp.add_url_rule('/register', view_func=User.as_view('register'))
    user_bp.add_url_rule('/login', view_func=User.as_view('login'))
    user_bp.add_url_rule('/get_email', view_func=User.as_view('get_email'))
    user_bp.add_url_rule('/logout', view_func=User.as_view('logout'))
    user_bp.add_url_rule('/code', view_func=User.as_view('code'))

    data.add_url_rule('/auth/', view_func=DataShow.as_view('auth'))
    data.add_url_rule('/refresh_data', view_func=DataShow.as_view('refresh_data'))
    data.add_url_rule('/data_analysis', view_func=DataShow.as_view('data_analysis'))

    fileupload_bp.add_url_rule("/upload", view_func=UpLoadFile.as_view("upload"))

    confirm_bp.add_url_rule("/<string:_id>", view_func=Confirmation.as_view("confirm"))

    crops.add_url_rule("/crops", view_func=Crops.as_view("crops"))
    crops.add_url_rule("/crops_info", view_func=Crops.as_view("crops_info"))

    plant_bp.add_url_rule("/plant_details", view_func=PlantDetail.as_view("plant_details"))

    app.register_blueprint(user_bp)  # 注册蓝图
    app.register_blueprint(fileupload_bp)  # 注册蓝图
    app.register_blueprint(confirm_bp)  # 注册蓝图
    app.register_blueprint(data)  # 注册蓝图
    app.register_blueprint(crops)  # 注册蓝图
    app.register_blueprint(plant_bp)  # 注册蓝图

    return app
