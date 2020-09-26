from flask import Flask, redirect, render_template, request, jsonify
import os
import gensim


def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))


app = Flask(__name__)
saved_model_path = 'savedmodel/maths-ai-model'
model = gensim.models.Word2Vec.load(saved_model_path)

def predict(a, b, c):
    try:
        f = open('searches.txt', 'a')
        prediction = model.wv.most_similar_cosmul(positive=[a, c], negative=[b])[0][0]
        ip = request.remote_addr
        device = request.headers.get('User-Agent')
        f.write(f'{ip}#{device}#{a}#{b}#{c}#{prediction}\n\n')
        f.close()
        return '', prediction
    except:
        return 'Word not in my dictionary, sorry.', ''

# def dberror():
#     return "500: Internal Server Error, try again later.."

@app.route('/', methods=['GET'])
def home():
    return render_template('sample.html', error=None, pred=None, last_updated=dir_last_updated('./static'))

@app.route('/infer/', methods=['POST'])
def pred():
    try:
        global a, b, c
        a = request.form['a'].lower().strip()
        b = request.form['b'].lower().strip()
        c = request.form['c'].lower().strip()
    except:
        return jsonify({'error': 'Invalid action!', 'pred': ''})
    
    if a == '' or b == '' or c == '':
        return jsonify({'error': 'Fill out all the fields!', 'pred': ''})
    
    if len(a.join(b).join(c).split()) > 3:
        return jsonify({'error': 'Only one word per box!', 'pred': ''})

    error, inference = predict(a, b, c)

    if error == '':
        return jsonify({'error': '', 'pred': inference})
    else:
        return jsonify({'error': error, 'pred': ''})


@app.route('/display/', methods=['GET'])
def display():
    pass


if __name__ == '__main__':
    app.run(port=5000)
    # conn = psycopg2.connect(database="testdb", user = "postgres", password = "pass123", host = "127.0.0.1", port = "5432")
    # if not conn:
    #     dberror()

