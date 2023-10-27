#!/usr/bin/env python3

from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
import subprocess
import shlex
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_files = request.form.getlist('selectedFiles') 
        files = request.files.getlist('file')

        if not files or all(not f.filename for f in files):
            flash('Please upload at least one file.', 'warning')
            return redirect(url_for('index'))

        files_to_process = [file for file in files if file.filename in selected_files]

        filenames = []
        for file in files_to_process:
            filename = os.path.basename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            filenames.append(file.filename)
            try:
                file.save(filepath)
            except:
                flash('There was an error converting the files. Please try again.', 'danger')
        
        filenames_str = ' '.join(filenames)
        cmd = ['dos2unix'] + shlex.split(filenames_str)
        
        try:
            subprocess.run(cmd, check=True, cwd = app.config['UPLOAD_FOLDER'])
            flash('Files successfully converted!', 'success')
        except subprocess.CalledProcessError:
            flash('There was an error converting the files. Please try again.', 'danger')
        
        return redirect(url_for('index'))

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/files/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)