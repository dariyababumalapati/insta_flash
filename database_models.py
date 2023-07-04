from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32), unique=True, nullable=False)
    passages = db.relationship('Passage', backref='user', lazy=True)
    # Add other columns as needed

    def __init__(self, user_id):
        self.user_id = user_id
        # Initialize other columns as needed

    def save(self):
        db.session.add(self)
        db.session.commit()

class Passage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passage_title = db.Column(db.Text)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flashcards = db.relationship('Flashcard', backref='passage', lazy=True)

    def __init__(self, content, passage_title, user_id):
        self.content = content
        self.passage_title = passage_title
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    passage_id = db.Column(db.Integer, db.ForeignKey('passage.id'), nullable=False)

    def __init__(self, question, answer, passage_id):
        self.question = question
        self.answer = answer
        self.passage_id = passage_id

    def save(self):
        db.session.add(self)
        db.session.commit()

class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    passage_id = db.Column(db.Integer, db.ForeignKey('passage.id'), nullable=False)

    def __init__(self, question, answer, passage_id):
        self.question = question
        self.answer = answer
        self.passage_id = passage_id

    def save(self):
        db.session.add(self)
        db.session.commit()


if __name__ == '__main__':
    print("database_models")