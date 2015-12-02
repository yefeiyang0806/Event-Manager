import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/static/uploads'
ALLOWED_EXTENSIONS = set(['txt'])

#
@upload.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('/upload.html')
    elif request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(UPLOAD_FOLDER, filename))
           # return redirect(url_for('uploaded_file', filename = filename))   
            return ("upload successfully!")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@upload.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)