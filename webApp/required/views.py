from webApp import app
from webApp.required.databs import *
from flask import render_template, url_for, request, redirect, session
import symmetric,important,timeit,time,hashlib,subprocess
app.secret_key="lkadsjfkldajslkfgaklsdflkals"


#--------------------------main page------------------------------#

@app.route("/")
def index():
	print "hello"
	if(("username" not in session) or ("cookie" not in session)):
		return render_template('login.html')
	return render_template("index.html")

#-------------------------login page -----------------------------#


@app.route("/login")
def login():
	if(("username" in session) and ("cookie" in session)):
		return redirect(url_for('index')) 
	return render_template("login.html")

#-----------------------register-----------------------------------#

@app.route("/register")
def register():
	if(("username" in session) and("cookie" in session)):
		return redirect(url_for('index'))
	return render_template("register.html")


#-------------------------charts ----------------------------------#

@app.route("/charts")
def charts():
	cont= sqlite3.connect('dataTable.db')
	c = cont.cursor()
	#c.execute("CREATE TABLE students ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'Firstname' TEXT,'lastName' TEXT,'email' TEXT UNIQUE, 'password' TEXT,'cookie' TEXT)")
	#c.execute("DROP TABLE compl")
	#c.execute("CREATE TABLE compl ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'string' VARCHAR(100),'ceaser' REAL,'vigenere' REAL,'playfair' REAL,'rc4' REAL,'rot13' REAL,'email' TEXT) ") 
	c.execute("SELECT string,ceaser,vigenere,playfair,rc4,rot13,email from compl where email='%s'"%(session['username']))
	results=c.fetchall()
	cont.commit()
	cont.close()
	a= time.localtime()
	tm= "{}:{}".format(a.tm_hour,a.tm_min)
	data=[results[-1][1],results[-1][2],results[-1][3],results[-1][4],results[-1][5]]
	return render_template("charts.html",dats=data,tim=tm)

#-------------------------tables ----------------------------------#

@app.route("/tables")
def tables():
	cont= sqlite3.connect('dataTable.db')
	c = cont.cursor()
	#c.execute("CREATE TABLE students ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'Firstname' TEXT,'lastName' TEXT,'email' TEXT UNIQUE, 'password' TEXT,'cookie' TEXT)")
	#c.execute("DROP TABLE compl")
	#c.execute("CREATE TABLE compl ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'string' VARCHAR(100),'ceaser' REAL,'vigenere' REAL,'playfair' REAL,'rc4' REAL,'rot13' REAL,'email' TEXT) ") 
	c.execute("SELECT string,ceaser,vigenere,playfair,rc4,rot13,email from compl where email='%s'"%(session['username']))
	results=c.fetchall()
	cont.commit()
	cont.close()
	a= time.localtime()
	tm= "{}:{}".format(a.tm_hour,a.tm_min)
	return render_template("tables.html",values=results,tim=tm)

#-------------------------compare ---------------------------------#

@app.route("/compare")
def compare():
	if("username" not in session):
		return render_template('login.html')
	if("cookie" not in session):
		return render_template('login.html')
	return render_template("compare.html",value=[["",1],["","",1],["","",1],["","",1],["","",1],["","",1]])


#------------------Encrypt Function -------------------------------#

@app.route("/encrypt",methods=["POST"])
def encrypt():
	dats={"caesar":0,"vigenere":0,"playfair":0,"rc4":0,"rot13":0}
	msg= request.form['plain']
	print "hiddenValue is {}".format(request.form['hiddenValue'])
	val = request.form['hiddenValue']
	caesar=request.form['caesar'],request.form['caesar_key'],int(request.form['caesar_hkey'])
	vigenere=request.form['vigenere'],request.form['vigenere_key'],int(request.form['vigenere_hkey'])
	playfair=request.form['playfair'],request.form['playfair_key'],int(request.form['playfair_hkey'])
	rc4=request.form['rc4'],request.form['rc4_key'],int(request.form['rc4_hkey'])
	rot13=request.form['rot13'],request.form['rot13_key'],int(request.form['rot13_hkey'])
	trval=int(request.form['masterVal'])
	a,b=0,0
	if(val=='-1'):

		try:
			a=time.clock()
			caesar=symmetric.caesar(msg,request.form['caesar'],request.form['caesar_key'],trval)
			b=time.clock()
		except Exception:
			ceaser=["Error in text",request.form['caesar_key'],int(request.form['caesar_hkey'])]
		dats["caesar"]=b-a
		a,b=0,0

		try:
			a=time.clock()
			vigenere=symmetric.vigenere(msg,request.form['vigenere'],request.form['vigenere_key'],trval)
			b=time.clock()
		except Exception:
			vigenere=["Error in text",request.form['vigenere_key'],int(request.form['vigenere_hkey'])]
		dats["vigenere"]=b-a
		a,b=0,0

		try:
			a=time.clock()
			playfair=symmetric.playfair(msg,request.form['playfair'],request.form['playfair_key'],trval)
			b=time.clock()
		except Exception:
			playfair=["Error in text",request.form['playfair_key'],int(request.form['playfair_hkey'])]
		dats["playfair"]=b-a
		a,b=0,0

		try:
			a=time.clock()
			rc4 = symmetric.RC4(msg,request.form['rc4'],request.form['rc4_key'],trval)
			b=time.clock()
		except Exception:
			rc4=["Error in text",request.form['rc4_key'],int(request.form['rc4_hkey'])]
		dats["rc4"]=b-a
		a,b=0,0

		try:
			a=time.clock()
			rot13 = symmetric.RoT13(msg,request.form['rot13'],request.form['rot13_key'],trval)
			b=time.clock()
		except Exception:
			rot13=["Error in text",request.form['rot13_key'],int(request.form['rot13_hkey'])]
		dats["rot13"]=b-a
		a,b=0,0
		cont= sqlite3.connect('dataTable.db')
		c = cont.cursor()
		#c.execute("CREATE TABLE students ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'Firstname' TEXT,'lastName' TEXT,'email' TEXT UNIQUE, 'password' TEXT,'cookie' TEXT)")
		#c.execute("DROP TABLE compl")
		#c.execute("CREATE TABLE compl ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'string' VARCHAR(100),'ceaser' REAL,'vigenere' REAL,'playfair' REAL,'rc4' REAL,'rot13' REAL,'email' TEXT) ") 
		c.execute("INSERT INTO compl ('string','ceaser','vigenere','playfair','rc4','rot13','email') VALUES ('%s',%f,%f,%f,%f,%f,'%s')"%(msg,dats['caesar'],dats['vigenere'],dats['playfair'],dats['rc4'],dats['rot13'],session['username']))
		print dats
		cont.commit()
		cont.close()

		print dats

		trval*=-1
		#request.form['caesar']=symmetric.caesar(msg,2)
		return render_template('compare.html',value=[[msg,trval],caesar,vigenere,playfair,rc4,rot13])
	elif(val=='0'):
		print "val is called"
		caesar=symmetric.caesar(msg,request.form['caesar'],request.form['caesar_key'],int(request.form['caesar_hkey']))
	elif(val=='1'):
		vigenere=symmetric.vigenere(msg,request.form['vigenere'],request.form['vigenere_key'],int(request.form['vigenere_hkey']))
	elif(val=='2'):
		playfair=symmetric.playfair(msg,request.form['playfair'],request.form['playfair_key'],int(request.form['playfair_hkey']))
	elif(val=='3'):
		rc4 = symmetric.RC4(msg,request.form['rc4'],request.form['rc4_key'],int(request.form['rc4_hkey']))
	elif(val=='4'):
		rot13 = symmetric.RoT13(msg,request.form['rot13'],request.form['rot13_key'],int(request.form['rot13_hkey']))
	print caesar[2],vigenere[2],playfair[2],rc4[2],rot13[2]
	return render_template('compare.html',value=[[msg,trval],caesar,vigenere,playfair,rc4,rot13])

#----------------------hash decrypter -------------------------------#
@app.route("/hashdecrypter")
def hashdecrypter():
	return render_template('hash.html',values=["","","","",""])

@app.route("/hashFind",methods=["POST"])
def hashFind():
	print request.form['hash']
	result=["not found","",True,"hashType",request.form['hash']]
	if(result[2]):
		conn= sqlite3.connect('students.db')
		c = conn.cursor()
		c.execute("SELECT word from hashes where md5='%s'"%(request.form['hash'])) 
		results=c.fetchall()
		if(len(results)==1):
			result[2]=False
			result[3]="MD5"
			for i in results:
				result[0]=i[0]
	
	if(result[2]):
		conn= sqlite3.connect('students.db')
		c = conn.cursor()
		c.execute("SELECT word from hashes where sha256='%s'"%(request.form['hash'])) 
		results=c.fetchall()
		if(len(results)==1):
			result[2]=False
			result[3]="SHA256"
			for i in results:
				result[0]=i[0]
	
	if(result[2]):
		conn= sqlite3.connect('students.db')
		c = conn.cursor()
		c.execute("SELECT word from hashes where sha512='%s'"%(request.form['hash'])) 
		results=c.fetchall()
		if(len(results)==1):
			result[2]=False
			result[3]="SHA512"
			for i in results:
				result[0]=i[0]
	conn.commit()
	conn.close()
	return render_template('hash.html',values=result)
	




#----------------------Key Generator -------------------------------#

@app.route("/key")
def key():
	output = subprocess.Popen(["openssl", "genpkey" " -algorithm RSA"  " -out privatekey.pem"], stdout=subprocess.PIPE).communicate()[0]
	print output
	return render_template("keyGenerate.html",public="" ,private="")

#---------------------- Generate Key -------------------------------#

@app.route("/geneKey",methods=["POST"])
def geneKey():
	bit=int(request.form['bits'])
	bit = bit-bit%256
	if(bit<1024):
		bit+=256
	public=symmetric.generate_RSA(bit)
	private=""
	return render_template("keyGenerate.html",public,private)

#------------------Error handelling  ----------------------------#
	
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('errors.html',value=["file not found","looks like you got wrong link","404"]), 404

@app.errorhandler(405)
def illegal_access(e):
	return render_template('errors.html',value=["Method not allowed","Looks like someone trying to hack","405"]),405
#----------------------- Hash Generator ---------------------------#

@app.route("/hashGenerator")
def hashGenerator():
	return render_template("hashGenerate.html",value=["","","","","","",""])	

#-----------------------Hash Create-------------------------#
@app.route("/hashCreate",methods=["POST"])
def hashCreate():
	values=[request.form['plain'],"","","","","",""]
	values[1]=hashlib.md5(str(values[0])).hexdigest()
	values[2]=hashlib.sha1(str(values[0])).hexdigest()
	values[3]=hashlib.sha224(str(values[0])).hexdigest()
	values[4]=hashlib.sha256(str(values[0])).hexdigest()
	values[5]=hashlib.sha384(str(values[0])).hexdigest()
	values[6]=hashlib.sha512(str(values[0])).hexdigest()
	return render_template("hashGenerate.html",value=values)	


#------------------------login validate-----------------------------#
@app.route("/success", methods=["POST"])
def success():
	if(request.form['username']==""):
		return redirect(url_for('login'))
	elif(request.form['password']==""):
		return redirect(url_for('login'))
	email = request.form['username']
	password= request.form['password']

	if(compare_credentials(email,password)):
		session['username']=email
		session['cookie']= important.randomString(30)
		update_credentials(session['cookie'],email)
		return redirect(url_for('index'))
	return redirect(url_for('login'))


#--------------------Register Validate---------------------------------#
@app.route("/check_register", methods=["POST"])
def check_register():
	try:
		print "{},{},{},{},{}".format(request.form['firstName'],request.form['lastName'],request.form['email'],request.form['password'],request.form['confirmPassword'])
		if(request.form['firstName']==""):
			return redirect(url_for('register'))
		elif(request.form['email']==""):
			return redirect(url_for('register'))
		elif(request.form['password']!=request.form['confirmPassword']):
			return redirect(url_for('register'))
		elif(request.form['password']==""):
			return redirect(url_for('register'))
	except KeyError:
			print "key error"
			return render_template("register.html")
	data =insert_into_database(request.form['firstName'],request.form['lastName'],request.form['email'],request.form['password'])
	if(data):
		return redirect(url_for('login'))
	else:
		print "Something wrong with database"
		return redirect(url_for('register'))

#-----------------------logout------------------------------#

@app.route("/logout")
def logout():
	if("username" in session):
		session.pop('username')
	if("cookie" in session):
		session.pop('cookie')
	return redirect(url_for('login'))
