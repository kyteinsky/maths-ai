from flask import Flask, redirect, render_template, request, jsonify
import os
import json
import gensim
from sheets import *
from datetime import datetime
# import bfa
# import requests


app = Flask(__name__)
saved_model_path = 'savedmodel/maths-ai-model'
model = gensim.models.Word2Vec.load(saved_model_path)
referrer, fp, ip, agent = '', '', '', ''
bt = 0


def predict(a, b, c):
    try:
        prediction = model.wv.most_similar_cosmul(positive=[a, c], negative=[b])[0][0]
        now = datetime.now()
        ''' [
            [ip, user-agent, fp, referrer],
            [a, b, c, prediction],
            [date, time],
            [btlvl]
        ]
        '''
        # [country, region, city], timezone, isp, device name, brand
        row = [ip, str(agent), fp, referrer,
                a, b, c, prediction,
                now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"),
                bt]

        sheet.append_row(row)

        return '', prediction

    except:
        return 'Word not in my dictionary, sorry.', ''

def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))

@app.route('/', methods=['GET'])
def home():
    global geoip_data, ip, agent, referrer
    referrer = request.referrer
    ip = request.remote_addr
    request.headers.get('User-Agent')

    return render_template('sample.html', error=None, pred=None, last_updated=dir_last_updated('./static'))


@app.route('/infer/', methods=['POST'])
def pred():
    try:
        global a, b, c
        a = request.form['a'].lower().strip()
        b = request.form['b'].lower().strip()
        c = request.form['c'].lower().strip()
        bt = int(request.form['bt'])*100
    except:
        return jsonify({'error': 'Invalid action!', 'pred': ''})

    if a == '' or b == '' or c == '':
        return jsonify({'error': 'Fill out all the fields!', 'pred': ''})
    
    if len(a.join(b).join(c).split()) > 3:
        return jsonify({'error': 'Only one word per box!', 'pred': ''})

    # gen = predict(a, b, c)
    # data = [i for i in gen]
    # error, inference = data[0][0], data[0][1]

    error, inference = predict(a, b, c)

    if error == '':
        return jsonify({'error': '', 'pred': inference})
    else:
        return jsonify({'error': error, 'pred': ''})


# privacy policy
@app.route('/privacy', methods=['GET'])
def privy():
    return render_template('privacy.html')


if __name__ == '__main__':
    app.run(port=5000)

