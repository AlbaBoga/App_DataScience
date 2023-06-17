#--------------LIBRERÍAS--------------#
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
from sklearn.preprocessing import LabelEncoder
import streamlit as st
from PIL import Image
#--------------LIBRERÍAS--------------#

st.set_page_config(page_title='Preprocesamiento', page_icon='📋', layout='centered')
st.set_option('deprecation.showPyplotGlobalUse', False)

data = pd.read_csv("data/ds_salaries.csv")

st.title('Limpieza de datos')

code = """
data.isnull().sum()
"""
st.code(code,language='python')
st.write(data.isnull().sum())
st.markdown("""
Primero, se buscan valores nulos. Ninguno es encontrado.
""")

code1="""
duplicates=data.duplicated()
num_duplicates=duplicates.sum()
if duplicates.any():
    print("Se han encontrado duplicados en el DataFrame.")
    print('Hay un total de', num_duplicates, 'valores duplicados en el DataFrame.')
else:
    print("No hay duplicados en el DataFrame.")
"""
st.code(code1, language='python')

duplicates=data.duplicated()
num_duplicates=duplicates.sum()
if duplicates.any():
    st.write("Se han encontrado duplicados en el DataFrame.")
    st.write('Hay un total de', num_duplicates, 'valores duplicados en el DataFrame.')
else:
    st.write("No hay duplicados en el DataFrame.")

st.markdown("""
Seguidamente, se buscan valores duplicados dentro del dataset, de los cuales se encuentran 1171 datos y se procede a eliminarlos.
""")

code2="""
data['job_title'] = data['job_title'].str.lower()
data['job_specialization']=None

job_specializations = {
    'data': 'Data',
    'insight': 'Data',
    'scientist': 'Scientist',
    'engineer': 'Engineer',
    'learning': 'Artificial Intelligence',
    'ml': 'Artificial Intelligence',
    'ai': 'Artificial Intelligence',
    'researcher': 'Artificial Intelligence',
    'technician': 'Artificial Intelligence',
    'bi': 'Business Intelligence',
    'developer': 'Engineer'
}

for i, v in enumerate(data['job_title']):
    if pd.isnull(data.loc[i, 'job_specialization']):
        for value, specialization in job_specializations.items():
            if value in v:
                data.loc[i, 'job_specialization'] = specialization
                break
data['job_title'] = data['job_title'].str.title()
"""
st.code(code2, language='python')

data['job_title'] = data['job_title'].str.lower()
data['job_specialization']=None

job_specializations = {
    'data': 'Data',
    'insight': 'Data',
    'scientist': 'Scientist',
    'engineer': 'Engineer',
    'learning': 'Artificial Intelligence',
    'ml': 'Artificial Intelligence',
    'ai': 'Artificial Intelligence',
    'researcher': 'Artificial Intelligence',
    'technician': 'Artificial Intelligence',
    'bi': 'Business Intelligence',
    'developer': 'Engineer'
}

for i, v in enumerate(data['job_title']):
    if pd.isnull(data.loc[i, 'job_specialization']):
        for value, specialization in job_specializations.items():
            if value in v:
                data.loc[i, 'job_specialization'] = specialization
                break
data['job_title'] = data['job_title'].str.title()

st.markdown("""
En este paso, se observa que en la columna de 'job_title' se tienen 93 valores diferentes para los trabajos que llevan a cabo los sujetos, por ello, se toma la decision de agrupar los diferentes trabajos en 7 grupos de interés, para mejorar la visualización gráfica del usuario. Estos grupos que se han asignado son Data, Scientist, Engineer, Artificial Intelligence y Business Intelligence.
""")

st.write(data.describe())
st.markdown("""
Finalmente, se observa de una manera global los datos que nos van a aportar las variables numéricas. De aquí, podemos ver que el salario medio en dólares se encuentra en casi 140 000 usd, mientras que el salario máximo estaría en 450 000 usd. Debido a la gran diferencia que hay entre el salario máximo y la media y la mediana, esto puede indicar la presencia de valores atípicos dentro de la variable.
""")

image1 = Image.open('img/dslg.png')
st.sidebar.image(image1)