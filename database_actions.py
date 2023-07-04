import random

from database_models import db, Flashcard, Study, User

def create_or_get_user(user_identity):
    existing_user = User.query.filter_by(user_id=user_identity).first()
    
    if existing_user is None:
        new_user = User(user_id=user_identity)
        new_user.save()
        return new_user
    else:
        return existing_user


def save_flashcards_to_database(flashcards, passage_id):
    for card in flashcards:
        question = card['front']
        answer = card['back']
        flashcard = Flashcard(question=question, answer=answer, passage_id=passage_id)
        db.session.add(flashcard)
    db.session.commit()

def clear_study_table():
    Study.query.delete()
    db.session.commit()

def copy_flashcards_to_study(passage_id):
    clear_study_table()  # Clear existing records
    flashcards = Flashcard.query.filter_by(passage_id=passage_id).all()
    for flashcard in flashcards:
        study_card = Study(question=flashcard.question, answer=flashcard.answer, passage_id=flashcard.passage_id)
        db.session.add(study_card)
    db.session.commit()

def get_random_flashcard():
    count = Study.query.count()
    random_index = random.randint(0, count - 1)
    flashcard = Study.query.offset(random_index).first()
    return flashcard

def save_user_instance(user_id):
    user = User(user_id)
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    print("database_actions module")
 