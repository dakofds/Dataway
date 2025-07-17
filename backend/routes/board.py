from flask import Blueprint, redirect, url_for, flash, abort, render_template
from sqlalchemy.orm import joinedload
from backend.database.session import SessionLocal
from backend.models import Board, Topic

board_blueprint = Blueprint("board", __name__)

ROOT_BOARD = "b"

@board_blueprint.route("/", methods=["GET"])
def read_root():
    return redirect(url_for("board.view_board", board_name=ROOT_BOARD))

@board_blueprint.route("/<board_name>", methods=["GET"])
def view_board(board_name):
    """
    GET na board passada pelo parametro <board_name>
    """
    db = SessionLocal()
    boards = db.query(Board).all()
    board = (
        db.query(Board)
        .options(joinedload(Board.topics).joinedload(Topic.author_user))
        .filter_by(name=board_name)
        .first()
    )
    if not board:
        db.close()
        abort(404, description="Board não encontrado")

    topics = board.topics
    db.close()
    return render_template("board.html", boards=boards, title=board.name, topics=topics)