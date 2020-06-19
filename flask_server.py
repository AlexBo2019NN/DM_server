from flask import Flask, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import numpy as np # linear algebra
import pandas as pd
import re
import scipy
import pickle
#import collections
from sklearn.ensemble import GradientBoostingClassifier


app = Flask(__name__)


model = torch.load("./model_DM01.pickle")

UPLOAD_FOLDER = './uploads/unknown'
data_root = './uploads'
test_dir = './uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_prediction():
     


    
    test_predictions = np.concatenate(test_predictions)

    inputs, labels, paths = next(iter(test_dataloader))
    submission_df = pd.DataFrame.from_dict({'id': test_img_paths, 'label': test_predictions})
    submission_df['label'] = submission_df['label'].map(lambda pred: 'porno yes' if pred > 0.5 else 'porno no')
    submission_df['id'] = submission_df['id'].str.replace('uploads/unknown/', '')
    submission_df['id'] = submission_df['id'].str.replace('.jpg', '')    
    return submission_df


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #img = Image.open(io.BytesIO(file))
            res = get_prediction()
            print(res)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <head>
    <title> MILK DETECT SERVER</title>
    </head>
    <body>
    <h1> Milk detect project :</h1>
    <p align=center><img src="\static\stop_p.png"
        alt="Town trip"></p>
    <p> Chek products for milk.
    Server detect milk.</p>    
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print(UPLOAD_FOLDER)
	
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

#from werkzeug import SharedDataMiddleware
#app.add_url_rule('/uploads/<filename>', 'uploaded_file',
#                 build_only=True)
#app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
#    '/uploads':  app.config['UPLOAD_FOLDER']
#})

if __name__ == '__main__':
    app.run(debug=True)