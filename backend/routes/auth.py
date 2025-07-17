from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database.session import SessionLocal
from backend.models import User

auth_blueprint = Blueprint("auth", __name__)

# Login

# render pager
@auth_blueprint.route("/login", methods=["GET"])
def login_page():
    """
    Esse endpoint é so pra renderizar a pagina de login
    """
    return render_template("login.html")

@auth_blueprint.route("/login", methods=["POST"])
def login():
    """
    Esse endpoint é só para o POST do login.
    """
    name = request.form.get('username')
    password = request.form.get('password')

    db = SessionLocal()
    user = db.query(User).filter_by(name=name).first()

    if not user or not check_password_hash(user.password, password):
        db.close()
        # Retorna para a página de login com mensagem de erro
        return render_template("login.html", error="Credenciais inválidas.")

    # Autenticação OK, armazena dados na sessão
    session["username"] = user.name
    session["user_id"] = user.id

    db.close()
    return redirect(url_for('board.read_root', board_name='home'))

# Register

@auth_blueprint.route("/register", methods=["GET"])
def register_page():
    """
    Esse endpoint é so pra renderizar a pagina de registro
    """
    return render_template("register.html")

@auth_blueprint.route("/register", methods=["POST"])
def register():
    """
    Esse endpoint é so pro POST de registro
    """
    name = request.form.get('username')
    password = request.form.get('password')

    db = SessionLocal()
    user_exists = db.query(User).filter_by(name=name).first()
    if user_exists:
        db.close()
        return render_template("register.html", error="Usuário já existe.")

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, password=hashed_password)

    db.add(new_user)
    db.commit()

    session["username"] = new_user.name
    db.close()
    return redirect(url_for('board.read_root', board='home'))
