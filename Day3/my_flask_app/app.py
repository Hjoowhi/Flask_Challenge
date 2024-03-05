from flask import Flask
from flask_smorest import Api
from flask_mysqldb import MySQL
import yaml
from posts_routes import create_posts_blueprint

app = Flask(__name__)

# db.yaml에서 필요한 정보 불러오기
db_info = yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] = db_info['mysql_host']
app.config["MYSQL_USER"] = db_info['mysql_user']
app.config["MYSQL_PASSWORD"] = db_info['mysql_password']
app.config["MYSQL_DB"] = db_info['mysql_db']

mysql = MySQL(app)

# blueprint 설정
app.config['API_TITLE'] = 'Blog API List'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.1.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

# api 초기화 후
api = Api(app)
# 객체 받아오기
posts_blp = create_posts_blueprint(mysql)
# 등록
api.register_blueprint(posts_blp)

from flask import render_template
# 모든 게시글 조회
@app.route('/posts')
def manage_blogs():
    return render_template('posts.html')

if __name__ == "__main__":
    app.run(debug=True)