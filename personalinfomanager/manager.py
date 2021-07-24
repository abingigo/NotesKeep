import datetime
import re
from sqlite3.dbapi2 import TimeFromTicks

from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask import g

from . import db

bp = Blueprint("personalinfomanager", "personalinfomanager", url_prefix="")

def format_date(d):
    if d:
        if d == 1:
            d = datetime.datetime.now()
        else:
            d = datetime.datetime.strptime(d, '%Y-%m-%d')
        v = d.strftime("%a - %b %d, %Y")
        return v
    else:
        return None

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor() 
    order = request.args.get("order", "asc")
    tag = request.args.get("tag", "all")
    if tag == "all":
        cursor.execute(f"select n.id, n.title, n.date, h.name from notes n, hashtag h where h.id=n.hashtag order by n.date {order}")
    else:
        cursor.execute(f"select n.id, n.title, n.date, h.name from notes n, hashtag h where h.id=n.hashtag and h.name=? order by n.date {order}", [tag])
    notes = cursor.fetchall()
    if notes:
        return render_template("index.html", notes = notes, order="desc" if order=="asc" else "asc")
    else:
        return render_template("none.html")

@bp.route("/<nid>")
def note_info(nid):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select n.title, n.date, n.description, h.name from notes n, hashtag h where n.id = ? and n.hashtag = h.id", [nid])
    note = cursor.fetchone()
    if note:
        title, date, description, tag = note
        data = dict(id = nid,
                    title = title,
                    date = format_date(date),
                    description = description,
                    hashtag = tag)
        return render_template("notedetail.html", **data)
    else:
        return ""

@bp.route("/add", methods=["GET", "POST"])
def add_note():
    if request.method == "GET":
        return render_template("addnote.html")
    elif request.method == "POST":
        conn = db.get_db()
        cursor = conn.cursor()
        title = request.form.get('title')
        description = request.form.get('description')
        date = datetime.datetime.now().date()
        if title:
            cursor.execute("INSERT INTO notes (title, date, description, hashtag) VALUES (?,?,?,2)", [title, date, description])
        conn.commit()
        return redirect(url_for("personalinfomanager.dashboard"), 302)

@bp.route("/<nid>/edit", methods=["GET", "POST"])
def edit(nid):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select n.title, n.date, n.description, h.name from notes n, hashtag h where n.id = ? and h.id = n.hashtag", [nid])
        note = cursor.fetchone()
        title, date, description, hashtag = note
        data = dict(id = nid,
                    title = title,
                    date = format_date(date),
                    description = description,
                    hashtag = hashtag)
        return render_template("editnote.html", **data)
    elif request.method == "POST":
        description = request.form.get('description')
        hashtag = request.form.get("Hashtag")
        cursor.execute("update notes set description = ?, hashtag = ? where id = ?", [description,hashtag,nid])
        conn.commit()
        return redirect(url_for("personalinfomanager.note_info", nid=nid), 302)
