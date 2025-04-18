from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

  def __init__(self, username, password):
    self.username= username
    self.set_password(password)

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)



  def create_review(self, student_id, text, rating):
    review = Review(student_id=student_id, user_id=self.id, text=text, rating=rating)
    db.session.add(review)
    db.session.commit()
    return review
  def delete_review(self, review_id):
    review = Review.query.get(review_id)
    db.session.delete(review)
    db.session.commit()
    return review
    
class Student(db.Model):
  id = db.Column(db.String(9), primary_key=True)
  first_name = db.Column(db.String(80), nullable=False)
  last_name = db.Column(db.String(80), nullable=False)
  image = db.Column(db.String(80), nullable=False)
  programme = db.Column(db.String(80), nullable=False)
  start_year = db.Column(db.Integer, nullable=False)
  reviews = db.relationship('Review', backref='student', lazy=True)


  def average_rating(self):
    if len(self.reviews) == 0:
      return 0 
    return sum([review.rating for review in  self.reviews]) / len(self.reviews)

  
class Review(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  student_id = db.Column(db.String(9), db.ForeignKey('student.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  text = db.Column(db.String(255), nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  user = db.relationship('User', backref='reviews', lazy=True)
