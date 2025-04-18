from flask import Blueprint, render_template, request, current_app, session

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    user_prompt = ""
    language = session.get('language', 'en')  # Default to English

    if request.method == "POST":
        # Check if this is a language change or content generation
        if 'language' in request.form and not request.form.get('user_prompt'):
            # Only language change, no content generation
            language = request.form.get("language", "en")
            session['language'] = language
        else:
            # Content generation
            user_prompt = request.form.get("user_prompt", "")
            language = request.form.get("language", "en")
            session['language'] = language
            response_text = current_app.content_service.create_content(user_prompt, language)

    return render_template("index.html", 
                         response_text=response_text,
                         user_prompt=user_prompt,
                         language=language) 