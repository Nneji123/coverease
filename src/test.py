from datetime import datetime
from models import User, Letter
from app import db

# create a new user
new_user = User(username='john', email='john@example.com', password='password')
db.session.add(new_user)
db.session.commit()

# create a new letter for the user
new_letter = Letter(content='Hello, world!', user=new_user)
db.session.add(new_letter)
db.session.commit()