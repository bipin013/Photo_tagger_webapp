from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
import webbrowser
import threading

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create the uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    full_name = request.form.get('full_name')
    phone_number = request.form.get('phone_number')
    email = request.form.get('email')

    image = request.files.get('image')
    filename = None

    if image and image.filename != '':
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_name = "".join([c if c.isalnum() else "_" for c in full_name])
        filename = f"{sanitized_name}_{timestamp}.jpg"
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    print("---- Form Submission ----")
    print(f"Name: {full_name}")
    print(f"Phone: {phone_number}")
    print(f"Email: {email}")
    print(f"Saved Image As: {filename if filename else 'No Image Uploaded'}")
    print("-------------------------")

    return redirect(url_for('index'))

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()  # Open browser after 1.25s
    app.run(debug=True)
