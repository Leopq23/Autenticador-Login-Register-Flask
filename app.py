from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "contraseña_Secreta2300"

# Configuracion SQL Alchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuarios.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Modelo de la base de datos ~ Fila de nuestra base de datos

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# RUTAS
@app.route("/")
def index():
    if "username" in session:
        return redirect("dashboard")
    return render_template("index.html")

# Login
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = Usuario.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session["username"] = username
        return redirect("dashboard")
    else:
        return render_template("index.html")
    
# Registro
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    user = Usuario.query.filter_by(username=username).first()
    if user:
        return render_template("index.html", error="El usuario ya esta activo")
    else:
        nuevo_usuario = Usuario(username=username)
        nuevo_usuario.set_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        session['username'] = username
        return redirect("dashboard")

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session["username"])
    return redirect("/")

# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)