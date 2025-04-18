from flask import Blueprint, render_template, request, current_app

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        user_prompt = request.form.get("user_prompt", "")
        response_text = current_app.content_service.create_content(user_prompt)

    return render_template("index.html", response_text=response_text) 