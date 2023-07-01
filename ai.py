import openai

from config import API_KEY


openai.api_key = API_KEY


class PassageFlashcards:
    """
    Represents a passage and provides methods to generate flashcards from it.
    """

    def __init__(self, passage):
        """
        Initialize the PassageFlashcard object.

        Parameters:
        - passage (str): The passage text.
        """
        self.passage = passage

    def generate_flashcards(self):
        """
        Generate flashcards from the passage.

        Returns:
        - flashcards (list): A list of dictionaries representing the generated flashcards.
                             Each dictionary contains 'front' and 'back' keys representing
                             the question and answer of the flashcard, respectively.
        """
        prompt = f"""
        Create Anki flashcards from the given passage, specifying the note type as Basic
        and limiting the Back card to a maximum of 10 words:

        {self.passage}
        @foreach(card in flashcards)
        Front: {{card.front}}
        Back: {{card.back}}
        Note Type: {{Basic}}
        @endforeach
        """

        # Generate the flashcards using the OpenAI library
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.7,
            n=1,  # Generate a single completion
            stop=None,
        )

        formatted_text = response.choices[0].text.strip()
        flashcards = self._convert_string_to_dictionaries_list(formatted_text)

        return flashcards

    @staticmethod
    def _convert_string_to_dictionaries_list(string):
        """
        Convert a formatted string into a list of dictionaries.

        Each dictionary represents a flashcard and contains 'front' and 'back' keys.

        Parameters:
        - string (str): The formatted string to convert.

        Returns:
        - flashcard_dictionaries_list (list): A list of dictionaries representing flashcards.
        """
        lines = [line.strip() for line in string.split('\n')]
        flashcard_dictionaries_list = []
        card = {}
        for line in lines:
            if "Front:" in line or "Back:" in line or "Note Type:" in line:
                key, value = map(str.strip, line.split(":"))
                card[key.lower()] = value

            elif line == "":
                if card:  # Check if card is non-empty
                    flashcard_dictionaries_list.append(card)
                    card = {}
        if card:  # Append the last card if it is non-empty
            flashcard_dictionaries_list.append(card)
        return flashcard_dictionaries_list

    def __str__(self):
        """
        Return a string representation of the PassageFlashcard object.

        Returns:
        - representation (str): A string representation of the PassageFlashcard object.
        """
        return f"PassageFlashcard(passage='{self.passage}')"


if __name__ == "__main__":
    passage_text = """
    Python is a popular programming language known for its simplicity and readability.
    """

    passage_flashcards = PassageFlashcards(passage_text)
    flashcards = passage_flashcards.generate_flashcards(passage_text)

    for flashcard in flashcards:
        print(f"Question: {flashcard['front']}")
        print(f"Answer: {flashcard['back']}")
        print()
