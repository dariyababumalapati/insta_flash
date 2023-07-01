from flask import request, session, redirect, url_for
from database_models import db, Study
import random

def process_answer(card_id, action):

    if action == 'right':
        flashcard = Study.query.get(card_id)
        if flashcard:
            db.session.delete(flashcard)  # Delete flashcard from the study table
            db.session.commit()

    elif action == 'wrong':
        session['show_answer'] = False  # Reset session variable to hide answer

        # Retrieve the remaining flashcards from the study table
        study_cards = Study.query.filter(Study.id != card_id).all()

        if study_cards:
            random_card = random.choice(study_cards)
            study_card_index = random_card.id
        else:
            study_card_index = None

        return redirect(url_for('study', card_id=study_card_index))

    return redirect(url_for('study'))

if __name__ == '__main__':
    print('answer module')