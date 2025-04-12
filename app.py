from flask import Flask, render_template, request, url_for, redirect, g, flash  
from models import db, Tasks, Mainmenu, Users
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import AddtaskForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'gjrevdfv89erghvreuvvujrnndkj'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@app.before_request
def load_menu():
    if 'menu' not in g:
        g.menu = Mainmenu.query.all()

@app.context_processor
def inject_menu():
    return dict(menu=g.get('menu', []))

@app.route('/')
def index():
    tasks = Tasks.query.all()
    menu = Mainmenu.query.all()
    return render_template('index.html', title="Home", tasks=tasks)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/checkbox/<int:task_id>', methods=['POST'])
def checkbox(task_id):
    task = Tasks.query.get_or_404(task_id)
    task.is_completed = not task.is_completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/addtasks', methods=['POST', 'GET'])
def add_task():
    form = AddtaskForm()
    if form.validate_on_submit():
        try:
            c = Tasks(title=form.name.data, description=form.description.data)
            db.session.add(c)
            db.session.commit()
            flash('Successfully added', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred + {str(e)}")
            flash('An error occurred', 'error')
    return render_template('addtask.html', title="Add a task", form=form)


@app.route('/tasks/<int:id>')
@login_required
def tasks(id):
    task = Tasks.query.get_or_404(id)
    return render_template('tasks.html', title="Tasks", task=task)

@app.route('/deltask/<int:id>')
def delete_task(id):
    task = Tasks.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if Users.query.filter_by(username=username).first():
            return render_template("sign_up.html", error="Username already taken")
        
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("sign_up.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
