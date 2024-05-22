import email
from re import U
from flask import jsonify, redirect, request, session, url_for

from app import User, app, db
from app.schemas import UserOut, UserIn


@app.route("/", methods=["GET", "POST"])
def index():
    if "user_email" not in session:
        return redirect(url_for("user_login"))

    return f"Index page for user {session['user_email']}"


@app.route("/login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        user_data = request.get_json()

        get_user = User.query.filter_by(email=user_data.get("email")).first()

        if get_user is None:
            return jsonify({"message": "Invalid email "}), 401

        if get_user.checkPassword(user_data.get("password")) is False:
            return jsonify({"message": "Invalid password"}), 401

        session["user_email"] = get_user.email

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "data": UserOut(**get_user.__dict__).dict(),
                }
            ),
            200,
        )

    return "Login page"


@app.route("/register", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        user_data = UserIn(**request.get_json())

        get_user = User.query.filter_by(email=user_data.email).first()

        if get_user:
            return jsonify({"message": "User already exists"}), 409

        new_user = User(
            username=user_data.username,
            email=user_data.email,
        )
        new_user.setPassword(user_data.password)

        db.session.add(new_user)
        db.session.commit()
        session["user_email"] = user_data.email

        return redirect(url_for("index"))

    return "Register page"
