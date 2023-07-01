from ai import PassageFlashcards

from database_models import db, Passage, Study, Flashcard


class PassageToCards:

    def __init__(self, passage_data) -> None:
        self.passage_db = Passage(passage_data)
        self.passage_ai_obj = PassageFlashcards(passage_data)
        self.passage_id = None
        self.flashcard_transients = self.passage_ai_obj.generate_flashcards()
        self.num_flashcards = len(self.flashcard_transients)  # Get the number of flashcards created

        
    def commit_passage_and_flashcards(self):
        self._passage_to_database()
        self._flashcards_to_db()
        self._copy_flashcards_to_study()
    
    def _passage_to_database(self):
        db.session.add(self.passage_db)
        db.session.commit()
        self.passage_id = self.passage_db.id
    
    def _flashcards_to_db(self):
        for card in self.flashcard_transients:
            question = card['front']
            answer = card['back']
            flashcard = Flashcard(question=question, answer=answer, passage_id=self.passage_id)
            db.session.add(flashcard)
        db.session.commit()

    def _copy_flashcards_to_study(self):
        Study.query.delete()
        db.session.commit()

        flashcards = Flashcard.query.filter_by(passage_id=self.passage_id).all()
        for flashcard in flashcards:
            study_card = Study(question=flashcard.question, answer=flashcard.answer, passage_id=flashcard.passage_id)
            db.session.add(study_card)
        db.session.commit()
    
if __name__ == 'main':
    print('passage_class module')