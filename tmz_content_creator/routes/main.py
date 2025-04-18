from flask import Blueprint, render_template, request, current_app, session, jsonify
import json

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    user_prompt = ""
    language = session.get('language', 'en')  # Default to English
    improve_again = request.form.get('improve_again') == 'true'
    reset = request.form.get('reset') == 'true'
    previous_content = session.get('previous_content')
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # Handle reset
    if reset:
        session.pop('previous_content', None)
        session.pop('improvement_history', None)
        response_text = ""
        user_prompt = ""
        
        if is_ajax:
            return jsonify({"status": "reset"})
        return render_template("index.html", 
                             response_text=response_text,
                             user_prompt=user_prompt,
                             language=language)

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
            history = session.get('improvement_history', [])
            
            # If this is an improvement request, use the current content as input
            if improve_again and previous_content:
                user_prompt = previous_content.get('improved', user_prompt)
            
            # Generate content with improvement history
            response_text = current_app.content_service.create_content(
                user_prompt=user_prompt,
                language=language,
                improve_again=improve_again,
                previous_content=previous_content,
                history=history
            )
            
            # Store the current content and history for potential future improvements
            session['previous_content'] = response_text
            session['improvement_history'] = response_text.get('history', [])

            # If it's an AJAX request, return JSON
            if is_ajax:
                return jsonify(response_text)

    # For non-AJAX requests, render the template
    return render_template("index.html", 
                         response_text=response_text,
                         user_prompt=user_prompt,
                         language=language) 