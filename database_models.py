from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Passage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    flashcards = db.relationship('Flashcard', backref='passage', lazy=True)

    def __init__(self, content):
        self.content = content


class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    passage_id = db.Column(db.Integer, db.ForeignKey('passage.id'), nullable=False)

    def __init__(self, question, answer, passage_id):
        self.question = question
        self.answer = answer
        self.passage_id = passage_id

class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    passage_id = db.Column(db.Integer, db.ForeignKey('passage.id'), nullable=False)

    def __init__(self, question, answer, passage_id):
        self.question = question
        self.answer = answer
        self.passage_id = passage_id

if __name__ == '__main__':
    print("database_models")