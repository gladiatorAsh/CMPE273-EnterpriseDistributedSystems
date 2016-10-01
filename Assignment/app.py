from flask import Flask, request, flash, url_for, redirect, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_api import status
from sqlalchemy.inspection import inspect
#from sqlalchemy import create_engine
#import MySQLdb

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///expenses.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:admin@172.17.0.3/CMPE273'
#app.config['SECRET_KEY']='ash'
db=SQLAlchemy(app)
#engine = create_engine('mysql+pymysql://root:admin@172.17.0.3/CMPE273')
#conn=engine.connect();

class Serializer(object):
	
	def serialize(self):
		return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

	@staticmethod
	def serialize_list(l):
		return [m.serialize() for m in l]

class expenses(db.Model):
	id=db.Column('id',db.Integer, autoincrement=True,primary_key=True)
	name=db.Column('name',db.String(100))
	email=db.Column('email',db.String(100))
	category=db.Column('category',db.String(100))
	description=db.Column('description',db.String(100))
	link=db.Column('link',db.String(100))
	estimated_costs=db.Column('estimated_costs',db.Integer)
	submit_date=db.Column('submit_date',db.String(100))
	status=db.Column('status',db.String(100))
	decision_date=db.Column('decision_date',db.String(100))

	def serialize(self):
		d = Serializer.serialize(self)
		return d

def __init__(self,name,email,category,description,link,estimated_costs,submit_date,status,decision_date):
	if name is not None:
			self.name= name
	if email is not None:
			self.email=email
	if category is not None:
			self.category=category
	if description is not None:
			self.description=description
	if link is not None:
			self.link=link
	if estimated_costs is not None:
			self.estimated_costs=estimated_costs
	if submit_date is not None:
			self.submit_date=submit_date
	if status is not None:
			self.status=status
	if decision_date is not None:
			self.decision_date=decision_date

	
@app.route('/v1/expenses',methods=['POST'])
def save_expenses():
		
			#args=request.args
			args=request.get_json(force=True)
			#args=request.data
			expense=expenses(name=args.get('name'),email=args.get('email'),category=args.get('category'),description=args.get('description'),link=args.get('link'),estimated_costs=args.get('estimated_costs'),
							submit_date=args.get('submit_date'),status=args.get('status'),decision_date=args.get('decision_date'))

			db.session.add(expense)
			db.session.commit()
			return jsonify(expense.serialize()),status.HTTP_201_CREATED,{'Content-Type': 'application/json'}

@app.route('/v1/expenses/<int:expense_id>', methods = ['PUT'])
def edit_expenses(expense_id):

			#args=request.args
			#args=request.json
			args=request.get_json(force=True)
			old_expense=expenses.query.filter_by(id = expense_id).first()
			if(old_expense is None):
				return '',status.HTTP_404_NOT_FOUND,{'Content-Type': 'application/json'}
			else:
				new_expense=expenses(name=args.get('name'),email=args.get('email'),category=args.get('category'),description=args.get('description'),link=args.get('link'),estimated_costs=args.get('estimated_costs'),
									submit_date=args.get('submit_date'),status=args.get('status'),decision_date=args.get('decision_date'))
				
				copy_expense(old_expense, new_expense)

				db.session.commit()
				return '',status.HTTP_202_ACCEPTED,{'Content-Type': 'application/json'}

@app.route('/v1/expenses/<int:expense_id>', methods = ['DELETE'])
def delete_expenses(expense_id):

			expense=expenses.query.filter_by(id = expense_id).first()
			if(expense is None):
				return '',status.HTTP_404_NOT_FOUND,{'Content-Type': 'application/json'}
			else: 
				db.session.delete(expense)
				db.session.commit()
				return '',status.HTTP_204_NO_CONTENT,{'Content-Type': 'application/json'}

@app.route('/v1/expenses/<int:expense_id>',methods=['GET'])
def show_one(expense_id):

	#return render_template('show_one.html',expenses=expenses.query.filter_by(id=expense_id))
			expense=expenses.query.filter_by(id=expense_id).first()
			if(expense is None):
				return jsonify(expense),status.HTTP_404_NOT_FOUND,{'Content-Type': 'application/json'}
			else:
				return jsonify(expense.serialize()),status.HTTP_200_OK,{'Content-Type': 'application/json'}

def copy_expense(old_expense,new_expense):
		if new_expense.name is not None:
				old_expense.name= new_expense.name
		if new_expense.email is not None:
				old_expense.email=new_expense.email
		if new_expense.category is not None:
				old_expense.category=new_expense.category
		if new_expense.description is not None:
				old_expense.description=new_expense.description
		if new_expense.link is not None:
				old_expense.link=new_expense.link
		if new_expense.estimated_costs is not None:
				old_expense.estimated_costs=new_expense.estimated_costs
		if new_expense.submit_date is not None:
				old_expense.submit_date=new_expense.submit_date
		if new_expense.status is not None:
				old_expense.status=new_expense.status
		if new_expense.decision_date is not None:
				old_expense.decision_date=new_expense.decision_date


if __name__ == "__main__":
	db.create_all()
	app.run(debug=True,host='0.0.0.0')