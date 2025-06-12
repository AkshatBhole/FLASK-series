from market import db
from market import bcrypt
from flask_login import UserMixin
from market import login_manager # Import UserMixin for using of all methods in login as shjown in documentation 
# press F12 to seee mixins.py file 

@login_manager.user_loader # This decorator is used to tell Flask-Login how to load a user given its 
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):  # UserMixin provides default implementations for the methods that Flask-Login expects user objects to have
    id=db.Column(db.Integer (),primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email_address=db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash=db.Column(db.String(length=60),nullable=False)
    budget=db.Column(db.Float(),nullable=False,default=1000.00)  # default budget is 1000.00
    items=db.relationship('Item',backref='owned_user',lazy=True)  # one to many relationship with Item model
    # lazy=True means that the items will be loaded only when accessed, not immediately when the user is loaded
    # backref='owned_user' creates a virtual column in Item model that refers to the User model

    @property
    def prettier_budget(self):
      if self.budget.is_integer():
        return f"{int(self.budget):,}$"
      else:
        return f"{self.budget:,.2f}$"



    @property
    def password(self):
        return self.password_hash  # Fixed: Return the hashed password instead of causing a recursive loop
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash=bcrypt.generate_password_hash(plain_text_password).decode('utf-8') # this will be used to set the password_hash field

    def check_password(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password) # This method checks if the attempted password matches the hashed password stored in the database
    
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items
    


class Item(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(length=30),nullable=False,unique=True)
    price=db.Column(db.Float(),nullable=False)
    barcode=db.Column(db.String(length=12),nullable=False,unique=True)
    description=db.Column(db.String(length=1024),nullable=False,unique=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))  # foreign key to User model    

    def __repr__(self):                        # ye bass apne ko <Item> terminal me ke jageh Iphone 10 dikhtaa hai... better way to show the data
        return f'Item {self.name}'
    
    def buy(self, user):
        self.owner = user.id  # Fixed: Use self.owner instead of self.owner_id
        user.budget -= self.price
        # Removed db.session.commit() to handle in routes.py

    def sell(self, user):
        self.owner = None  # Fixed: Use self.owner instead of self.owner_id
        user.budget += self.price
        # Removed db.session.commit() to handle in routes.py