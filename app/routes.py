from app import app, db
from flask import render_template, abort, redirect, url_for, session, request, flash, send_from_directory, send_file
from pyotp import TOTP
from app.models import Admins, Users
import string, random, os
from werkzeug.utils import secure_filename
from app import tools
from app import divider as dv
from app import encrypter as enc
from app import decrypter as dec
from app import restore as rst

ROWS_PER_PAGE = 2

UPLOAD_FOLDER = './uploads/'
UPLOAD_KEY = './key/'
ALLOWED_EXTENSIONS = set(['pem'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_KEY'] = UPLOAD_KEY

#generate userid 
def userid(chars=string.ascii_uppercase+string.digits, len=6):
	return ''.join(random.SystemRandom().choice(chars) for _ in range(len))

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def start_encryption():
	dv.divide()
	tools.empty_folder('uploads')
	enc.encrypter()
	return render_template('success.html')

def start_decryption():
	dec.decrypter()
	tools.empty_folder('key')
	rst.restore()
	return render_template('restore_success.html')

@app.route('/decrypt/<path:filename>')
def return_key(filename):
    list_directory = tools.list_dir('key')
    filename = './key/My_Key.pem'
    return send_from_directory(os.getcwd()+'/decrypt', path=filename)

@app.route('/return-file/')
def return_file():
	list_directory = tools.list_dir('restored_file')
	filename = './restored_file/' + list_directory[0]
	print ("****************************************")
	print (list_directory[0])
	print ("****************************************")
	return send_file(filename, attachment_filename=list_directory[0], as_attachment=True)

@app.route('/download/')
def downloads():
	return render_template('download.html')

@app.route('/upload')
def call_page_upload():
	return render_template('upload.html')

@app.route('/home')
def back_home():
	tools.empty_folder('key')
	tools.empty_folder('restored_file')
	return render_template('index.html')
    
@app.route('/data', methods=['GET', 'POST'])
def upload_file():
	tools.empty_folder('uploads')
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return 'NO FILE SELECTED'
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
			return start_encryption()
		return 'Invalid File Format !'
	
@app.route('/download_data', methods=['GET', 'POST'])
def upload_key():
	tools.empty_folder('key')
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return 'NO FILE SELECTED'
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_KEY'], file.filename))
			return start_decryption()
		return 'Invalid File Format !'
        
    
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']
            token = request.form['token']
            
            check = Users.query.filter_by(email=email).first()
            if check:
                if check.password == password:
                    if TOTP('base32secret3232').now() == token:
                        session['email'] = email
                        return redirect(url_for('dashboard'))
                    flash('Wrong token')
                    return redirect(url_for('index'))
                flash('Wrong password')
                return redirect(url_for('index'))
            flash('Wrong Email')
            return redirect(url_for('index'))
        
        return render_template('login.html')
    except:
        return redirect(url_for('index'))
    
@app.route('/alogin', methods=['POST', 'GET'])
def alogin():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            check = Admins.query.filter_by(email=email, password=password).first()
            if check:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index'))
        return render_template('alogin.html')
    except:
        return redirect(url_for('index'))
        
@app.route('/dashboard')
def dashboard():
    try:
        return render_template('dashboard.html')
    except:
        return redirect(url_for('index'))
        
@app.route('/register', methods=['POST', 'GET'])
def register():
    try:
        if request.method == "POST":
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            job = request.form['job']
            
            _userid = userid()
            
            addRec = Users(email=email, username=username, password=password, job=job, userid=_userid)
            db.session.add(addRec)
            db.session.commit()
            flash("New record added!!")
            return redirect(url_for('viewRec'))
        return render_template('register.html')
    except:
        return redirect(url_for('index'))
        
@app.route('/viewRec')
def viewRec():
    try:
        page = request.args.get('page', 1, type=int)
        viewRec = Users.query.order_by(Users.id.desc()).paginate(page=page, per_page=ROWS_PER_PAGE)
        nums = Users.query.all()
        return render_template('viewRec.html', viewRec=viewRec, nums=nums)
    except:
        return redirect(url_for('index'))
        
@app.route('/admin')
def admin():
    try:
        return render_template('admin.html')
    except:
        return redirect(url_for('index'))
        
@app.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('index'))
    except:
        return redirect(url_for('index'))
    