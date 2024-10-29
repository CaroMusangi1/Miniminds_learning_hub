from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secure key for session management

# Example math questions (15 questions)
math_questions = [
    {"question": "5 + 3", "answer": 8},
    {"question": "10 - 4", "answer": 6},
    {"question": "6 * 2", "answer": 12},
    {"question": "9 / 3", "answer": 3},
    {"question": "7 + 6", "answer": 13},
    {"question": "15 - 7", "answer": 8},
    {"question": "3 * 4", "answer": 12},
    {"question": "16 / 2", "answer": 8},
    {"question": "5 + 5", "answer": 10},
    {"question": "18 - 9", "answer": 9},
    {"question": "2 * 6", "answer": 12},
    {"question": "20 / 4", "answer": 5},
    {"question": "8 + 5", "answer": 13},
    {"question": "14 - 7", "answer": 7},
    {"question": "9 * 2", "answer": 18},
]

# Example language quiz questions (15 questions)
language_questions = [
    {"question": "Which of the following is a vowel?", "options": ['B', 'A', 'F'], "correct": 'A'},
    {"question": "Which of the following is a consonant?", "options": ['E', 'I', 'D'], "correct": 'D'},
    {"question": "What is the first letter of the English alphabet?", "options": ['A', 'B', 'C'], "correct": 'A'},
    {"question": "How many vowels are there in the English alphabet?", "options": ['5', '6', '7'], "correct": '5'},
    {"question": "Which letter comes after 'C'?", "options": ['D', 'E', 'F'], "correct": 'D'},
    {"question": "What is the last letter of the English alphabet?", "options": ['Y', 'Z', 'X'], "correct": 'Z'},
    {"question": "Which of these is a vowel?", "options": ['M', 'O', 'P'], "correct": 'O'},
    {"question": "Which letter starts the word 'Elephant'?", "options": ['E', 'L', 'T'], "correct": 'E'},
    {"question": "Which of the following is a fruit?", "options": ['Dog', 'Apple', 'Car'], "correct": 'Apple'},
    {"question": "Which letter is a vowel?", "options": ['B', 'A', 'F'], "correct": 'A'},
    {"question": "What letter comes before 'E'?", "options": ['D', 'F', 'C'], "correct": 'D'},
    {"question": "Which letter comes after 'F'?", "options": ['G', 'H', 'I'], "correct": 'G'},
    {"question": "What is the second vowel?", "options": ['E', 'I', 'O'], "correct": 'E'},
    {"question": "Which animal starts with 'C'?", "options": ['Cat', 'Dog', 'Fish'], "correct": 'Cat'},
    {"question": "What is the third vowel?", "options": ['I', 'O', 'U'], "correct": 'I'}
]

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/math')
def math():
    return render_template('math.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])
    operation = request.form['operation']

    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        result = num1 / num2 if num2 != 0 else "Cannot divide by zero"

    return render_template('math.html', result=result)

@app.route('/language')
def language():
    return render_template('language.html')

@app.route('/math-quiz', methods=['GET', 'POST'])
def math_quiz():
    if 'asked_math_questions' not in session:
        session['asked_math_questions'] = random.sample(range(len(math_questions)), len(math_questions))
        session['math_questions_answered'] = 0
        session['math_correct_answers'] = 0

    # Check if all questions have been answered
    if session['math_questions_answered'] >= len(math_questions):
        return redirect(url_for('math_results'))

    question_index = session['asked_math_questions'][session['math_questions_answered']]
    question_data = math_questions[question_index]
    feedback = None  # Initialize feedback variable

    if request.method == 'POST':
        answer = request.form.get('answer')
        correct_answer = question_data['answer']

        if answer is not None:
            if answer.isdigit():
                answer = int(answer)
                if answer == correct_answer:
                    session['math_correct_answers'] += 1
                    feedback = "Well done! You can proceed."
                else:
                    feedback = f"Incorrect. You answered {answer}. The correct answer is {correct_answer}."

                session['math_questions_answered'] += 1  # Move to the next question
                # Refresh the question after answering
                if session['math_questions_answered'] < len(math_questions):  # Check to prevent index error
                    question_index = session['asked_math_questions'][session['math_questions_answered']]
                    question_data = math_questions[question_index]
            else:
                feedback = "Please enter a valid number."

    return render_template(
        'math_quiz.html',
        feedback=feedback,
        questions_answered=session['math_questions_answered'],
        correct_answers=session['math_correct_answers'],
        question=question_data['question'],
        autocomplete="off"  # Disable suggestion box in HTML input
    )

@app.route('/language-quiz', methods=['GET', 'POST'])
def language_quiz():
    if 'asked_language_questions' not in session:
        session['asked_language_questions'] = random.sample(range(len(language_questions)), len(language_questions))
        session['language_questions_answered'] = 0
        session['language_correct_answers'] = 0

    # Check if all questions have been answered
    if session['language_questions_answered'] >= len(language_questions):
        return redirect(url_for('language_results'))

    question_index = session['asked_language_questions'][session['language_questions_answered']]
    question_data = language_questions[question_index]

    feedback = None  # Initialize feedback variable

    if request.method == 'POST':
        answer = request.form['answer'].strip().capitalize()
        correct_answer = question_data['correct'].strip().capitalize()

        if answer == correct_answer:
            session['language_correct_answers'] += 1
            feedback = "Well done! You can proceed."
        else:
            feedback = f"You still got it! The correct answer was {correct_answer}."

        session['language_questions_answered'] += 1

        if session['language_questions_answered'] >= len(language_questions):
            return redirect(url_for('language_results'))

        # Get the next question after answering
        question_index = session['asked_language_questions'][session['language_questions_answered']]
        question_data = language_questions[question_index]

    return render_template(
        'language_quiz.html',
        feedback=feedback,
        questions_answered=session['language_questions_answered'],
        correct_answers=session['language_correct_answers'],
        question=question_data['question'],
        options=question_data['options']
    )

@app.route('/math-results')
def math_results():
    correct_answers = session.get('math_correct_answers', 0)
    total_questions = len(math_questions)
    return render_template('math_results.html', correct_answers=correct_answers, total=total_questions)

@app.route('/language-results')
def language_results():
    correct_answers = session.get('language_correct_answers', 0)
    total_questions = len(language_questions)
    return render_template('language_results.html', correct_answers=correct_answers, total=total_questions)

@app.route('/reset-progress')
def reset_progress():
    session.clear()  # Clears all session data
    return redirect(url_for('home'))

@app.route('/reset-language-progress')
def reset_language_progress():
    session.pop('language_questions_answered', None)
    session.pop('language_correct_answers', None)
    return redirect(url_for('language_quiz'))

if __name__ == '__main__':
    app.run(debug=True)
