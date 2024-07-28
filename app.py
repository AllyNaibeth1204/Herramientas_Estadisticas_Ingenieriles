from flask import Flask, request, jsonify, render_template, render_template_string
import math
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from statistics import mode, StatisticsError
import random as rnd

app = Flask(__name__)

# Variables globales
data_list = []
Tablas_frecuencia = []
mean_value = 0
mode_value = None
median_value = 0
variance_value = 0
std_dev_value = 0
moment_1 = 0 
moment_2 = 0
moment_3 = 0
moment_4 = 0


#De aqui hacia abajo es el randomizar
#De aqui hacia abajo es el randomizar
#De aqui hacia abajo es el randomizar
#De aqui hacia abajo es el randomizar

@app.route('/generar_numeros', methods=['POST'])
def generar_numeros():
    global data_list, min_num, max_num, total_data
    min_num = int(request.form['Min_place'])
    max_num = int(request.form['Max_place'])
    total_data = int(request.form['num'])

    data_list = [rnd.randint(min_num, max_num) for _ in range(total_data)]

    return render_template('random.html', data_list=data_list)

@app.route('/randomizar', methods=['POST'])
def rand():
    global Tablas_frecuencia, data_list, LSC, intervals, class_mark, mark, ojiva_faa, ojiva_fad, mean_value, mode_value, median_value, variance_value, std_dev_value,skewness_value, kurtosis_value,pearson1_value,pearson2_value 
    

    #moda
    frequency = {}
    for number in data_list:
        frequency[number] = frequency.get(number, 0) + 1
    max_frequency = max(frequency.values())
    mode_candidates = [k for k, v in frequency.items() if v == max_frequency]
    mode_value = mode_candidates[0]  # Selecciona solo la primera moda en caso de múltiples modas
    
    #mediana
    data_list.sort()
    if total_data % 2 == 0:
        median_value = (data_list[total_data // 2 - 1] + data_list[total_data // 2]) / 2
    else:
        median_value = data_list[total_data // 2]

    #Varianza
    variance_value = sum((x - mean_value) ** 2 for x in data_list) / total_data
    #desviación estandar
    std_dev_value = math.sqrt(variance_value)

     # Calcular los coeficientes de asimetría y curtosis
    skewness_numerator = sum((x - mean_value) ** 3 for x in data_list)
    skewness_value = (total_data * skewness_numerator) / ((total_data - 1) * (total_data - 2) * (std_dev_value ** 3))
    
    kurtosis_numerator = sum((x - mean_value) ** 4 for x in data_list)
    kurtosis_value = ((total_data * (total_data + 1) * kurtosis_numerator) / 
                      ((total_data - 1) * (total_data - 2) * (total_data - 3) * (std_dev_value ** 4))) - \
                     (3 * (total_data - 1) ** 2) / ((total_data - 2) * (total_data - 3))

    # Calcular los coeficientes de Pearson
    pearson1_value = (mean_value - mode_value) / std_dev_value
    pearson2_value = 3 * (mean_value - median_value) / std_dev_value

    #inicio codigo Hector
    rng = max(data_list) - min(data_list)
    k = 1 + 3.33 * math.log10(total_data)
    TIC = math.ceil(rng / k)
    intervals = math.ceil(rng / TIC)
    Tablas_frecuencia = [["LIC", "LSC", "f", "Xi", "fr", "faa", "fad", "fra", "frd","M1","M2","M3","M4"]]
    LIC = min(data_list)
    faa = fra = Totf = 0
    class_mark = [LIC - (TIC / 2)]
    mark = [0]
    for rp in range(intervals):
        LSC = LIC + TIC
        num_f = [frc for frc in data_list if LIC <= frc < LSC]
        f = len(num_f)
        Xi = (LIC + LSC) / 2
        class_mark.append(Xi)
        mark.append(f)
        fr = f / total_data
        Totf = Totf + f
        Tablas_frecuencia.append([LIC, LSC, f, Xi, round(fr, 2)])
        LIC = LSC
    class_mark.append(LSC + (TIC / 2))
    mark.append(0)

    #Obtener la media
    for pos in range(len(Tablas_frecuencia) - 1):
        mean_value += Tablas_frecuencia[pos + 1][2] * Tablas_frecuencia[pos + 1][3]
    mean_value = mean_value/total_data

    frd = fad = Totf
    ojiva_faa = [0]
    ojiva_fad = [Totf]
    for rp in range(intervals):
        faa = faa + Tablas_frecuencia[rp + 1][2]
        ojiva_faa.append(faa)
        fad = fad - Tablas_frecuencia[rp + 1][2]
        ojiva_fad.append(fad)
        fra = faa / Totf
        frd = fad / Totf

        #Momentos
        M1 = ((Tablas_frecuencia[rp + 1][3] - mean_value) * Tablas_frecuencia[rp + 1][2])/total_data
        M2 = (((Tablas_frecuencia[rp + 1][3] - mean_value) ** 2) * Tablas_frecuencia[rp + 1][2])/total_data
        M3 = (((Tablas_frecuencia[rp + 1][3] - mean_value) ** 3) * Tablas_frecuencia[rp + 1][2])/total_data
        M4 = (((Tablas_frecuencia[rp + 1][3] - mean_value) ** 4) * Tablas_frecuencia[rp + 1][2])/total_data

        Tablas_frecuencia[rp + 1].append(faa)
        Tablas_frecuencia[rp + 1].append(fad)
        Tablas_frecuencia[rp + 1].append(round(fra, 2))
        Tablas_frecuencia[rp + 1].append(round(frd, 2))

        #Adicion de los momentos
        Tablas_frecuencia[rp + 1].append(M1)
        Tablas_frecuencia[rp + 1].append(M2)
        Tablas_frecuencia[rp + 1].append(M3)
        Tablas_frecuencia[rp + 1].append(M4)

    ojiva_fad.append(0)
    ojiva_faa.append(faa)

    bins_personalizados = np.linspace(min(data_list), LSC, intervals + 1) 

    # Histograma
    plt.figure(figsize=(6, 4))
    plt.hist(data_list, bins=bins_personalizados, edgecolor="black")
    plt.xticks(bins_personalizados)
    plt.title("Histograma")

    hist = io.BytesIO()
    plt.savefig(hist, format='png')
    hist.seek(0)

    hist_graph = base64.b64encode(hist.getvalue()).decode('utf8')

    # Polígono de frecuencia
    plt.figure(figsize=(6, 4))
    xpoints = np.array(class_mark)
    ypoints = np.array(mark)
    plt.xticks(class_mark)
    plt.plot(xpoints, ypoints, marker='.')
    plt.title("Polígono de frecuencia")

    frec = io.BytesIO()
    plt.savefig(frec, format='png')
    frec.seek(0)

    frec_graph = base64.b64encode(frec.getvalue()).decode('utf8')

    # Ojiva ascendente
    plt.figure(figsize=(6, 4))
    xpoints = np.array(class_mark)
    ypoints = np.array(ojiva_faa)
    plt.xticks(class_mark)
    plt.plot(xpoints, ypoints, marker='.')
    plt.title("Ojiva ascendente")

    P_asc = io.BytesIO()
    plt.savefig(P_asc, format='png')
    P_asc.seek(0)

    P_asc_graph = base64.b64encode(P_asc.getvalue()).decode('utf8')

    # Ojiva descendente
    plt.figure(figsize=(6, 4))
    xpoints = np.array(class_mark)
    ypoints = np.array(ojiva_fad)
    plt.xticks(class_mark)
    plt.plot(xpoints, ypoints, marker='.')
    plt.title("Ojiva descendente")

    P_des = io.BytesIO()
    plt.savefig(P_des, format='png')
    P_des.seek(0)

    P_des_graph = base64.b64encode(P_des.getvalue()).decode('utf8')

    html = f'''
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Matriz de Datos</title>
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <script src="{{{{ url_for('static', filename='js/script.js') }}}}" defer></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js" defer></script>
    </head>
    <body>
    
    <div id="contenedor">

        <h2 id="tabla">Tablas de frecuencias</h2>
        <table class="mi-tabla">
            {{% for fila in matriz %}}
            <tr>
                {{% for dato in fila %}}
                <td>{{{{dato}}}}</td>
                {{% endfor %}}
            </tr>
            {{% endfor %}}
        </table>
        
        <div class="resultados">
        <h3 id="rMedia">Rango: {rng}</h3>
        <h3 id="rMedia">TIC: {TIC}</h3>
        <h3 id="rMedia">Media: {round(mean_value, 2)}</h3>
        <h3 id="rModa">Moda: {mode_value}</h3>
        <h3 id="rMediana">Mediana: {median_value}</h3>
        <h3 id="rVarianza">Varianza: {round(variance_value, 2)}</h3>
        </div>

        <div class="result">
        <h3 id="rDesviacionEstandar">Desviación Estándar: {round(std_dev_value, 2)}</h3>
        <h3 id="rFisher">Fisher: {round(skewness_value, 2)}</h3>
        <h3 id="rCurtois">Curtosis: {round(kurtosis_value, 2)}</h3>
        <h3 id="rPearson 1">Pearson 1: {round(pearson1_value, 2)}</h3>
        <h3 id="rPearson 2">Pearson 2: {round(pearson2_value, 2)}</h3>
        </div>
        
        <div class="imagenes">
        <img id="histo" src="data:image/png;base64,{hist_graph}" class="original-size" />
        <img id="poli" src="data:image/png;base64,{frec_graph}" />
        <img id="asc" src="data:image/png;base64,{P_asc_graph}" />
        <img id="des" src="data:image/png;base64,{P_des_graph}" />
        </div>

    </div>
    </body>
    </html>
    '''
    return render_template_string(html, matriz=Tablas_frecuencia)

#De aqui hacia arriba es el randomizar
#De aqui hacia arriba es el randomizar
#De aqui hacia arriba es el randomizar
#De aqui hacia arriba es el randomizar
#De aqui hacia arriba es el randomizar

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/seleccion') 
def seleccion():
    return render_template('seleccion.html')

@app.route('/entrada')
def entrada():
    return render_template('entrada.html')

@app.route('/random')
def random():
    return render_template('random.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    data = request.json
    global Tablas_frecuencia, data_list, LSC, intervals, class_mark, mark, ojiva_faa, ojiva_fad, mean_value, mode_value,median_value, variance_value, std_dev_value,skewness_value, kurtosis_value,pearson1_value,pearson2_value, TIC, rng 

    data_list = [int(d) for d in data] 
    total_data = len(data_list)

    #moda
    frequency = {}
    for number in data_list:
        frequency[number] = frequency.get(number, 0) + 1
    max_frequency = max(frequency.values())
    mode_candidates = [k for k, v in frequency.items() if v == max_frequency]
    mode_value = mode_candidates[0]  # Selecciona solo la primera moda en caso de múltiples modas
    
    #mediana
    data_list.sort()
    if total_data % 2 == 0:
        median_value = (data_list[total_data // 2 - 1] + data_list[total_data // 2]) / 2
    else:
        median_value = data_list[total_data // 2]
    
    #varianza
    variance_value = sum((x - mean_value) ** 2 for x in data_list) / total_data
    #desviación estandar
    std_dev_value = math.sqrt(variance_value)

    # Calcular los coeficientes de asimetría y curtosis
    skewness_numerator = sum((x - mean_value) ** 3 for x in data_list)
    skewness_value = (total_data * skewness_numerator) / ((total_data - 1) * (total_data - 2) * (std_dev_value ** 3))
    
    kurtosis_numerator = sum((x - mean_value) ** 4 for x in data_list)
    kurtosis_value = ((total_data * (total_data + 1) * kurtosis_numerator) / 
                      ((total_data - 1) * (total_data - 2) * (total_data - 3) * (std_dev_value ** 4))) - \
                     (3 * (total_data - 1) ** 2) / ((total_data - 2) * (total_data - 3))

    # Calcular los coeficientes de Pearson
    pearson1_value = (mean_value - mode_value) / std_dev_value
    pearson2_value = 3 * (mean_value - median_value) / std_dev_value
   
    #inicio codigo Hector
    rng = max(data_list) - min(data_list)
    k = 1 + 3.33 * math.log10(total_data)
    TIC = math.ceil(rng / k)
    intervals = math.ceil(rng / TIC)
    Tablas_frecuencia = [["LIC", "LSC", "f", "Xi", "fr", "faa", "fad", "fra", "frd","M1","M2","M3","M4"]]
    LIC = min(data_list)
    faa = fra = Totf = 0
    class_mark = [LIC - (TIC / 2)]
    mark = [0]
    for rp in range(intervals):
        LSC = LIC + TIC
        num_f = [frc for frc in data_list if LIC <= frc < LSC]
        f = len(num_f)
        Xi = (LIC + LSC) / 2
        class_mark.append(Xi)
        mark.append(f)
        fr = f / total_data
        Totf = Totf + f
        Tablas_frecuencia.append([LIC, LSC, f, Xi,round(fr, 2)])
        LIC = LSC
    class_mark.append(LSC + (TIC / 2))
    mark.append(0)

    #Obtener la media
    for pos in range(len(Tablas_frecuencia) - 1):
        mean_value += Tablas_frecuencia[pos + 1][2] * Tablas_frecuencia[pos + 1][3]
    mean_value = mean_value/total_data

    frd = fad = Totf
    ojiva_faa = [0]
    ojiva_fad = [Totf]
    for rp in range(intervals):
        faa = faa + Tablas_frecuencia[rp + 1][2]
        ojiva_faa.append(faa)
        fad = fad - Tablas_frecuencia[rp + 1][2]
        ojiva_fad.append(fad)
        fra = faa / Totf
        frd = fad / Totf

        #Momentos
        M1 = ((Tablas_frecuencia[rp + 1][3] - mean_value) * Tablas_frecuencia[rp + 1][2])/total_data
        M2 = (((Tablas_frecuencia[rp + 1][3] - mean_value) ** 2) * Tablas_frecuencia[rp + 1][2])/total_data
        M3 = (((Tablas_frecuencia[rp + 1][3] - mean_value) ** 3) * Tablas_frecuencia[rp + 1][2])/total_data
        M4 = (((Tablas_frecuencia[rp + 1][3] - mean_value) ** 4) * Tablas_frecuencia[rp + 1][2])/total_data

        Tablas_frecuencia[rp + 1].append(faa)
        Tablas_frecuencia[rp + 1].append(fad)
        Tablas_frecuencia[rp + 1].append(round(fra, 2))
        Tablas_frecuencia[rp + 1].append(round(frd, 2))

        #Adicion de los momentos
        Tablas_frecuencia[rp + 1].append(M1)
        Tablas_frecuencia[rp + 1].append(M2)
        Tablas_frecuencia[rp + 1].append(M3)
        Tablas_frecuencia[rp + 1].append(M4)

    ojiva_fad.append(0)
    ojiva_faa.append(faa)

    
    
    return jsonify({"status": "success", "received_data": data,"mean":round(mean_value, 2),"mode": mode_value})

@app.route('/resultados', methods=['POST'])
def graficas():
    bins_personalizados = np.linspace(min(data_list), LSC, intervals + 1) 

    # Histograma
    plt.figure(figsize=(6, 4))
    plt.hist(data_list, bins=bins_personalizados, edgecolor="black")
    plt.xticks(bins_personalizados)
    plt.title("Histograma")

    hist = io.BytesIO()
    plt.savefig(hist, format='png')
    hist.seek(0)

    hist_graph = base64.b64encode(hist.getvalue()).decode('utf8')

    # Polígono de frecuencia
    plt.figure(figsize=(6, 4))
    xpoints = np.array(class_mark)
    ypoints = np.array(mark)
    plt.xticks(class_mark)
    plt.plot(xpoints, ypoints, marker='.')
    plt.title("Polígono de frecuencia")

    frec = io.BytesIO()
    plt.savefig(frec, format='png')
    frec.seek(0)

    frec_graph = base64.b64encode(frec.getvalue()).decode('utf8')

    # Ojiva ascendente
    plt.figure(figsize=(6, 4))
    xpoints = np.array(class_mark)
    ypoints = np.array(ojiva_faa)
    plt.xticks(class_mark)
    plt.plot(xpoints, ypoints, marker='.')
    plt.title("Ojiva ascendente")

    P_asc = io.BytesIO()
    plt.savefig(P_asc, format='png')
    P_asc.seek(0)

    P_asc_graph = base64.b64encode(P_asc.getvalue()).decode('utf8')

    # Ojiva descendente
    plt.figure(figsize=(6, 4))
    xpoints = np.array(class_mark)
    ypoints = np.array(ojiva_fad)
    plt.xticks(class_mark)
    plt.plot(xpoints, ypoints, marker='.')
    plt.title("Ojiva descendente")

    P_des = io.BytesIO()
    plt.savefig(P_des, format='png')
    P_des.seek(0)

    P_des_graph = base64.b64encode(P_des.getvalue()).decode('utf8')

    html = f'''
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Matriz de Datos</title>
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/style.css') }}}}">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css" rel="stylesheet">
    <script src="{{{{ url_for('static', filename='js/script.js') }}}}" defer></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js" defer></script>
    </head>
    <body>
    
    <div id="contenedor">

        <h2 id="tabla">Tablas de frecuencias</h2>
        <table class="mi-tabla">
            {{% for fila in matriz %}}
            <tr>
                {{% for dato in fila %}}
                <td>{{{{dato}}}}</td>
                {{% endfor %}}
            </tr>
            {{% endfor %}}
        </table>
        
        <div class="resultados">
        <h3 id="rMedia">Rango: {rng}</h3>
        <h3 id="rMedia">TIC: {TIC}</h3>
        <h3 id="rMedia">Media: {round(mean_value, 2)}</h3>
        <h3 id="rModa">Moda: {mode_value}</h3>
        <h3 id="rMediana">Mediana: {median_value}</h3>
        <h3 id="rVarianza">Varianza: {round(variance_value, 2)}</h3>
        </div>

        <div class="result">
        <h3 id="rDesviacionEstandar">Desviación Estándar: {round(std_dev_value, 2)}</h3>
        <h3 id="rFisher">Fisher: {round(skewness_value, 2)}</h3>
        <h3 id="rCurtois">Curtosis: {round(kurtosis_value, 2)}</h3>
        <h3 id="rPearson 1">Pearson 1: {round(pearson1_value, 2)}</h3>
        <h3 id="rPearson 2">Pearson 2: {round(pearson2_value, 2)}</h3>
        </div>
        
        <div class="imagenes">
        <img id="histo" src="data:image/png;base64,{hist_graph}" class="original-size" />
        <img id="poli" src="data:image/png;base64,{frec_graph}" />
        <img id="asc" src="data:image/png;base64,{P_asc_graph}" />
        <img id="des" src="data:image/png;base64,{P_des_graph}" />
        </div>

    </div>
    </body>
    </html>
    '''
    return render_template_string(html, matriz=Tablas_frecuencia)

if __name__ == '__main__':
    app.run(debug=True)
