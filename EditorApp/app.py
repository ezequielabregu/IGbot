import os
import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['CAPTION_FILE'] = 'posts.csv'

def get_captions():
    captions = {}
    if os.path.exists(app.config['CAPTION_FILE']):
        with open(app.config['CAPTION_FILE'], 'r') as f:
            reader = csv.reader(f)
            captions = {rows[0]: rows[1] for rows in reader}
    return captions

def save_captions(captions):
    os.remove('posts.csv')
    with open(app.config['CAPTION_FILE'], 'w') as f:
        writer = csv.writer(f)
        rows = [[key, value] for key, value in sorted(captions.items())]
        writer.writerows(rows)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        captions = get_captions()
        for key in request.form:
            captions[key] = request.form[key]
        save_captions(captions)
        return redirect(url_for('index'))
    else:
        images = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
        images.sort()
        captions = get_captions()
        
        # Remove entries from captions for images that are no longer in the UPLOAD_FOLDER
        deleted_images = set(captions.keys()) - set(images)
        for image in deleted_images:
            del captions[image]
        
        # Save the updated captions to the CSV file
        save_captions(captions)
        
        return render_template('index.html', images=images, captions=captions)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        for file in files:
            if allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('index'))
    else:
        return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
