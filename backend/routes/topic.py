from datetime import datetime
from flask import Blueprint, request, redirect, url_for, flash, abort, render_template
from flask import session
from sqlalchemy.orm import joinedload, selectinload
import cloudinary.uploader
from werkzeug.utils import secure_filename
from backend.database.session import SessionLocal
from backend.models import Board, Topic, Reply
from backend.core.auth import login_required

topic_blueprint = Blueprint("topic", __name__)

@topic_blueprint.route("/<board_name>/<int:topic_id>/delete", methods=["POST"])
def view_topic_delete(board_name, topic_id):
    

@topic_blueprint.route("/<board_name>/create", methods=["GET"])
def view_topic_create(board_name):
    """
    Renderiza criação de topico
    """
    return render_template("create.html")

@topic_blueprint.route("/<board_name>/create", methods=["POST"])
@login_required
def topic_create(board_name):
    """
    Tratamento do POST de criação de topico
    """
    db = SessionLocal()

    subject = request.form.get("subject")
    content = request.form.get("content")
    file = request.files.get("media")

    if not subject or not content:
        db.close()
        flash("Título e conteúdo são obrigatórios.", "error")
        return redirect(url_for("board.view_board", board_name=board_name))

    board = db.query(Board).filter_by(name=board_name).first()
    if not board:
        db.close()
        abort(404, description="Board não encontrado")

    author_id = session.get("user_id")
    if not author_id:
        db.close()
        return redirect(url_for("auth.login"))

    media_url = None
    if file and file.filename != "":
        filename = secure_filename(file.filename)
        # Faz upload para Cloudinary, criando pasta com nome do board
        result = cloudinary.uploader.upload(
            file,
            folder=f"{board_name}/media",
            public_id=filename,
            overwrite=True,
            resource_type="auto"  # Para aceitar imagem e vídeo
        )
        media_url = result.get("secure_url")

    topic = Topic(
        subject=subject,
        content=content,
        media=media_url,
        board=board.id,
        author=author_id,
        created_at=datetime.now()
    )

    db.add(topic)
    db.commit()
    topic_id = topic.id
    db.close()

    return redirect(url_for("topic.view_topic", board_name=board_name, topic_id=topic.id))

@topic_blueprint.route("/<board_name>/<int:topic_id>", methods=["GET"])
def view_topic(board_name, topic_id):
    """
    GET num topico com base no ID
    """
    db = SessionLocal()

    topic = (
        db.query(Topic)
        .options(
            joinedload(Topic.author_user),
            selectinload(Topic.replies).joinedload(Reply.author_user),
            joinedload(Topic.board_rel)
        )
        .filter(Topic.id == topic_id)
        .first()
    )

    if not topic:
        db.close()
        abort(404, description="Tópico não encontrado")

    db.close()

    return render_template("topic.html", topic=topic)

@topic_blueprint.route("/<board_name>/<int:topic_id>/reply", methods=["POST"])
@login_required
def create_topic_reply(board_name, topic_id):
    db = SessionLocal()

    content = request.form.get("content")
    if not content:
        db.close()
        flash("O conteúdo da resposta não pode ser vazio.", "error")
        return redirect(url_for("topic.view_topic", board_name=board_name, topic_id=topic_id))

    topic = db.query(Topic).filter_by(id=topic_id).first()
    if not topic:
        db.close()
        abort(404, description="Tópico não encontrado")

    author_id = session.get("user_id")
    if not author_id:
        db.close()
        return redirect(url_for("auth.login"))

    reply = Reply(
        content=content,
        author=author_id,
        topic=topic_id,
        created_at=datetime.now()
    )

    db.add(reply)
    db.commit()
    db.close()

    return redirect(url_for("topic.view_topic", board_name=board_name, topic_id=topic_id))
