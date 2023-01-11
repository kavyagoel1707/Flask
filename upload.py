from flask import Blueprint, render_template, flash,send_file,redirect, url_for,request, current_app as app
from __init__ import create_app,db
from werkzeug.utils import secure_filename
from models import Files
import os
upload=Blueprint('upload',__name__)
#defining paths for uploading images and documents
UPLOAD_IMAGE='uploadimage/' 
UPLOAD_DOCUMENT='uploaddoc/'
#for working on the app outside the framework
app=create_app()
app.app_context().push()
#configuring the paths
app.config['UPLOAD_IMAGE']=UPLOAD_IMAGE
app.config['UPLOAD_DOCUMENT']=UPLOAD_DOCUMENT
#defining the maximum content length
app.config['MAX_CONTENT_LENGTH'] = 2*100
ALLOWED_EXTENSIONS=set(['png','jpg','gif'])
ALLOWED_EXTENSIONS1=set(['txt','pdf'])
#to check if the uploaded file is from allowed extensions 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def allowed_filedoc(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS1
#for uploading images
@upload.route("/uploads",methods=['GET','POST'])
def uploads():
    if request.method=='POST':
        #retrieving the file
        file=request.files['file']
        if file and allowed_file(file.filename): #if file is from allowed extensions
            filename=secure_filename(file.filename) #checking security
            new_file=Files(fName=filename,type='image') #creating file record
            db.session.add(new_file) #adding file record
            db.session.commit()
            filedata=Files.query.order_by(Files.id) #retrieving all the records
            return render_template('view.html',filedata=filedata,new_file=new_file)
        else:
            #if file is not an image
            flash('Upload an image')
            return render_template('upload.html')
    return render_template('upload.html')
#for uploading docs
@upload.route("/uploaddoc",methods=['GET','POST'])
def uploaddoc():
    if request.method=='POST':
        file=request.files['file']
        if file and allowed_filedoc(file.filename):#checking for docs
            filename=secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER']+filename)
            filedata=Files.query.order_by(Files.id)
            new_file=Files(fName=filename,type='Document')
            db.session.add(new_file)
            db.session.commit()
            return render_template('view.html',filedata=filedata,new_file=new_file)
        else:
            flash('Upload a Document')
            return render_template('upload.html')
    return render_template('upload.html')
#for deleting the record by name
@upload.route("/delete/<fName>",methods=['GET',"POST"])
def delete(fName):
    file_to_delete=Files.query.get_or_404(fName)
    fName=None
    type=None
    #deleting the record
    db.session.delete(file_to_delete)
    db.session.commit()
    filedata=Files.query.order_by(Files.id)
    flash('deleted')
    return render_template("view.html",filedata=filedata,fName=fName,type=type,new_file=None)
@upload.route('/view',methods=['POST','GET'])
def view():
    filedata=Files.query.order_by(Files.id)
    return render_template('view.html',filedata=filedata)
@upload.route('/download_file')
def download_file():
    path="output.png"
    return send_file(path,as_attachment=True)