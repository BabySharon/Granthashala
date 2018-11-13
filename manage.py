from flask import Flask, render_template, request,session

import sqlite3
app = Flask(__name__)
app.secret_key = 'any random string'

''' welcome link'''
#@app.route('/home',defaults={'bookname': ""})
@app.route('/home')
@app.route('/home/<no>')
#no of book that is book id or primary key
#@app.route('/home/<bookname>')
def home( no = None):
	session.pop('em',None)
	conn = sqlite3.connect('book.db')
	cur = conn.cursor()
	if no == None:
		return render_template('home.html')
		
	else:
		#To dispaly full details of book
		cur.execute("SELECT  * from book where no =?",(no,))
		ReqBook = cur.fetchall()
		return render_template("home.html",ReqBook = ReqBook)

@app.route("/login")
def signlog():
	return render_template("signlog.html")

@app.route("/addbook", methods =['GET','POST'])

def addbook( ):
	
	conn = sqlite3.connect('book.db')
	cur = conn.cursor()
	
	

	
	if 'signup' in request.form.keys():
		name = request.form['name']  
		email = request.form['email']
		password = request.form['pswd']
		phone = request.form['phno']
		location = request.form['location']
			
		cur.execute("INSERT INTO user(name,email,password,phno,location) VALUES(?,?,?,?,?)",(name,email,password,phone,location))
		conn.commit();
		msg = "sign up successfull"
		return render_template("profile.html", msg = msg, name = name)
				
		
	if 'login' in request.form.keys():
		email = request.form['email']
		password = request.form['pswd']
		
		
		cur.execute("SELECT * FROM user WHERE email = ? and password = ?",(email, password) )
		login_query = cur.fetchall()
		
		if  not login_query:
			msg = "Invalid User"
			conn.commit()
			return render_template("signlog.html",msg = msg)
		else:
			msg = "login succesful"
			return render_template("profile.html",msg = msg, login_query = login_query)
		
	conn.close()				
@app.route("/book", methods =['POST','GET'])
def book():
	if request.method == "GET":
		try:
			conn = sqlite3.connect('book.db')
			cur = conn.cursor()
			#if 'education' in form.request:
			book_name = request.form['book_name']				
			author = request.form['author']
			price = request.form['price']
			description = request.form['description']
			booktype = request.form['booktype']
			genre = request.form['genre']
			cur.execute("INSERT INTO edubook VALUES(?,?,?,?,?)",(book_name,author,price,description,booktype,genre))
			msg = "Book added"
			conn.commit();
			return render_template('profile.html', msg = msg)

			
		except:
			conn.rollback()
		finally:
			conn.close()
''' For searching a book in textbox of homepage'''
@app.route('/search', methods = ['POST','GET'])
def search():
	if request.method == "POST":
		searchBook = request.form['searchBook']
		conn = sqlite3.connect('book.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM book WHERE name = ? ",(searchBook,))
		res= cur.fetchall()
		
		
		if len(res) == 0 :
			msg = "No results found :("
			return render_template("home.html",msg=msg)
		else:
			listlength = str(len(res))
			msg = listlength + " books found" 
			return render_template('home.html', msg = msg, res = res)

@app.route('/logout')
def logout():
	session.pop('em',none)
	return render_template('home.html')
	
if __name__ == "__main__":
  	app.run(host = '192.168.43.7', port = 8080, debug = True)
