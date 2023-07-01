from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap

from ai import PassageFlashcards

from database_actions import save_flashcards_to_database, copy_flashcards_to_study, get_random_flashcard


from database_models import db, Passage, Study
from process_answer import process_answer

from passage_class import PassageToCards

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'insta_flash'  # Replace with your own secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashcards.db'  # Replace with your desired database URL
bootstrap = Bootstrap(app)
db.init_app(app)

with app.app_context():
    # Create the database tables
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/process_passage', methods=['POST'])
def process_passage():
    # Retrieve the form data
    passage_content = request.form['passage']

    passage_and_flashcards = PassageToCards(passage_content)
    passage_and_flashcards.commit_passage_and_flashcards()

    copy_flashcards_to_study(passage_and_flashcards.passage_id)

    num_flashcards = len(passage_and_flashcards.flashcard_transients)  # Get the number of flashcards created
    
    return render_template('result.html', numb_flashcards=num_flashcards)

@app.route('/study')
def study():
    
    card_to_show = get_random_flashcard()
    session['show_answer'] = False  # Initialize session variable for answer display

    # Get the total number of flashcards in the study table
    total_flashcards = Study.query.count()

    return render_template('study.html', flashcard=card_to_show, total_flashcards=total_flashcards)

@app.route('/process_answer/<int:card_id>', methods=['POST'])
def process_answer_route(card_id):
    action = request.form.get('action')
    return process_answer(card_id, action)


if __name__ == '__main__':
    app.run(debug=True)
