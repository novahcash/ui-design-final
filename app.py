from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
import os

from class_data import CLASS_INFO
from species_data import SPECIES_INFO
from feats_data import ORIGIN_FEATS
from background_data import background_data

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

STEPS = ["Intro", "Class", "Class Info", "Species", "Species Info", "Background", "Background Info", "Bio", "Sheet"]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def restrict_progress():
    if request.endpoint == 'learn' and 'step_index' in request.view_args:
        step_index = request.view_args['step_index']
        max_step = session.get('max_step', 0)
        if step_index > max_step + 1:
            return redirect(url_for('learn', step_index=max_step))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start')
def start():
    session.clear()
    session['progress'] = {
        'started': datetime.now().isoformat(),
        'class': None,
        'species': None,
        'background': None,
        'name': '',
        'backstory': '',
        'image': '',
        'class_info': {},
        'species_info': {},
        'background_info': {},
        'quiz': {
            'answers': {},
            'feedback': {},
            'score': 0,
            'total': 0
        }
    }
    session['max_step'] = 0
    return redirect(url_for('learn', step_index=0))

@app.route('/learn/<int:step_index>')
def learn(step_index):
    step = STEPS[step_index]
    progress = session.get('progress', {})

    if step == "Class":
        if not progress.get('class'):
            progress['class'] = "Fighter"
            session['progress'] = progress
        return render_template('lesson_class.html', step_index=step_index, steps=STEPS)

    elif step == "Class Info":
        class_choice = progress.get('class')
        class_data = CLASS_INFO.get(class_choice)
        if not class_data:
            return redirect(url_for('learn', step_index=1))
        prior_selections = progress.get('class_info', {})
        template = f"lesson_{class_choice.lower()}.html" if class_choice in CLASS_INFO else "class_info.html"
        return render_template(template, step_index=step_index, steps=STEPS, class_data=class_data, prior_selections=prior_selections)

    elif step == "Species":
        if not progress.get('species'):
            progress['species'] = "Human"
            session['progress'] = progress
        return render_template('lesson_species.html', step_index=step_index, steps=STEPS)

    elif step == "Species Info":
        species_choice = progress.get('species', 'Human')
        species_data = SPECIES_INFO.get(species_choice)
        if not species_data:
            return redirect(url_for('learn', step_index=3))
        prior_selections = progress.get('species_info', {})
        template = f"lesson_{species_choice.lower()}.html"
        if species_choice == "Human":
            class_choice = progress.get("class", "Fighter")
            class_data = CLASS_INFO.get(class_choice)
            return render_template(template, step_index=step_index, steps=STEPS,
                                   species_data=species_data,
                                   prior_selections=prior_selections,
                                   origin_feats=ORIGIN_FEATS,
                                   class_data=class_data)
        return render_template(template, step_index=step_index, steps=STEPS,
                               species_data=species_data,
                               prior_selections=prior_selections)

    elif step == "Background":
        class_choice = progress.get('class')
        recommended = CLASS_INFO.get(class_choice, {}).get("recommended_backgrounds", [])
        return render_template('lesson_background.html', step_index=step_index, steps=STEPS, backgrounds=recommended)

    elif step == "Background Info":
        background_choice = progress.get('background')
        if background_choice == "Guard":
            return render_template('lesson_background_info.html',
                                   step_index=step_index,
                                   steps=STEPS,
                                   selected_background=background_choice,
                                   background_data=background_data[background_choice],
                                   prior_selections=progress.get('background_info', {}))
        else:
            return render_template('lesson_background_placeholder.html', step_index=step_index, steps=STEPS)

    elif step == "Bio":
        return render_template('lesson_bio.html', step_index=step_index, steps=STEPS, progress=progress)

    elif step == "Sheet":
        return render_template('lesson_sheet.html', step_index=step_index, steps=STEPS, progress=progress)

    else:
        return render_template('lesson_intro.html', step_index=step_index, steps=STEPS)

@app.route('/save', methods=['POST'])
def save():
    data = request.form.to_dict()
    progress = session.get('progress', {})

    if 'class' in data and data['class'] != progress.get('class'):
        progress['class'] = data['class']
        progress['class_info'] = {}
        class_data = CLASS_INFO.get(data['class'], {})
        if 'stats' in class_data:
            progress['class_info']['stats'] = class_data['stats']

    for key, value in data.items():
        if key.startswith('class_'):
            progress.setdefault('class_info', {})[key[6:]] = value
        elif key.startswith('species_'):
            progress.setdefault('species_info', {})[key[8:]] = value
        elif key.startswith('background_'):
            progress.setdefault('background_info', {})[key[11:]] = value
        elif key.startswith('quiz_'):
            progress.setdefault('quiz', {}).setdefault('answers', {})[key[5:]] = value
        elif key.startswith('feedback_'):
            progress.setdefault('quiz', {}).setdefault('feedback', {})[key[9:]] = value
        elif key not in ('next_step',):
            progress[key] = value

    if 'char_image' in request.files:
        file = request.files['char_image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            progress['image'] = filepath

    class_choice = progress.get("class")

    if class_choice == "Cleric":
        divine_order = progress["class_info"].get("divine_order")
        if divine_order == "Protector":
            progress["class_info"]["proficiency_bonus_weapons"] = ["Martial weapons"]
            progress["class_info"]["proficiency_bonus_armor"] = ["Heavy armor"]
            progress["class_info"]["cleric_feature"] = "Divine Order: Protector"
            progress["class_info"].pop("extra_cantrip", None)
            progress["class_info"].pop("skill_bonus_overrides", None)
        elif divine_order == "Thaumaturge":
            progress["class_info"]["extra_cantrip"] = "Word of Radiance"
            progress["class_info"]["skill_bonus_overrides"] = {
                "Arcana": 4,
                "Religion": 4
            }
            progress["class_info"]["cleric_feature"] = "Divine Order: Thaumaturge"
            progress["class_info"].pop("proficiency_bonus_weapons", None)
            progress["class_info"].pop("proficiency_bonus_armor", None)

    elif class_choice == "Fighter":
        style = progress["class_info"].get("fighting_style")
        if style:
            progress["class_info"]["fighter_feature"] = f"Fighting Style: {style}"

    elif class_choice == "Rogue":
        progress["class_info"]["expertise"] = ["Sleight of Hand", "Stealth"]
        progress["class_info"]["skill_bonus_overrides"] = {
            "Sleight of Hand": 6,
            "Stealth": 6
        }

    session['progress'] = progress

    next_step = int(request.form.get('next_step', -1))
    if 0 <= next_step < len(STEPS):
        session['max_step'] = max(session.get('max_step', 0), next_step)
        return redirect(url_for('learn', step_index=next_step))
    return redirect(url_for('home'))

@app.route('/set_species', methods=['POST'])
def set_species():
    data = request.get_json()
    species = data.get("species")
    if species:
        session.setdefault('progress', {})['species'] = species
    return '', 204

@app.route('/summary')
def show_summary():
    return render_template('summary.html', progress=session.get('progress', {}))

@app.route('/quiz')
def quiz_intro():
    progress = session.setdefault('progress', {})
    progress['quiz'] = {
        'answers': {},
        'feedback': {},
        'score': 0,
        'total': 0
    }
    session['progress'] = progress
    return render_template('quiz_intro.html')

@app.route('/quiz/<int:question_num>')
def quiz(question_num):
    return render_template(f'quiz_question{question_num}.html')

@app.route('/quiz/1/submit', methods=['POST'])
def submit_quiz1():
    part = request.form.get('part')
    answer = request.form.get('answer')
    progress = session.setdefault('progress', {})
    quiz = progress.setdefault('quiz', {})
    answers = quiz.setdefault('answers', {})
    feedbacks = quiz.setdefault('feedback', {})

    response = {"correct": False, "feedback": "", "score": 0}
    quiz['total'] = quiz.get('total', 0) + 1

    if part == "1":
        try:
            val = int(answer)
        except ValueError:
            val = -1

        answers["q1_part1"] = val
        if val == 25:
            response["correct"] = True
            response["feedback"] = "Correct! Nice work."
            response["score"] = 1
            quiz['score'] = quiz.get('score', 0) + 1
        else:
            response["feedback"] = "Not quite — try counting the diagonals again."

        feedbacks["q1_part1"] = response["feedback"]

    elif part == "2":
        answers["q1_part2"] = answer
        if answer.strip().lower() == "yes":
            response["correct"] = True
            response["feedback"] = "Correct! Well done."
            response["score"] = 1
            quiz['score'] = quiz.get('score', 0) + 1
        else:
            response["feedback"] = "Actually, 30' is just enough — try visualizing the path."

        feedbacks["q1_part2"] = response["feedback"]

    session['progress'] = progress
    return jsonify(response)

@app.route('/quiz/2/submit', methods=['POST'])
def submit_quiz2():
    answer = request.form.get('answer', '').strip().lower()
    progress = session.setdefault('progress', {})
    quiz = progress.setdefault('quiz', {})
    answers = quiz.setdefault('answers', {})
    feedbacks = quiz.setdefault('feedback', {})

    response = {"correct": False, "feedback": "", "score": 0}
    quiz['total'] = quiz.get('total', 0) + 1

    answers["q2"] = answer
    if answer == "perception":
        response["correct"] = True
        response["feedback"] = "Correct! Perception is used to notice hidden creatures, traps, or changes in the environment."
        response["score"] = 1
        quiz['score'] = quiz.get('score', 0) + 1
    else:
        response["feedback"] = "Incorrect. The correct answer is Perception — it lets you notice hidden creatures, traps, or changes in the environment."

    feedbacks["q2"] = response["feedback"]
    session['progress'] = progress
    return jsonify(response)

@app.route('/quiz/3/submit', methods=['POST'])
def submit_quiz3():
    part = request.form.get('part')
    answer = request.form.get('answer', '').strip().lower()

    progress = session.setdefault('progress', {})
    quiz = progress.setdefault('quiz', {})
    answers = quiz.setdefault('answers', {})
    feedbacks = quiz.setdefault('feedback', {})

    response = {"correct": False, "feedback": "", "score": 0}
    quiz['total'] = quiz.get('total', 0) + 1

    if part == '1':
        answers["q3_part1"] = answer
        if answer == 'attack roll':
            response["correct"] = True
            response["feedback"] = "Correct! Attack rolls determine whether weapons or projectiles hit their target."
            response["score"] = 1
            quiz['score'] = quiz.get('score', 0) + 1
        else:
            response["feedback"] = "Incorrect. The correct answer is Attack roll — these determine whether weapons or projectiles hit their target."
        feedbacks["q3_part1"] = response["feedback"]

    elif part == '2':
        answers["q3_part2"] = answer
        if answer == 'saving throw':
            response["correct"] = True
            response["feedback"] = "Correct! Saving throws are used to resist area-of-effect attacks and status effects like paralysis."
            response["score"] = 1
            quiz['score'] = quiz.get('score', 0) + 1
        else:
            response["feedback"] = "Incorrect. The correct answer is Saving throw — these are usually used against area-of-effect attacks and status effects such as paralysis."
        feedbacks["q3_part2"] = response["feedback"]

    session['progress'] = progress
    return jsonify(response)

@app.route('/quiz/result')
def quiz_result():
    return render_template('quiz_result.html', progress=session.get('progress', {}))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
