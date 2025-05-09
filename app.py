import os
from datetime import date
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo 
from wtforms.fields import SelectField, DateField
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False) 
    dob = db.Column(db.Date, nullable=False)             


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    category = SelectField('Audition Category', choices=[
        ('dancing', 'Dancing'),
        ('singing', 'Singing'),
        ('acting', 'Acting')
    ], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddAdminForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Add Admin')

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if current_user.is_authenticated:
        flash('Admins cannot submit contact form.', 'warning')
        return redirect(url_for('home'))

    if form.validate_on_submit():
        age = (date.today() - form.dob.data).days // 365
        if age < 18:
            flash('You must be at least 18 years old to participate.', 'warning')
            return render_template('contact.html', form=form)

        try:
            contact = Contact(
                name=form.name.data,
                email=form.email.data,
                message=form.message.data,
                category=form.category.data,
                dob=form.dob.data
            )
            db.session.add(contact)
            db.session.commit()
            flash('SEE YOU IN THE Audition! 🎉', 'success')
            return redirect(url_for('success'))
        except Exception as e:
            db.session.rollback()
            flash('Error submitting form!', 'danger')

    elif form.is_submitted():
        flash('Please correct the errors in the form.', 'danger')

    return render_template('contact.html', form=form)


@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('admin'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    contacts = Contact.query.all()
    return render_template('admin.html', contacts=contacts)

@app.route('/admin/manage')
@login_required
def manage_admins():
    admins = User.query.all()
    return render_template('manage_admins.html', admins=admins)

@app.route('/admin/add', methods=['GET', 'POST'])
@login_required
def add_admin():
    form = AddAdminForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        admin = User(
            name=form.name.data,
            username=form.username.data,
            password=hashed_pw
        )
        db.session.add(admin)
        db.session.commit()
        flash('New admin added successfully!', 'success')
        return redirect(url_for('manage_admins'))
    return render_template('add_admin.html', form=form)

@app.route('/admin/delete/<int:admin_id>')
@login_required
def delete_admin(admin_id):
    if current_user.id == admin_id:
        flash('You cannot delete yourself!', 'danger')
        return redirect(url_for('manage_admins'))
    admin = User.query.get_or_404(admin_id)
    db.session.delete(admin)
    db.session.commit()
    flash('Admin deleted successfully', 'success')
    return redirect(url_for('manage_admins'))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def create_first_admin():
    with app.app_context():
        if not User.query.first():
            # REMOVE FALLBACK VALUES - Only use .env
            default_username = os.getenv('ADMIN_USERNAME')
            default_password = os.getenv('ADMIN_PASSWORD')
            
            if not default_username or not default_password:
                raise ValueError(
                    "Missing admin credentials! "
                    "Please set ADMIN_USERNAME and ADMIN_PASSWORD in .env file"
                )
            
            hashed_pw = generate_password_hash(default_password)
            admin = User(
                name='Yuvraj',  # This can remain hardcoded
                username=default_username,
                password=hashed_pw
            )
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    create_first_admin()
    app.run(debug=True)