from flask import Blueprint, jsonify, request, render_template
from models import Card, db, Transaction
import uuid
from datetime import datetime
import pytz

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/', methods=['GET','POST'])
def card_details():
    if request.method == 'POST':
        card_number = request.form['card_number']
        card = Card.query.filter_by(card_number = card_number).first()
        if card and card.name:
            data = {
                'name': card.name,
                'card_number':card.card_number
            }
            return render_template('display.html', data = data)
        else:
            data = {
                'message': "Data not found. Please register."
            }
            return render_template('home.html', data = data)
    return render_template('home.html', data = None)


@user_routes.route('/register', methods=['GET','POST'])
def register_card():
    if request.method == 'POST':
        card_number = request.form['card_number']
        name = request.form['name']
        pin = request.form['pin']
        confirm_pin = request.form['confirm_pin']
        card_id = str(uuid.uuid4())
        amount = 2000
        
        card_detail_exist = Card.query.filter_by(card_number = card_number).first()
        if card_detail_exist:
            data = {
                'message': "The card has already been registered."
            }
            return render_template('register.html', data = data)
        
        if pin != confirm_pin:
            data = {'message': "Your PINs do not match. Please re-enter." }
            return render_template('register.html', data = data)
        
        if card_number and name:
            new_card = Card(name = name, card_number = card_number, pin = pin, amount = amount, card_id = card_id)
            db.session.add(new_card)
            db.session.commit()        
            data = {'message': "Registration successful." }
            return render_template('home.html', data = data)
        
    return render_template('register.html', data = None)
    

@user_routes.route('/balance', methods=['GET','POST'])
def card_balance():
    if request.method == 'GET':
        global card    
        card_number = request.args.get('card_number',default="default", type=str)
        card = Card.query.filter_by(card_number = card_number).first()
        data = {"amount1":card.amount, "name":card.name, "display":"all"}
        return render_template('balance.html', data = data)
        
        
    if request.method == 'POST':    
        pin = request.form['pin']
        if int(pin) == int(card.pin):
            if card.amount == 0:
                card.amount = 1            
            data = {"amount":card.amount, "name":card.name}                           
            return render_template('balance.html', data = data)
        else:
            data = {
                "name":card.name,
                "display":"all",
                "message":"Incorrect pin"
            }
            return render_template('balance.html', data = data)
        

@user_routes.route('/withdrawal', methods=['GET','POST'])
def withdrawal():
    if request.method == 'GET':
        global card    
        card_number = request.args.get('card_number',default="default", type=str)
        card = Card.query.filter_by(card_number = card_number).first()
        data = { "name":card.name, "display":"all"}
        return render_template('withdrawal.html', data = data)

    if request.method == 'POST':
        if 'pin' in request.form:
            pin = request.form['pin']
            if int(pin) == int(card.pin):            
                data = {"name":card.name, "withdrawal_amount":"all"}
                return render_template('withdrawal.html', data = data)
            else:
                data = {
                    "name":card.name,
                    "display":"all",
                    "message":"Incorrect pin"
                }
                return render_template('withdrawal.html', data = data)
        else:
            amount = card.amount
            withdrawal = int(request.form['withdrawal'])
            if withdrawal > amount:
                data = {"name":card.name, "withdrawal_amount":"all", "message":"Insufficient balance"}
                return render_template('withdrawal.html', data = data)
            if withdrawal%500 !=0:
                data = {"name":card.name, "withdrawal_amount":"all", "message":"Enter amount in multiples of 500"}
                return render_template('withdrawal.html', data = data)
            
            if withdrawal <= amount and withdrawal%500 == 0:
                card = Card.query.filter_by(card_number=card.card_number).first()  # Find the card by card_number
                remaining_amount = card.amount - withdrawal
                card.amount = remaining_amount
                
                ist = pytz.timezone('Asia/Kolkata')
                date_time = datetime.now(ist)
                transaction_id = str(uuid.uuid4())
                new_transaction = Transaction(transaction_id = transaction_id, card_id = card.card_id, amount = withdrawal, transaction_type = "withdrawal", date_time = date_time)
                db.session.add(new_transaction)  
                db.session.commit()                
                data = {"name":card.name, "msg":"Amount withdrawn successfully.", "remaining_amount":remaining_amount}
                return render_template('withdrawal.html', data = data)
                
        
@user_routes.route('/deposit', methods=['GET','POST'])
def deposit():
    if request.method == 'GET':
        global card    
        card_number = request.args.get('card_number',default="default", type=str)
        card = Card.query.filter_by(card_number = card_number).first()
        data = {"name":card.name, "display":"all"}
        return render_template('deposit.html', data = data)
        
    if request.method == 'POST':
        if 'pin' in request.form:
            pin = request.form['pin']
            if int(pin) == int(card.pin):            
                data = {"name":card.name, "deposit":"all"}
                return render_template('deposit.html', data = data)
            else:
                data = {
                    "name":card.name,
                    "display":"all",
                    "message":"Incorrect pin"
                }
                return render_template('deposit.html', data = data)
        else:
            amount = card.amount
            deposit = int(request.form['deposit'])            
            if deposit%500 !=0:
                data = {"name":card.name, "deposit":"all", "message":"Notes should be in multiples of 500."}
                return render_template('deposit.html', data = data)
            
            if deposit%500 == 0:
                card = Card.query.filter_by(card_number=card.card_number).first()  # Find the card by card_number
                remaining_amount = card.amount + deposit
                card.amount = remaining_amount 
                
                ist = pytz.timezone('Asia/Kolkata')
                date_time = datetime.now(ist)
                transaction_id = str(uuid.uuid4())
                new_transaction = Transaction(transaction_id = transaction_id, card_id = card.card_id, amount = deposit, transaction_type = "deposit", date_time = date_time)
                db.session.add(new_transaction)
                db.session.commit()                
                data = {"name":card.name, "msg":"Amount deposited successfully.", "remaining_amount":remaining_amount}
                return render_template('deposit.html', data = data)


        
@user_routes.route('/transaction', methods=['GET','POST'])
def transaction():
    if request.method == 'GET':
        global card    
        card_number = request.args.get('card_number',default="default", type=str)
        print(card_number)
        card = Card.query.filter_by(card_number = card_number).first()
        data = {"name":card.name, "display":"all"}
        return render_template('mini_statement.html', data = data)
        
    if request.method == 'POST':
        if 'pin' in request.form:
            pin = request.form['pin']
            if int(pin) == int(card.pin):  
                card = Card.query.filter_by(card_number = card.card_number).first()
                transaction = Transaction.query.filter_by(card_id = card.card_id).limit(5).all()
                data = {"name":card.name, "transaction":transaction }
                return render_template('mini_statement.html', data = data)
            else:
                data = {
                    "name":card.name,
                    "display":"all",
                    "message":"Incorrect pin"
                }
                return render_template('mini_statement.html', data = data)
        