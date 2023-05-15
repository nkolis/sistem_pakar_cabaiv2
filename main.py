from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import numpy as np


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})
app.config['CORS_HEADERS'] = 'Content-Type'

symptoms = [
    ['G001', 'Akar tanaman layu berjamur'],
    ['G002', 'Bercak bulat panjang berwarna coklat kehitaman seperti terbakar Pada Buah'],
    ['G003', 'Buah belang hijau tua dan hijau muda'],
    ['G004', 'Buah busuk kering'],
    ['G005', 'Buah kerdil'],
    ['G006', 'Buah tampak berjerawat'],
    ['G007', 'Busuk Kering Pada Daun dan batang'],
    ['G008', 'Daun menjadi belang hijau muda dan hijau tua'],
    ['G009', 'Daun menjadi keriput dan kerdil'],
    ['G010', 'Daun terdapat bercak bercak kuning hingga kecoklatan'],
    ['G011', 'Tanaman layu hanya saat panas terik'],
    ['G012', 'Tanaman layu mendadak'],
    ['G013', 'Tanaman layu mengakibatkan tanaman mati'],
    ['G014', 'Terdapat garis-garis keperakan pada daun'],
    ['G015', 'Tulang daun berubah menguning']
]

diseases = [
    ['P01', 'Virus Kuning'],
    ['P02', 'Thrips'],
    ['P03', 'Anthraknose'],
    ['P04', 'Aphids'],
    ['P05', 'Layu Fusarium'],
    ['P06', 'Virus Keriting']
]

plant_symptoms = []
plant_diseases = []


@app.route('/')
def index():
    return render_template('index.html', title='Home', message='Welcome to my website!')


@app.route('/symptoms', methods=['GET'])
@cross_origin()
def get_symptoms():
    return symptoms


@app.route('/diagnose', methods=['POST'])
@cross_origin()
def diagnose():
    p_symptoms = np.array(request.form.getlist('symptoms[]'))
    if np.isin(np.array(['G005', 'G006', 'G008', 'G009', 'G015']), p_symptoms).all():
        plant_diseases.append(diseases[0])
    if np.isin(np.array(['G009', 'G010', 'G014']), p_symptoms).all():
        plant_diseases.append(diseases[1])
    if np.isin(np.array(['G002', 'G004', 'G007']), p_symptoms).all():
        plant_diseases.append(diseases[2])
    if np.isin(np.array(['G009', 'G013']), p_symptoms).all():
        plant_diseases.append(diseases[3])
    if np.isin(np.array(['G001', 'G011', 'G012']), p_symptoms).all():
        plant_diseases.append(diseases[4])
    if np.isin(np.array(['G003', 'G005', 'G009', 'G015']), p_symptoms).all():
        plant_diseases.append(diseases[5])

    return plant_diseases


@app.route('/clear', methods=['DELETE'])
@cross_origin()
def clear():
    plant_symptoms.clear()
    plant_diseases.clear()
    return 'clear'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
