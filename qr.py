from flask import Flask, render_template, request, send_file, session, redirect, url_for
import segno
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
QR_DIR = os.environ.get('QR_FOLDER')

if not os.path.exists(QR_DIR):
    os.makedirs(QR_DIR)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        data = request.form.get('data')
        color = request.form.get('color', 'black')
        scale = int(request.form.get('scale', 5))

        if data:
            qr = segno.make(data)
            filename = f"{uuid.uuid4().hex}.png"
            filepath = os.path.join(QR_DIR, filename)
            qr.save(filepath, scale=scale, dark=color)

            # Update history
            history = session['history']
            history.append(filename)
            session['history'] = history

            return redirect(url_for('index', file=filename))

    file = request.args.get('file')
    return render_template('index.html', file=file, history=session.get('history', []))

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(QR_DIR, filename), as_attachment=True)
