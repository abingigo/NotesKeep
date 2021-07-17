import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("notes", "notes", url_prefix="")

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
    	cursor.execute(f"select n.id, n.name, n.date from notes n, hashtag h, hashtag_notes hn where hn.note=n.id and hn.hashtag=h.id and h.name = ? order by n.{oby} {order}", [value])
    else:
    	cursor.execute(f"select n.id, n.name, n.date from notes n, hashtag h, hashtag_notes hn where n.{field} = ? order by n.{oby} {order}", [value])
    notes = cursor.fetchall()
    return render_template('search.html', notes = notes, field=field, value=value, order="desc" if order=="asc" else "asc")

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor() 
    order = request.args.get("order", "asc")
    cursor.execute(f"select n.id, n.name, n.date from note n order by n.date order by n.date {order}")
    notes = cursor.fetchall()
    return render_template("index.html", notes = notes, order = order)

@bp.route("/<nid>")
def note_info(nid):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select n.name, n.date, n.description from note n where n.id = ?", [nid])
    note = cursor.fetchone()
    cursor.execute("select h.name from hashtag_notes hn, hashtag h where hn.note = ? and hn.hashtag = h.id", [nid])
    tags = (x[0] for x in cursor.fetchall())
    name, date, description = note
    data = dict(id = id,
                name = name,
                date = format_date(date),
                description = description,
                tags = tags)
    return render_template("notedetail.html", **data)
