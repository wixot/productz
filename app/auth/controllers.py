from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash

from app.auth import auth
from app.auth.forms import RegistrationForm, LoginForm
from app.mail.postbox import send_mail
from app.models import User

from flask import redirect, render_template, flash, request, abort, url_for
from flask_login import login_required, logout_user

from app.utils.flask_snippets import is_safe_url, generate_timed_token


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.objects.create(email=form.email.data,
                                   username=form.username.data,
                                   password=generate_password_hash(form.password.data))

        token = generate_timed_token(user.get_id())

        send_mail(user.email, 'Hello, you are one step close to create your account.',
                  'mail/confirmation', user=user, token=token)

        flash('We sent you a confirmation email by email.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm(token):
        flash('Thank you for confirming account!', 'success')
    else:
        flash('Your confirmation link can be expired!', 'error')
    return redirect(url_for('index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user)

            flash('Logged in!')
            next = request.args.get('next')

            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('index'))
    return render_template('auth/login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
