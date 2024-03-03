from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        'title':'Day1 Flask Challenge'
    }
    users = [
        {"username": "traveler", "name": "Alex"},
        {"username": "photographer", "name": "Sam"},
        {"username": "gourmet", "name": "Chris"}
    ]

    return render_template('index.html', data=data, users=users)

if __name__ == '__main__':
    app.run(debug=True)