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

st.set_page_config(page_title='Primer Vistazo', page_icon='📋', layout='centered')
st.set_option('deprecation.showPyplotGlobalUse', False)

data = pd.read_csv("data/ds_salaries.csv")

st.title('Conjunto de Datos')

st.write(data.head())

st.markdown("""
En el dataset se nos muestra los datos recogidos de los diferentes empleados dentro del sector de Data Science, recogido dentro de la columna 'work_year' entre los años que van de 2020 a 2023. Dentro de los datos se especificará su nivel de experiencia, columna 'experience_level', que se va a dividir en EX (nivel experto), SE (nivel senior), MI (nivel intermedio) y EN (nivel junior). En la columna 'employment_type', se lista el tipo de contrato al que los empleados están sujetos y se divide en FT (a tiempo completo), PT (media jornada), 'FL' (autónomo) y CT (subcontrata). En la columna 'job_title', 'salary', 'salary_currency', 'salary_in_usd' y 'employee_residence' se puede ver el empleo de los sujetos, su salario, la divisa, el salario en dólares y su residencia, respectivamente. En 'remote_ratio', veremos el porcentaje de trabajo remoto que realizan. En 'company_location' vemos el país donde está situada la empresa en la que trabajan. Y, finalmente, en la columna 'company_size' podemos ver el tamaño de empresa en la que trabajan, que se divide en S(una empresa pequeña), M (una empresa mediana) y L (una empresa grande).
""")
st.write(data.shape)
st.write(data.dtypes)
st.markdown("""
Observamos que en el dataset vamos a tener 3755 filas y 11 columnas. En estas últimas tenemos 4 columnas que van a ser variables numéricas, las cuales serían 'work_year', 'salary', 'salary_in_usd' y 'remote_ratio' y el resto van a ser variables categóricas, aportando información a los datos numéricos.
""")

image1 = Image.open('img/dslg.png')
st.sidebar.image(image1)