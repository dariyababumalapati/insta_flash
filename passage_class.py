from ai import PassageFlashcards

from database_models import User, Passage, Study, Flashcard

from database_actions import clear_study_table


class PassageToCards:

    def __init__(self, passage_data, user_id) -> None:
        self.passage_data = passage_data
        self.user_table_obj = User(user_id)
        self.passage_id = None
        self.num_flashcards = None  # Get the number of flashcards created

        
    def commit_passage_and_flashcards(self):
        self._user_to_database()
        self._passage_to_database()
        self._flashcards_to_db()
        self._copy_flashcards_to_study()

    def _user_to_database(self):
        self.user_table_obj.save()
    
    def _passage_to_database(self):
        passage_title = self.passage_ai_obj.generate_title()
        passage_transient = Passage(passage_content=self.passage_data, passage_title=passage_title, user_id= self.user_table_obj.id)
        passage_transient.save()
        self.passage_id = passage_transient.id
    
    def _flashcards_to_db(self):
        passage_ai_obj = PassageFlashcards(self.passage_data)
        flashcard_transients = passage_ai_obj.generate_flashcards()
        for card in flashcard_transients:
            question = card['front']
            answer = card['back']
            flashcard = Flashcard(question=question, answer=answer, passage_id=self.passage_id)
            flashcard.save()
        self.num_flashcards = len(flashcard_transients)

    def _copy_flashcards_to_study(self):
        clear_study_table()

        flashcards = Flashcard.query.filter_by(passage_id=self.passage_id).all()
        for flashcard in flashcards:
            study_card = Study(question=flashcard.question, answer=flashcard.answer, passage_id=flashcard.passage_id)
            study_card.save()

if __name__ == 'main':
    print('passage_class module')