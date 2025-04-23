import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

RECOMMENDED_BACKGROUNDS = {
    "Fighter": ["Soldier", "Guard", "Farmer"]
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start')
def start():
    session['start_time'] = datetime.now().isoformat()
    session['progress'] = {
        'lesson': 1,
        'quiz': 1,
        'answers': [],
        'class': None
    }
    return redirect(url_for('learn', lesson_num=1))

@app.route('/learn/<int:lesson_num>')
def learn(lesson_num):
    if lesson_num == 1:
        return render_template('lesson_intro.html')
    elif lesson_num == 2:
        return render_template('lesson_class.html')
    elif lesson_num == 3:
        selected_class = session.get('progress', {}).get('class')
        if selected_class == 'Fighter':
            return render_template('lesson_fighter.html')
        else:
            return f"Class info for '{selected_class}' not yet implemented."
    elif lesson_num == 4:
        return render_template('lesson_species.html')
    elif lesson_num == 5:
        selected_species = session.get('progress', {}).get('species')
        if selected_species == 'Human':
            return render_template('lesson_species_info.html')
        else:
            return f"Species info for '{selected_species}' not yet implemented."
    elif lesson_num == 6:
        selected_class = session.get('progress', {}).get('class')
        recommended = RECOMMENDED_BACKGROUNDS.get(selected_class, [])
        return render_template('lesson_background.html', backgrounds=recommended)
    elif lesson_num == 7:
        selected_background = session.get('progress', {}).get('background')
        if selected_background == 'Guard':
            return render_template('lesson_background_info.html')
        return f"Background info for '{selected_background}' not yet implemented."
    elif lesson_num == 8:
        return render_template('lesson_bio.html')
    else:
        return f"Lesson {lesson_num} not yet implemented."

@app.route('/save_class_info', methods=['POST'])
def save_class_info():
    selected_class = request.form.get('selected_class')
    progress = session.get('progress', {})

    # Mutate and reassign the full session dictionary
    progress['class'] = selected_class
    session['progress'] = progress

    print(f"[DEBUG] Saved class in session: {session['progress']['class']}")
    return redirect(url_for('learn', lesson_num=3))

@app.route('/save_species_info', methods=['POST'])
def save_species_info():
    selected_species = request.form.get('selected_species')
    progress = session.get('progress', {})
    progress['species'] = selected_species
    session['progress'] = progress
    return redirect(url_for('learn', lesson_num=5))

@app.route('/save_background_info', methods=['POST'])
def save_background_info():
    selected_background = request.form.get('selected_background')
    progress = session.get('progress', {})
    progress['background'] = selected_background
    session['progress'] = progress
    return redirect(url_for('learn', lesson_num=7))  # Next step after background

@app.route('/debug')
def debug():
    return session.get('progress', {})

@app.route('/save_bio_info', methods=['POST'])
def save_bio_info():
    char_name = request.form.get('char_name')
    char_backstory = request.form.get('char_backstory')
    char_image = request.files.get('char_image')

    progress = session.get('progress', {})

    if char_name:
        progress['name'] = char_name

    if char_backstory:
        progress['backstory'] = char_backstory

    if char_image and allowed_file(char_image.filename):
        filename = secure_filename(char_image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        char_image.save(filepath)
        progress['image'] = filepath

    session['progress'] = progress

    return redirect(url_for('show_summary'))

@app.route('/summary')
def show_summary():
    progress = session.get('progress', {})
    return f"<h1>Character Summary</h1><pre>{progress}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
