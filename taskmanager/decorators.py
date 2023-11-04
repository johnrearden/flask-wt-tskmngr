from flask import session, redirect, url_for, flash
from functools import wraps

# Note, user is not redirected to their original chosen route after login.
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_logged_in = "user" in session.keys()
        print(f'logged in : {user_logged_in}')
        if not user_logged_in:
            flash('Please login first')
            return redirect(url_for('login'))

        # Execute decorated function
        result = func(*args, **kwargs)
        return result

    return wrapper