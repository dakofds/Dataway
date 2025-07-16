from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Item, Reply
from datetime import datetime
import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.environ.get('c_name'),
    api_key="a_key",
    api_secret="s_key"
)

app = Flask(__name__)
app.secret_key = os.environ.get('sc_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI')

db.init_app(app)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(name=name, password=password).first()
        if user:
            session["username"] = user.name
            return redirect(url_for('view_board', board='home'))
        else:
            return render_template("login.html", error="Credenciais inválidas.")
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route("/<board>/", methods=['GET', 'POST'])
def view_board(board):
    valid_boards = ['home', 'root', 'dev', 'tech', 'tv', 'weeb', 'pol', 'pr0n']
    if board not in valid_boards:
        return "Board não encontrado", 404

    posts = Item.query.filter_by(board=board).all()
    return render_template(f"{board}.html", post=posts)

@app.route("/<board>/upload", methods=['GET', 'POST'])
@login_required
def upload_board(board):
    valid_boards = ['home', 'root', 'dev', 'tech', 'tv', 'weeb', 'pol', 'pr0n']
    if board not in valid_boards:
        return "Board inválido", 404

    if request.method == 'POST':
        file = request.files['files']
        filename = secure_filename(file.filename)
        result = cloudinary.uploader.upload(file, folder=f"{board}/images", public_id=filename)

        title = request.form['title']
        description = request.form['description']
        user = session.get("username", "Anônimo")
        date_format = datetime.now().strftime("%d/%m/%Y %H:%M")
        img = result["secure_url"]

        new_post = Item(
            board=board,
            title=title,
            description=description,
            author=user,
            date=date_format,
            img=img
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('view_board', board=board))

    return render_template(f"upload_{board}.html")

@app.route("/<board>/item/<int:id>", methods=['GET', 'POST'])
@login_required
def view_item(board, id):
    valid_boards = ['home', 'root', 'dev', 'tech', 'tv', 'weeb', 'pol', 'pr0n']
    if board not in valid_boards:
        return "Board inválido", 404

    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        content = request.form['content']
        author = session.get('username', 'Anônimo')
        date = datetime.now().strftime("%d/%m/%Y %H:%M")
        new_reply = Reply(content=content, author=author, date=date, item_id=item.id)
        db.session.add(new_reply)
        db.session.commit()
        return redirect(url_for('view_item', board=board, id=id))

    replies = Reply.query.filter_by(item_id=id).all()
    return render_template("item.html", item=item, replies=replies)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
