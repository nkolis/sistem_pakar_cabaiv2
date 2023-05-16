import numpy as np
import pandas as pd
import os
import platform
from tabulate import tabulate
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

system = platform.system()
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

disease = [
    ['P01', 'Virus Kuning'],
    ['P02', 'Thrips'],
    ['P03', 'Anthraknose'],
    ['P04', 'Aphids'],
    ['P05', 'Layu Fusarium'],
    ['P06', 'Virus Keriting']
]

plant_symptoms = []
plant_diseases = []


####################################### Mode Tampilan Website #######################################


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
        plant_diseases.append(disease[0])
    if np.isin(np.array(['G009', 'G010', 'G014']), p_symptoms).all():
        plant_diseases.append(disease[1])
    if np.isin(np.array(['G002', 'G004', 'G007']), p_symptoms).all():
        plant_diseases.append(disease[2])
    if np.isin(np.array(['G009', 'G013']), p_symptoms).all():
        plant_diseases.append(disease[3])
    if np.isin(np.array(['G001', 'G011', 'G012']), p_symptoms).all():
        plant_diseases.append(disease[4])
    if np.isin(np.array(['G003', 'G005', 'G009', 'G015']), p_symptoms).all():
        plant_diseases.append(disease[5])

    return plant_diseases


@app.route('/clear', methods=['DELETE'])
@cross_origin()
def clear():
    plant_symptoms.clear()
    plant_diseases.clear()
    return 'clear'


def run_server():
    port = 5000
    print(
        f"Silakan akses aplikasi ->: http://localhost:{port} atau http://127.0.0.1:{port}")
    if __name__ == '__main__':
        app.run(debug=False, port=port)

####################################### Mode Tampilan Website #######################################


####################################### Mode Tampilan CLI #######################################


# menu 1


def show_symptoms():
    dataframes = pd.DataFrame(symptoms)
    diseases_table = tabulate(dataframes, headers=['Kode Gejala', 'Nama Gejala'],
                              tablefmt='fancy_grid', numalign='left')
    print(diseases_table)
    main('cli')

# menu 2


def add_symptoms():
    for i in range(len(symptoms)):
        symptomp = input('Masukkan kode gejala yang anda alami: ')
        plant_symptoms.append(symptomp.upper())
        choice = input('Apakah ada gejala lain ? (Y/N) : ')
        if choice == 'N' or choice == 'n':
            break
    main('cli')


# menu 3
def show_pt_symptoms():
    if not plant_symptoms:
        print('Silakan masukkan gejala terlebih dahulu')
        main('cli')
    else:
        plant_symps = []
        for pt_symp in plant_symptoms:
            for symtomp in symptoms:
                if symtomp[0] == pt_symp:
                    plant_symps.append(symtomp)
        plant_symps.sort()
        dataframes = pd.DataFrame(plant_symps)
        diases_table = tabulate(dataframes, headers=['Kode Gejala', 'Nama Gejala'],
                                tablefmt='fancy_grid', numalign='left')

        print(diases_table)
        choice = input('Adakah gejala lain yang belum anda sebutkan? (Y/N) : ')
        if choice == 'Y' or choice == 'y':
            add_symptoms()
        else:
            main('cli')

# menu 4


def diagnose(sy):
    if not sy:
        print('Silakan masukkan gejala terlebih dahulu')
        main('cli')
    else:
        sy.sort()
        sy = np.array(sy)
        if np.isin(np.array(['G005', 'G006', 'G008', 'G009', 'G015']), sy).all():
            plant_diseases.append(disease[0])
        if np.isin(np.array(['G009', 'G010', 'G014']), sy).all():
            plant_diseases.append(disease[1])
        if np.isin(np.array(['G002', 'G004', 'G007']), sy).all():
            plant_diseases.append(disease[2])
        if np.isin(np.array(['G009', 'G013']), sy).all():
            plant_diseases.append(disease[3])
        if np.isin(np.array(['G001', 'G011', 'G012']), sy).all():
            plant_diseases.append(disease[4])
        if np.isin(np.array(['G003', 'G005', 'G009', 'G015']), sy).all():
            plant_diseases.append(disease[5])

        return plant_diseases

# menu utama cli


def run_cli():
    print("="*15+'Sistem Pakar Indetifikasi Penyakit Tanaman Cabai Metode Forward Chaining'+"="*15+'\n')
    print('Silakan pilih menu dibawah : ')
    print('1. Tampilkan daftar gejala')
    print('2. Masukkan gejala tanaman')
    print('3. Tampilkan gejala tanaman')
    print('4. Tampilkan diagnosa')
    print('5. Keluar')
    choice = int(input('Masukkan pilihan : '))
    print('-'*30)
    if choice == 1:
        show_symptoms()
    elif choice == 2:
        add_symptoms()
    elif choice == 3:
        show_pt_symptoms()
    elif choice == 4:
        disease = diagnose(plant_symptoms)
        if disease:
            disease = ', '.join(map(lambda x: x[1], disease))
            print('Tanaman mengalami penyakit : ', disease)
            plant_symptoms.clear()
            plant_diseases.clear()
            main('cli')
        else:
            print('Penyakit tanaman tidak dikenali!')
            show_pt_symptoms()
            main('cli')
    elif choice == 5:
        exit()
    print('\n'+'-'*30)


####################################### Mode Tampilan CLI #######################################


def main(mode):
    if mode == 'web':
        run_server()

    elif mode == 'cli':
        run_cli()


def init():
    print("="*15+'Sistem Pakar Indetifikasi Penyakit Tanaman Cabai Metode Forward Chaining'+"="*15+'\n')
    print("Kelompok: ")
    print("1. Nurkholis Setiawan (2102020032)")
    print("1. Trio Anggoro (2102020031)\n")
    print('Silakan pilih mode tampilan aplikasi : ')
    print('1. Website')
    print('2. Command Line Interface (CLI)')
    mode = int(input('mode : '))
    os.system('cls' if system == 'Windows' else 'clear')
    if mode == 1:
        main('web')
    elif mode == 2:
        main('cli')


init()
