from ai import PassageFlashcards

from database_models import db, Passage, Study, Flashcard

from database_actions import clear_study_table


class PassageToCards:

    def __init__(self, passage_data, user_id) -> None:
        self.passage_data = passage_data
        self.passage_ai_obj = PassageFlashcards(passage_data)
        self.user_id = user_id
        self.num_flashcards = None  # Get the number of flashcards created
        self.passage_id = None

        
    def commit_passage_and_flashcards(self):
        self._passage_to_database()
        self._flashcards_to_db()
        self._copy_flashcards_to_study()
    
    def _passage_to_database(self):
        passage_title = self.passage_ai_obj.generate_title()
        passage_transient = Passage(passage_content=self.passage_data, passage_title=passage_title, user_id= self.user_id)
        passage_transient.save()
    
    def _flashcards_to_db(self):
        flashcard_transients = self.passage_ai_obj.generate_flashcards()
        for card in flashcard_transients:
            question = card['front']
            answer = card['back']
            flashcard = Flashcard(question=question, answer=answer, passage_id=self.passage_id)
            flashcard.save()

    def _copy_flashcards_to_study(self):
        clear_study_table()

        flashcards = Flashcard.query.filter_by(passage_id=self.passage_id).all()
        for flashcard in flashcards:
            study_card = Study(question=flashcard.question, answer=flashcard.answer, passage_id=flashcard.passage_id)
            study_card.save()

if __name__ == 'main':
    print('passage_class module')