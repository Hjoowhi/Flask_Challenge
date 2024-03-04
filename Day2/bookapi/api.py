from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import BookSchema

# Blueprint를 사용하여 api 기능단위로 묶어줌
book_blp = Blueprint('books', 'books', url_prefix='/books', description='Operations on books')

# 메모리 영역에서 데이터 저장
books = []

# 여러 개의 데이터 가져오기
@book_blp.route('/')
class BookList(MethodView):
    @book_blp.response(200, BookSchema(many=True))  # 여러 개의 데이터가 True라면, 북리스트의 모든 데이터 가져오기
    def get(self):
        return books
    
    @book_blp.arguments(BookSchema) # POST, PUT -> arguments로 스키마 검증
    @book_blp.response(201, BookSchema)
    def post(self, new_data):
        new_data['id'] = len(books) + 1
        books.append(new_data)
        return new_data

# GET, PUT, DELETE
@book_blp.route('/<int:book_id>')
class Book(MethodView):
    @book_blp.response(200, BookSchema)
    def get(self, book_id):
        book = next((book for book in books if book['id'] == book_id), None) # next 함수로 하나의 조건을 만족하면 return 시킴
        if book is None: # 데이터가 없으면 None
            abort(404, message="Book not found")
        return book
    
    @book_blp.arguments(BookSchema)
    @book_blp.response(200, BookSchema)
    def put(self, new_data, book_id):
        book = next((book for book in books if book['id'] == book_id), None) #
        if book is None: 
            abort(404, message="Book not found")
        book.update(new_data)
        return book
    
    @book_blp.response(204)
    def delete(self, book_id):
        global books
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="Book not found")
        books = [book for book in books if book['id'] != book_id]
        return ''