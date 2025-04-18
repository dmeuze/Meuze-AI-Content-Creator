from flask import Blueprint, render_template, request, current_app, session, jsonify
import json

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    user_prompt = ""
    language = session.get('language', 'en')  # Default to English
    improve_again = request.form.get('improve_again') == 'true'
    previous_content = session.get('previous_content')
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

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
            
            # Get improvement history if available
            history = []
            if request.form.get('history'):
                try:
                    history = json.loads(request.form.get('history'))
                except json.JSONDecodeError:
                    pass
            
            # Generate content with improvement history
            response_text = current_app.content_service.create_content(
                user_prompt=user_prompt,
                language=language,
                improve_again=improve_again,
                previous_content=previous_content,
                history=history
            )
            
            # Store the current content for potential future improvements
            session['previous_content'] = response_text

            # If it's an AJAX request, return JSON
            if is_ajax:
                return jsonify(response_text)

    # For non-AJAX requests, render the template
    return render_template("index.html", 
                         response_text=response_text,
                         user_prompt=user_prompt,
                         language=language) 