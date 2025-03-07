import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        elif user['is_blocked']:
            error = 'Your account has been blocked.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/admin')
@login_required
def admin():
    if not g.user['is_admin']:
        return redirect(url_for('index'))
    
    db = get_db()
    users = db.execute(
        'SELECT u.*, COUNT(p.id) as post_count '
        'FROM user u '
        'LEFT JOIN post p ON u.id = p.author_id '
        'WHERE u.id != ? '
        'GROUP BY u.id', 
        (g.user['id'],)
    ).fetchall()
    
    # Get current posts per page setting
    posts_per_page = db.execute('SELECT value FROM settings WHERE key = "posts_per_page"').fetchone()
    posts_per_page = int(posts_per_page['value']) if posts_per_page else 10
    
    return render_template('auth/admin.html', users=users, posts_per_page=posts_per_page)

@bp.route('/admin/update-settings', methods=['POST'])
@login_required
def update_settings():
    if not g.user['is_admin']:
        abort(403)
    
    posts_per_page = request.form.get('posts_per_page', type=int)
    if posts_per_page:
        db = get_db()
        db.execute('UPDATE settings SET value = ? WHERE key = ?', (posts_per_page, 'posts_per_page'))
        db.commit()
        flash('Settings updated successfully.')
    
    return redirect(url_for('auth.admin'))

@bp.route('/admin/toggle-admin/<int:user_id>', methods=['POST'])
@login_required
def toggle_admin(user_id):
    if not g.user['is_admin']:
        return redirect(url_for('index'))
    
    if g.user['id'] == user_id:
        flash('You cannot change your own admin status.')
        return redirect(url_for('auth.admin'))
    
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    
    if user is None:
        flash('User not found.')
        return redirect(url_for('auth.admin'))
    
    new_status = not user['is_admin']
    db.execute('UPDATE user SET is_admin = ? WHERE id = ?', (new_status, user_id))
    db.commit()
    
    flash(f"Admin status {'granted to' if new_status else 'removed from'} {user['username']}.")
    return redirect(url_for('auth.admin'))
    if not g.user['is_admin']:
        return redirect(url_for('index'))
    
    posts_per_page = request.form.get('posts_per_page', type=int)
    if not posts_per_page or posts_per_page < 1 or posts_per_page > 50:
        flash('Invalid posts per page value. Must be between 1 and 50.')
        return redirect(url_for('auth.admin'))
    
    db = get_db()
    db.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
               ('posts_per_page', str(posts_per_page)))
    db.commit()
    
    flash('Settings updated successfully.')
    return redirect(url_for('auth.admin'))

@bp.route('/admin/toggle-block/<int:user_id>', methods=['POST'])
@login_required
def toggle_block(user_id):
    if not g.user['is_admin']:
        return redirect(url_for('index'))
    
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    
    if user:
        db.execute(
            'UPDATE user SET is_blocked = ? WHERE id = ?',
            (not user['is_blocked'], user_id)
        )
        db.commit()
        flash(f'User {user["username"]} has been {"blocked" if not user["is_blocked"] else "unblocked"}.')
    
    return redirect(url_for('auth.admin'))

@bp.route('/admin/reset-password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if not g.user['is_admin']:
        return redirect(url_for('index'))
    
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
    
    if user:
        new_password = request.form['new_password']
        db.execute(
            'UPDATE user SET password = ? WHERE id = ?',
            (generate_password_hash(new_password), user_id)
        )
        db.commit()
        flash(f'Password for user {user["username"]} has been reset successfully.')
    
    return redirect(url_for('auth.admin'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

