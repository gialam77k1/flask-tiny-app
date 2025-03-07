from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    page = request.args.get('page', 1, type=int)
    # Get posts per page from settings
    posts_per_page = db.execute('SELECT value FROM settings WHERE key = "posts_per_page"').fetchone()
    per_page = int(posts_per_page['value']) if posts_per_page else 10
    offset = (page - 1) * per_page
    
    # Get total number of posts
    total_posts = db.execute('SELECT COUNT(*) as count FROM post').fetchone()['count']
    total_pages = (total_posts + per_page - 1) // per_page
    
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC LIMIT ? OFFSET ?',
        (per_page, offset)
    ).fetchall()
    return render_template('blog/index.html', posts=posts, page=page, total_pages=total_pages)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    flash('Post was successfully deleted.')
    return redirect(url_for('blog.index'))

@bp.route('/bulk-delete', methods=['POST'])
@login_required
def bulk_delete():
    post_ids = request.form.getlist('post_ids[]')
    if not post_ids:
        flash('No posts selected for deletion.')
        return redirect(url_for('blog.index'))
    
    db = get_db()
    # Verify all posts belong to current user
    for post_id in post_ids:
        post = db.execute(
            'SELECT author_id FROM post WHERE id = ?', (post_id,)
        ).fetchone()
        if not post or post['author_id'] != g.user['id']:
            abort(403)
    
    # Delete all selected posts
    db.execute(
        'DELETE FROM post WHERE id IN ({})'.format(
            ','.join('?' * len(post_ids))
        ),
        post_ids
    )
    db.commit()
    flash(f'{len(post_ids)} posts have been deleted.')
    return redirect(url_for('blog.index'))