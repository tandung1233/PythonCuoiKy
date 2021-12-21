from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
@login_required
def home():
    page = request.args.get('page', default = 1, type = int)

    user_note = Note.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=5)
    next_url = url_for('views.home', page=user_note.next_num) \
        if user_note.has_next else None
    prev_url = url_for('views.home', page=user_note.prev_num) \
        if user_note.has_prev else None
    
    #user_note = Note.query.paginate(page=page, per_page=5)
    return render_template("home.html", user_note=user_note.items, user=current_user, next_url=next_url, 
    prev_url=prev_url, pagination=user_note)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/edit-note', methods=['POST'])
def edit_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    noteContent = note['noteContent']
    print(noteId, noteContent)
    note = Note.query.get(noteId)
    if note:
        note.data = noteContent
        db.session.commit()
    return jsonify({})


@views.route('/search', methods=['GET'])
@login_required
def method_name():
    txt = request.args.get('txt', default = "", type = str)
    print(txt)

    user_note = Note.query.filter_by(user_id=current_user.id).filter(Note.data.ilike(f"%{txt}%")).all()
    print(user_note)

    return render_template("search.html", user=current_user, user_note=user_note)
  


@views.route('/add', methods=['GET', 'POST'])
@login_required
def method_name2():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
        return redirect('/')

    return render_template("add.html", user=current_user)
