from flask import render_template, request, redirect, url_for, flash
from taskmanager import app, db
from taskmanager.models import Category, Task, AppUser
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():
    tasks = Task.query.order_by(Task.id).all()
    return render_template("tasks.html", tasks=tasks)


@app.route("/categories")
def categories():
    categories = Category.query.order_by(Category.category_name).all()
    print(type(categories))
    categories = list(categories)
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = Category(category_name=request.form.get('category_name'))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template("add_category.html")


@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories'))


@app.route("/tasks")
def tasks():
    tasks = Task.query.order_by(Task.task_name).all()
    return render_template("tasks.html", tasks=tasks)


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    categories = Category.query.order_by("category_name").all()
    if request.method == "POST":
        task = Task(
            task_name=request.form.get("task_name"),
            task_description=request.form.get("task_description"),
            is_urgent=True if request.form.get("is_urgent") else False,
            due_date=request.form.get("due_date"),
            category_id=request.form.get("category_id")
            )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_task.html", categories=categories)


@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    categories = Category.query.order_by(Category.category_name).all()
    if request.method == "POST":
        task = Task.query.get_or_404(task_id)
        task.task_name=request.form.get("task_name")
        task.task_description=request.form.get("task_description")
        task.is_urgent=True if request.form.get("is_urgent") else False
        task.due_date=request.form.get("due_date")
        task.category_id=request.form.get("category_id")
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("tasks"))
    return render_template("edit_task.html", task=task, categories=categories)


@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("tasks"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username").lower()
        user_exists = AppUser.query.filter(AppUser.username==name).first() is not None
        if user_exists:
            flash("Username already exists")
            return redirect(url_for("register"))
        else:
            new_user = AppUser(
                username=name,
                password=generate_password_hash(request.form.get("password"))
            )
            db.session.add(new_user)
            db.session.commit()
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        user = AppUser.query.filter(AppUser.username==username).first()
        if user is not None:
            password_correct = check_password_hash(user.password, password)
            if password_correct:
                return redirect(url_for("tasks"))
        flash("Sorry, your login details are incorrect. Please try again")
        return redirect(url_for("login"))
         
    return render_template("login.html")
