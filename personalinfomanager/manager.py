import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("notes", "notes", url_prefix="")

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor() 
    order = request.args.get("order", "asc")
    cursor.execute(f"select n.id, n.name, n.date from note n order by n.date order by n.date {order}")
    notes = cursor.fetchall()
    return render_template("index.html", notes = notes, order = order)
