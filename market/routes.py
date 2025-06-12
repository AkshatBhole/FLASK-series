from market import app,render_template, db
from flask import redirect, url_for ,flash  # <-- ADD THIS
from market.models import Item,User
from market.forms import RegisterForm,LoginForm,PurchaseItemForm, SellItemForm
from flask_login import login_user,logout_user  # <-- ADD THIS
from flask_login import login_required 
from flask import request
from flask_login import current_user
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route("/")
def home_page(): 
    return render_template("home.html")

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        logger.debug(f"Attempting to purchase item: {purchased_item}")
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            logger.debug(f"Item found: {p_item_object.name}, Price: {p_item_object.price}, User Budget: {current_user.budget}")
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                db.session.commit()  # Commit changes to the database
                logger.debug(f"After purchase commit - Item: {p_item_object.name}, Owner: {p_item_object.owner}, User Budget: {current_user.budget}")
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                logger.warning(f"User {current_user.username} cannot purchase {p_item_object.name}: Insufficient budget")
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
        #Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            logger.debug(f"Item found: {s_item_object.name}, Owner: {s_item_object.owner}")
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                db.session.commit()  # Commit changes to the database
                logger.debug(f"After sell commit - Item: {s_item_object.name}, Owner: {s_item_object.owner}, User Budget: {current_user.budget}")
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                logger.warning(f"User {current_user.username} cannot sell {s_item_object.name}")
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        logger.debug(f"Current User ID: {current_user.id}")
        items = Item.query.filter_by(owner=None).all()  # Fetch available items
        owned_items = Item.query.filter_by(owner=current_user.id).all()  # Fetch owned items
        logger.debug(f"Owned Items: {[item.name for item in owned_items]}")
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register',methods=['GET','POST'])  # <-- ADD methods=['GET', 'POST']
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # Here you would typically handle the registration logic, such as saving the user to the database
        user_to_create = User(  
                                                 # ye sab User  KA INSTANT BANAE K LIYE LIKHA BRAXKET ME
            username=form.username.data,
            email_address=form.email_address.data,
            # password_hash=form.password1.data 
            password=form.password1.data  # Use the password setter to hash the password....ye apna models.py me s aaya hai @property e se 2nd vaki
        )

        db.session.add(user_to_create)        #submit changes to db                  # Add the new user to the session
        db.session.commit()
        login_user(user_to_create)
        flash(f'account created successfully you are now logged in as  {user_to_create.username}', category='success')   
        return redirect(url_for('market_page')) # Redirect to the market page after successful registration
    
    if form.errors != {}: # If there are errors, print them to the console
        for err_msg in form.errors.values():
            flash(f'there wasa problem with creating a user: {err_msg}',category='danger')
        # You can also log the errors or handle them as needed

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        # Get the user by username
        attempted_user = User.query.filter_by(username=form.username.data).first() # Attempt to find the user in the database
        if attempted_user and attempted_user.check_password(attempted_password=form.password.data): # Check if the user exists and if the password matches
            # If the user exists and the password is correct, log them in
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))  # Redirect to the market page after successful login
        else:
            flash('Username and password do not match. Please try again.', category='danger')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was a problem with logging in: {err_msg}', category='danger')
    return render_template('login.html', form=form)  # ✅ PASS FORM HERE

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out.", category='info')
    return redirect(url_for('home_page'))