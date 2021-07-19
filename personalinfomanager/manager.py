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

@bp.route("/search/<field>/<value>")
def search(field, value):
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id")
    order = request.args.get("order", "asc")
    if field == "tag":
    	cursor.execute(f"select n.id, n.title, n.date,n.hashtag from notes n, hashtag h where n.hashtag=h.id and h.name = ? order by n.{oby} {order}", [value])
    else:
    	cursor.execute(f"select n.id, n.title, n.date from notes n where n.{field} = ? order by n.{oby} {order}", [value])
    notes = cursor.fetchall()
    return render_template('search.html', notes = notes, field=field, value=value, order="desc" if order=="asc" else "asc")

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor() 
    order = request.args.get("order", "asc")
    cursor.execute(f"select n.id, n.title, n.date, h.name from notes n, hashtag h where h.id=n.hashtag order by n.date {order}")
    notes = cursor.fetchall()
    return render_template("index.html", notes = notes, order = order)

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
                    hashtags = tag)
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
        cursor.execute("INSERT INTO notes (title, date, description, hashtag) VALUES (?,?,?,2)", [title, date, description])
        conn.commit()
        return redirect(url_for("personalinfomanager.dashboard"), 302)

@bp.route("/<nid>/edit", methods=["GET", "POST"])
def edit(nid):
    return ""
