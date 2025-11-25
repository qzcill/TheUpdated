
from app import db 

# --- Core Tables ---

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255)) 
    
    answers = db.relationship('UserAnswer', backref='user', lazy=True)
    recommendation = db.relationship('Recommendation', backref='user', uselist=False, lazy=True)

class QuizQuestion(db.Model):
    __tablename__ = 'quizquestions'
    question_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50)) 
    question_text = db.Column(db.Text)
    
    options = db.relationship('QuizOption', backref='question', lazy=True)
    user_answers = db.relationship('UserAnswer', backref='question', lazy=True)

class QuizOption(db.Model):
    __tablename__ = 'quizoptions'
    option_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('quizquestions.question_id'))
    option_text = db.Column(db.Text)
    value = db.Column(db.Integer) 

class UserAnswer(db.Model):
    __tablename__ = 'useranswers'
    answer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    question_id = db.Column(db.Integer, db.ForeignKey('quizquestions.question_id'))
    selected_option = db.Column(db.Integer, db.ForeignKey('quizoptions.option_id'))

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    rec_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True)
    career_path = db.Column(db.String(100))
    description = db.Column(db.Text)
    date_generated = db.Column(db.DateTime, default=db.func.current_timestamp())


from app import app, ma 

class OptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuizOption
        load_instance = True
        fields = ('option_id', 'option_text', 'value')

class FullQuestionSchema(ma.SQLAlchemyAutoSchema):
    options = ma.List(ma.Nested(OptionSchema))

    class Meta:
        model = QuizQuestion
        load_instance = True
        include_relationships = True
        fields = ('question_id', 'category', 'question_text', 'options')

quiz_schema = FullQuestionSchema(many=True)