from flask import request, jsonify
from flask_smorest import Blueprint, abort

# Mysql을 받아오기 위해 함수로 묶어주기 (db 전역으로 사용하기)
# API CRUD
def create_posts_blueprint(mysql):
    posts_blp = Blueprint("posts", __name__, description="posts api", url_prefix="/posts")

    @posts_blp.route('/', methods=['GET', 'POST'])
    def posts():
        cursor = mysql.connection.cursor()

        # 게시글 조회
        if request.method == 'GET':
            sql = "SELECT * FROM posts"
            cursor.execute(sql)

            posts = cursor.fetchall()
            cursor.close()

            post_list = []

            for post in posts:
                post_list.append({
                    'id':post[0],
                    'title':post[1],
                    'content':post[2]
                })

            return jsonify(post_list)
        
        # 게시글 생성
        elif request.method == 'POST':
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(400, message="Title or Content cannot be empty")

            sql = 'INSERT INTO posts (title, content) VALUES (%s, %s)'
            cursor.execute(sql, (title, content))
            mysql.connection.commit()

            return jsonify({'message':"successfully created post data", 'title':title, 'content':content}), 201
        
    # 1번 게시글만 조회하기
    # 게시글 수정 및 삭제
    @posts_blp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def post(id):
        cursor = mysql.connection.cursor()
        sql = f'SELECT * FROM posts WHERE id = {id}'
        cursor.execute(sql)
        post = cursor.fetchone()

        if request.method == 'GET':
            if not post:
                abort(404, "Not found post")
            return ({"id":post[0], "title":post[1], "content":post[2]})
        
        elif request.method == 'PUT':
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(400, "Not found title, content")

            if not post:
                abort(404, "Not found post")

            sql = f'UPDATE posts SET title={title}, content={content} WHERE id = {id}'
            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({"message":"successfully updated title & content"})

        # else로 할 경우, post에 대한 리스크가 생길 수도 있다. -> elif
        # 요청을 post로 했을 경우, 무조건 else문이 실행되기 때문에.
        elif request.method == 'DELETE':
            if not post:
                abort(400, "Not found title, content")

            sql = f'DELETE FROM posts WHERE id = {id}'
            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({"message":"successfully deleted title & content"})
        
    return posts_blp