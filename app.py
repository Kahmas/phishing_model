from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static")

@app.route('/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory("static/assets", filename)

# Load model
model = pickle.load(open('random_forest_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [float(x) for x in request.form.values()]
        input_array = np.array([features])
        prediction = model.predict(input_array)
        result = 'Phishing' if prediction[0] == 1 else 'Legitimate'
        return render_template('index.html', prediction_text=f'Hasil : {result}')
    except Exception as e:
        return render_template('index.html', prediction_text=f'Error: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
