from flask import Flask, redirect, render_template

app = Flask(__name__)
model = load_model()

@app.route('/')
def home():
    return render_template('sample.html', content='yoho')

def load_model():
    pass

if __name__ == '__main__':
    app.run(debug=True)

