import os
from flask import Flask, jsonify, json, render_template

from flask_cors import CORS

# Load the Pandas libraries with alias 'pd' 
import pandas as pd 

app = Flask(__name__,static_url_path='/static')

CORS(app)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
 

municipios = [
    {
        'id':21, 
        'sigla':'MA',
        'nome':'Maranhão'
    },
    {
        'id':22, 
        'sigla':'PI',
        'nome':'Piauí'
    },
    {
        'id':23, 
        'sigla':'CE',
        'nome':'Ceará'
    },
    {
        'id':24, 
        'sigla':'RN',
        'nome':'Rio Grande do Norte'
    },
    {
        'id':25, 
        'sigla':'PB',
        'nome':'Paraíba'
    },
     {
        'id':26, 
        'sigla':'PE',
        'nome':'Pernambuco'
    },
     {
        'id':27, 
        'sigla':'AL',
        'nome':'Alagoas'
    },
     {
        'id':28, 
        'sigla':'SE',
        'nome':'Sergipe'
    },
     {
        'id':29, 
        'sigla':'BA',
        'nome':'Bahia'
    }
]

metricas = [
    {'id':'QUANTIDADE_EMPREGOS','nome':'Empregos'},
    {'id':'QUANTIDADE_ESTABELECIMENTOS','nome':'Estabelecimentos'},
    {'id':'QUANTIDADE_VISITAS_ESTIMADA_NACIONAL','nome':'Visitas estimadas nacional'},
    {'id':'QUANTIDADE_VISITAS_ESTIMADA_INTERNACIONAL','nome':'Visitas estimadas internacional'}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/estados/nomes')
def get_estados_nome():
    return jsonify(municipios)


@app.route('/api/metricas/nomes')
def get_metricas_nomes():
    return jsonify(metricas)


@app.route('/api/metricas/dados/<sigla>')
def get_metricas_dados(sigla):
    ano = '2016'
   
    # Read data from file 'filename.csv' 
    # (in the same directory that your python process is based)
    # Control delimiters, rows, column names with read_csv (see later) 
    feats = [
        'QUANTIDADE_EMPREGOS',
        'QUANTIDADE_ESTABELECIMENTOS',
        'QUANTIDADE_VISITAS_ESTIMADA_NACIONAL',
        'QUANTIDADE_VISITAS_ESTIMADA_INTERNACIONAL',
    ]
    cols = ['UF', 'CODIGO_MUNICIPIO'] + feats

    data = pd.read_csv(
        os.path.join(SITE_ROOT, "dataset", "2016-categorizacao.csv"),
        usecols =cols,
        delimiter=';',
        dtype=object
    ) 

    result = data[data['UF'] == sigla.upper()]

    for  feat in feats:
        result[feat] = result[feat].astype(float)
        result[feat+'_MAX'] = result[feat].max(axis=0)
        result[feat+'_MEDIA'] = result[feat].mean(axis=0)
    
    j = result.to_json(orient='records')
    return j

# Carrega municípo por sigla do estado
# Arquivos baixados no github: https://github.com/tbrugz/geodata-br/tree/master/geojson
@app.route('/api/municipios/<sigla>', methods=['GET'])
def get_municipio(sigla):
     
    filename = get_nome_shape_municipio(sigla)
    
    if filename != '':
        json_url = os.path.join(SITE_ROOT, "geojson", filename)
        data = json.load(open(json_url,encoding='utf-8'))
        return data
    
    return {} 

def get_nome_shape_municipio(sigla):
   
    for mun in municipios:
        print(mun['sigla'])
        print(sigla)
        if mun['sigla'].upper() == sigla.upper():
            print('geojs-{}-mun.json'.format(mun['id']))
            return 'geojs-{}-mun.json'.format(mun['id'])

    return ''


@app.route('/api/pontos/', methods=['GET'])
def get_pontos():
    return jsonify({
        'pontos': [
            [-44.3001,-2.52001],
            [-44.309468, -2.509284],
            [-44.307802, -2.557744],
            [-44.251520, -2.526351 ],
            [-46.328358, -7.217394],
            [-45.925941,-1.281689],
            [-45.925941, -10.232576]
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)    