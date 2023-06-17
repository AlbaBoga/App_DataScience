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

st.set_page_config(page_title='Observaciones', page_icon='📋', layout='centered')
st.set_option('deprecation.showPyplotGlobalUse', False)

df = pd.read_csv("data/preprocesado.csv")

st.title('Observaciones')

st.subheader('Variables categóricas')
cols = ['experience_level', 'employment_type', 'job_specialization', 'salary_currency', 'employee_residence', 'company_size', "company_location"]
fig = make_subplots(rows=3, cols=3, subplot_titles=cols)
for i, col in enumerate(cols):
    row = i // 3 + 1
    col = i % 3 + 1
    fig.add_trace(go.Histogram(x=df[cols[i]], nbinsx=20, name=f'Distribución de {cols[i]}'), row=row, col=col)
fig.update_yaxes(showticklabels=False, row=3, col=3) #Esto elimina aquellas que están vacías.
fig.update_layout(height=1200, width=1500, title_text="Distribución de Variables", template='plotly_dark', showlegend=False)
fig.update_xaxes(tickangle=90)
st.plotly_chart(fig)

st.markdown("""
Aquí se está representando el conteo de las variables categóricas que se han utilizado para clasificar la variables numéricas del dataset. En la primera podemos ver que el nivel de experiencia SE (experiencia senior) es el más predominante entre los usuarios. En la segunda, el tipo de contrato FT (a tiempo completo) es el más común entre los empleados. En la tercera vemos los diferentes grupos creados para encasillar los trabajos listados dentro de la columna 'job_title'. Se comprueba que dentro del grupo 'Data' que englobaría todos aquellos trabajos especializados en el análisis y manejo de datos, es donde hay el mayor número de trabajos. En las tres siguientes, 'salary_currency', 'employee_residence' y 'company_location' vemos que los más predominante en las tres son los dólares (usd) y la residencia en Estados Unidos. Finalmente, en la gráfica que muestra el tamaño de la empresa, llamada 'company_size', vemos que la más predominante entre los usuarios es la empresa de tamaño mediano (M).
""")

st.subheader('Variables numéricas')
cols = ['work_year', 'salary', 'salary_in_usd', 'remote_ratio']
fig = make_subplots(rows=1, cols=4)
for i, col in enumerate(cols):
    fig.add_trace(go.Histogram(x=df[col], nbinsx=20, name=f'Distribución de {cols[i]}'), row=1, col=i+1)
fig.update_layout(height=400, width=1200, title_text="Distribución de Variables", template='plotly_dark',showlegend=True)
st.plotly_chart(fig)
st.markdown("""
Aquí se comprueba la distribución de las diferentes variables numéricas dentro del DataFrame. En la primera gráfica, la distribución de 'work_year', se observa que la mayoría de datos se han recogido para el año 2023. En la segunda gráfica, la distribución de 'salary', en sus diferentes divisas, vemos que la mayoría de datos están recogidos dentro de un rango, no obstante, hay presencia de valores atípicos muy alejados del rango mayoritario. En la tercera, la distribución de salary_in_usd, vemos que al pasar el salario a dólares, éste queda más repartido en diferentes rangos, ya que el tener diferentes divisas se creaba un rango muy amplio debido a la gran disparidad entre las monedas de cada país. Aún así, también se observan valores atípicos, como se predijo en el análisis global de los datos. Finalmente, en la distribución de 'remote_ratio', se puede ver que los datos están distribuidos en tres grupos, aquellos que desempeñan su trabajo de manera presencial, los que lo desempeñan de mañnera híbrida (presencial + remoto) y los que lo desempeñan de manera completamente remota, siendo la más predominante la presencial y la que menos, la híbrida.
""")

st.subheader('Identificación de Valores Atípicos')
def identificar_outliers(dataframe):
    """
    Esta función crea un gráfico de caja (boxplot) para cada columna numérica 
    en un DataFrame para ayudar a identificar los outliers.
    """
    # Seleccionamos solo las columnas numéricas
    numeric_cols = dataframe.select_dtypes(include='number').columns
    # Calculamos el número de filas y columnas para los subplots
    ncols = 4
    nrows = math.ceil(len(numeric_cols) / ncols)
    # Creamos la figura y los subplots
    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=numeric_cols)
    for i, col in enumerate(numeric_cols):
        # Calculamos las coordenadas del subplot
        row = i // ncols + 1
        col_idx = i % ncols + 1
        # Comprobamos si la columna tiene más de un valor único para evitar errores
        if len(dataframe[col].unique()) > 1:
            fig.add_trace(go.Box(y=dataframe[col], name=col), row=row, col=col_idx)
        else:
            print(f"La columna {col} tiene un solo valor único y no se puede graficar")
    fig.update_layout(title="Gráfico de caja de los outliers", height=600*nrows, showlegend=False, template='plotly_dark')
    st.plotly_chart(fig)

identificar_outliers(df)
st.markdown("""
En la primera gráfica, se puede observar que se ha considerado como valor atípico los datos recogidos dentro del año 2020. Esto se debe a que la cantidad de datos recogidos para ese año es tan pequeña, que no se considera que tengan un peso suficientemente grande como para entrar dentro del rango de datos de interés. En la segunda gráfica se puede comprobar como los salarios quedan recogidos dentro de un rango muy pequeño en comparación con la distribución de valores atípicos. Esto se debe a que la diferencia entre divisas hay imposible recoger todos los salarios dentro de un rango coherente, lo cual alza la necesidad del cambio de divisas a dólares, como se ha hecho dentro del dataset. En la gráfica de 'salary_in_usd' se han conseguido unificar la mayoría de salarios dentro de un rango mayor, no obstante, siguen existiendo valores atípicos muy lejos de ese rango, lo que quiere indicar que puede haber ciertos países en los que para un mismo puesto de trabajo, paguen una cantidad considerablemente mayor en comparación con la mayoría de datos recogidos. Finalmente, para la gráfica de 'remote_ratio' y como se pudo ver en el apartado anterior, todos los datos quedan recogidos dentro del rango establecido, que va del 0 a 100 por ciento.
""")

st.subheader('Salario Medio según el Nivel de Experiencia')
fig = px.strip(df, x="experience_level", y="salary_in_usd", template="plotly_dark", color='job_specialization')

fig.update_layout(
    title='Distribución de salarios por nivel de experiencia',
    xaxis=dict(title='Nivel de experiencia'),
    yaxis=dict(title='Salario en USD')
)
st.plotly_chart(fig)
st.markdown("""
De esta gráfica podemos comprobar que hay una mayor concentración de trabajos dentro de la experiencia SE. Como es de esperar, los salarios dentro del nivel EN (junior) son más bajos que en el nivel MI (medio), que a su véz son ligéramente más bajos que en nivel SE (senior) y que, igualmente, son ligéramente más bajos que en el nivel EX (experto).
""")

fig = make_subplots(rows=2, cols=1)
salario_medio = df.groupby('experience_level')['salary_in_usd'].mean().reset_index()
fig.add_trace(go.Bar(x=salario_medio["experience_level"], y=salario_medio["salary_in_usd"]),row=1,col=1)
fig.add_trace(go.Box(x=df["experience_level"], y=df["salary_in_usd"]),row=2,col=1)
fig.update_layout(height=1200, width=1200, title_text="Salario Promedio por Nivel de Experiencia", template='plotly_dark', showlegend=True)
st.plotly_chart(fig)
st.markdown("""
En la gráfica de arriba se puede observar que el nivel de experiencia EX (nivel experto) es el que tiene el salario medio más alto, como se pudo comprobar en la gráfica anterior, seguido por el nivel SE (senior), luego por el nivel MI (medio) y finalmente por el nivel EN (junior). No obstante, aquí no somos capaces de apreciar la influencia de los valores atípicos dentro de la media. A pesar de los valores atípicos, la media de los salarios está bastante cerca de la mediana, lo cuál indicaría una distribución simétrica entre los salarios, y que éstos valores suponen un majen de error bastante pequeño dentro de los datos dados.
""")

st.subheader('Comparación del Salario por Experiencia y Tipo de Contrato')
by_employment = df.groupby(['job_specialization','experience_level','employment_type'])['salary_in_usd'].mean().reset_index()

fig = px.scatter_3d(by_employment,
                    x='employment_type', y='salary_in_usd', z='experience_level', color='job_specialization', template="plotly_dark")
fig.update_layout(
    title="Salario Medio en función del Tipo de Empleo y Experiencia",
    scene=dict(
        xaxis=dict(title="Tipo de Empleo"),
        yaxis=dict(title="Salario Medio en USD"),
        zaxis=dict(title="Nivel de Experiencia")
    )
)
st.plotly_chart(fig)
st.markdown("""
La finalidad de esta comparativa es descubrir si existen diferencias en el salario medio dentro de la misma experiencia cuando hay diferentes tipo de contrato. Se puede observar para todos los niveles de experiencia que el tipo de contrato FL (autónomo), llega a ganar mucho menos que un empleado contratado FT (a tiempo completo), para el mismo nivel de experiencia, y, en ocasiones, incluso considerablemente menos que un PT (media jornada). Para el tipo de contrato CT (subcontrata), se comprueba que su salario es menor que el empleado FT a excepción de un valor atípico, en el cuál el salario medio es mucho mayor que el resto de salarios de la tabla para la especialidad de Data.
""")

st.subheader('Evolución del Salario Medio con el paso de los Años')

tab1,tab2=st.tabs(['Evolución', 'Predicción'])
with tab1:
    data=df.groupby('work_year')['salary_in_usd'].mean().reset_index()
    fig = px.line(data, x='work_year', y='salary_in_usd', template="plotly_dark")

    fig.update_layout(
        title='Evolución del Salario Medio',
        xaxis=dict(title='Paso del Tiempo'),
        yaxis=dict(title='Salario en USD')
    )
    st.plotly_chart(fig)
    st.markdown("""
    A partir de la gráfica se puede reparar en que, a partir de 2021 hasta el año 2022, hay un crecimiento muy brusco del salario medio. Mientras que para la evolución de 2022 a 2023, el crecimiento deja de tener una pendiente tan pronunciada, lo cuál puede indicar una estabilización del crecimiento salarial.
    """)
with tab2:
    col1,col2 = st.columns(2)
    with col1:
        code=("""
        x_mean=data['work_year'].mean()
    y_mean=data['salary_in_usd'].mean()

    suma_prod_dif=0
    suma_cuad_dif=0

    for v1,v2 in zip(data['work_year'],data['salary_in_usd']):
        suma_prod_dif+=(v1-x_mean)*(v2-y_mean)
        suma_cuad_dif+=(v1-x_mean)**2

    b1=suma_prod_dif/suma_cuad_dif
    b0=y_mean-(x_mean*b1)
    y=b0+(b1*2024)

    print(f'Para 2024, se estima que el salario medio alcance {round(y,2)} dólares')

    pct_salary=((y*100)/data.loc[3,'salary_in_usd'])-100
    pct_salary2=((data.loc[2,'salary_in_usd']*100)/data.loc[3,'salary_in_usd'])-((data.loc[1,'salary_in_usd']*100)/data.loc[3,'salary_in_usd'])

    print(f'Esto supondría un crecimiento del {round(pct_salary,2)}% frente al {round(pct_salary2,2)}% que hubo de 2021 a 2022.')
        """)
        st.code(code,language='python')

        x_mean=data['work_year'].mean()
        y_mean=data['salary_in_usd'].mean()

        suma_prod_dif=0
        suma_cuad_dif=0

        for v1,v2 in zip(data['work_year'],data['salary_in_usd']):
            suma_prod_dif+=(v1-x_mean)*(v2-y_mean)
            suma_cuad_dif+=(v1-x_mean)**2

        b1=suma_prod_dif/suma_cuad_dif
        b0=y_mean-(x_mean*b1)
        y=b0+(b1*2024)

        st.write(f'Para 2024, se estima que el salario medio alcance {round(y,2)} dólares')

        pct_salary=((y*100)/data.loc[3,'salary_in_usd'])-100
        pct_salary2=((data.loc[2,'salary_in_usd']*100)/data.loc[3,'salary_in_usd'])-((data.loc[1,'salary_in_usd']*100)/data.loc[3,'salary_in_usd'])

        st.write(f'Esto supondría un crecimiento del {round(pct_salary,2)}% frente al {round(pct_salary2,2)}% que hubo de 2021 a 2022.')

    with col2:
        fig = go.Figure()
        valor = go.Indicator( mode = "number+delta", value = round(y,2), name = "Evolución Salario Medio",
                            delta = dict( reference = data.loc[3,'salary_in_usd'], increasing_color = "green", decreasing_color = "red" ))
        fig.add_trace(valor)
        fig.update_layout(
            width=400,
            height=300,
            template='plotly_dark'
        )
        st.plotly_chart(fig)
    
    st.markdown("""
    Si se continúa con la misma tendencia de crecimiento, para 2024, se estima que el salario medio alcance 169563.54 dólares. Esto supondría un crecimiento de 2023 a 2024 del 13.77% frente al 26.34% que hubo de 2021 a 2022.
    """)

st.subheader('Proporción de Trabajo Remoto con la Especialidad')
average_remote_ratio_per_job= df.groupby(['job_specialization'])['remote_ratio'].mean().reset_index()

fig = px.bar(average_remote_ratio_per_job,x='remote_ratio', y='job_specialization', template="plotly_dark", color='job_specialization',height=500,orientation='h')

fig.update_layout(
    title='Distribución del Empleo Remoto entre Especializaciones',
    xaxis=dict(title='Ratio Remoto'),
    yaxis=dict(title='Título del empleo')
)
st.plotly_chart(fig)
st.markdown("""
En la gráfica se aprecia que, de media, todos aquellos trabajos relacionados con Business Intelligence tienen un ratio de trabajo remoto del 61% aproximadamente, seguido por aquellos trabajos agrupados en Artifical Intelligence. En las demás especialidades, al ser trabajos más dedicados al tratamiento de datos, donde puede existir el interés de realizar los pertinentes análisis o simulaciones en el sitio de trabajo, ya sea por conveniencia o por temas legales, el ratio se ve disminuido, alcanzando en la especialidad Scientist el 42% aproximadamente.
""")

st.subheader('Usuarios con Trabajo Remoto')
remote_work_by_country=df[df['remote_ratio']>0].groupby('employee_residence')['remote_ratio'].value_counts()
remote_work_by_country_df=pd.DataFrame(remote_work_by_country).reset_index()
remote_work_by_country_df=remote_work_by_country_df.groupby('employee_residence')['count'].sum()
remote_work_count=pd.DataFrame(remote_work_by_country_df).reset_index()
fig = px.bar(remote_work_count.sort_values(by='count', ascending=False),
             x='employee_residence', y='count', template="plotly_dark", color='employee_residence')

fig.update_layout(
    title='Residencia del Usuario vs Trabajo Remoto',
    yaxis=dict(title='Usuarios con Trabajo Remoto'),
    xaxis=dict(title='Título del empleo')
)
st.plotly_chart(fig)
st.markdown("""
En esta gráfica se está mostrando aquellos países donde viven los usuarios que tienen una situación de trabajo híbrido o teletrabajo. Se comprueba que en Estados Unidos es donde hay un mayor número de empleados con trabajo remoto en comparación con los demás.
""")

st.subheader('Evolución del Ratio Remoto con los Años')

tab1,tab2=st.tabs(['Evolución', 'Predicción'])
with tab1:
    data=df.groupby('work_year')['remote_ratio'].mean().reset_index()
    fig = px.line(data, x='work_year', y='remote_ratio', template="plotly_dark")

    fig.update_layout(
        title='Evolución del Trabajo Remoto',
        xaxis=dict(title='Paso del Tiempo'),
        yaxis=dict(title='Proporción trabajo remoto')
    )
    st.plotly_chart(fig)
    st.markdown("""
En la gráfica se observa una considerable caída de la proporción del trabajo remoto en comparación con el crecimiento observado en 2020, lo cual coincide con la terminación del encerramiento por la pandemia en 2021.
    """)
with tab2:
    col1,col2 = st.columns(2)
    with col1:
        code=("""
       x_mean=data['work_year'].mean()
y_mean=data['remote_ratio'].mean()

suma_prod_dif=0
suma_cuad_dif=0

for v1,v2 in zip(data['work_year'],data['remote_ratio']):
    suma_prod_dif+=(v1-x_mean)*(v2-y_mean)
    suma_cuad_dif+=(v1-x_mean)**2

b1=suma_prod_dif/suma_cuad_dif
b0=y_mean-(x_mean*b1)
y=b0+(b1*2024)

print(f'Para 2024, se estima que el ratio de trabajo remoto alcance {round(y,2)}%')

pct_remote=((y*100)/data.loc[3,'remote_ratio'])-100
pct_remote2=((data.loc[2,'remote_ratio']*100)/data.loc[3,'remote_ratio'])-((data.loc[1,'remote_ratio']*100)/data.loc[3,'remote_ratio'])

print(f'Esto supondría un decrecimiento del {round(abs(pct_remote),2)}% frente al {round(abs(pct_remote2),2)}% que hubo de 2021 a 2022.')
        """)
        st.code(code,language='python')

        x_mean=data['work_year'].mean()
        y_mean=data['remote_ratio'].mean()

        suma_prod_dif=0
        suma_cuad_dif=0

        for v1,v2 in zip(data['work_year'],data['remote_ratio']):
            suma_prod_dif+=(v1-x_mean)*(v2-y_mean)
            suma_cuad_dif+=(v1-x_mean)**2

        b1=suma_prod_dif/suma_cuad_dif
        b0=y_mean-(x_mean*b1)
        y=b0+(b1*2024)

        st.write(f'Para 2024, se estima que el ratio de trabajo remoto alcance {round(y,2)}%')

        pct_remote=((y*100)/data.loc[3,'remote_ratio'])-100
        pct_remote2=((data.loc[2,'remote_ratio']*100)/data.loc[3,'remote_ratio'])-((data.loc[1,'remote_ratio']*100)/data.loc[3,'remote_ratio'])

        st.write(f'Esto supondría un decrecimiento del {round(abs(pct_remote),2)}% frente al {round(abs(pct_remote2),2)}% que hubo de 2021 a 2022.')

    with col2:
        fig = go.Figure()
        valor = go.Indicator( mode = "number+delta", value = y, name = "Evolución Trabajo Remoto",
                            delta = dict( reference = data.loc[3,'remote_ratio'], increasing_color = "green", decreasing_color = "red" ))
        fig.add_trace(valor)
        fig.update_layout(
            width=400,
            height=300,
            template='plotly_dark'
        )
        st.plotly_chart(fig)
    
    st.markdown("""
Si se continúa con la misma tendencia, se estima que, para 2024, el ratio de trabajo remoto alcance el 29.2%. Esto supondría un decrecimiento del 14.27% frente al decrecimiento del 39.01% que hubo de 2021 a 2022.
        """)

st.subheader('El Salario Medio en función de los Países de los Usuarios')
avg_salary_by_country = df.groupby('employee_residence')['salary_in_usd'].mean().reset_index()

fig = px.bar(avg_salary_by_country.sort_values(by='salary_in_usd',ascending=False), x='employee_residence', 
             y='salary_in_usd',color='employee_residence', template="plotly_dark",
             title='Salarios medios en USD por país')
fig.update_layout(xaxis_title='País', yaxis_title='Salario')
fig.update_xaxes(tickangle=90)
st.plotly_chart(fig)
st.markdown("""
En la gráfica se puede ver que la media de salario más alta se corresponde con Israel con más de 400,000 USD, mientras que Estados Unidos se encontraría situado en cuarto lugar, con una media de casi 153,000 USD, estando muy por encima de España, cuya media es de aproximadamente 61,000 USD.
""")

st.subheader('Distribución de Roles de Trabajo por Experiencia')
experience_job_ds = df.groupby(['experience_level', 'job_title']).size().reset_index(name='Counts')
fig = px.treemap(experience_job_ds, path=['experience_level', 'job_title'], values='Counts', title='Árbol de Trabajo',template="plotly_dark")
st.plotly_chart(fig)
st.markdown("""
Se puede apreciar que un mayor número de roles caen dentro de la experiencia SE (senior), la cuál tendrá una mayor responsabilidad y permitirá diferentes especializaciones con mayor flexibilidad, debido a los conocimientos adquiridos. Por otro lado, la experiencia EX (experto) tiene un menor número de roles agrupados, ya que serán empleos centrados en la organización, la supervisación y la gerencia, lo cuál hace que se generen menos puestos y que los mismos sean muy específicos.
""")

st.subheader('Salario Medio en función del Tipo de Contrato')
avg_salary_by_employment = df.groupby(['employment_type'])['salary_in_usd'].mean().reset_index()

fig = px.bar(avg_salary_by_employment.sort_values('salary_in_usd', ascending=False),
                    x='employment_type', y='salary_in_usd', color='employment_type', template="plotly_dark")
fig.update_layout(
    title="Salario Medio en función del Tipo de Contrato",
    scene=dict(
        xaxis=dict(title="Tipo de Contrato"),
        yaxis=dict(title="Salario Medio en USD")
    )
)
st.plotly_chart(fig)
st.markdown("""
En la gráfica se observa que en el tipo de contrato FT (a tiempo completo) es donde se alcanza un salario medio mayor, de más de 138,000 USD, lo cuál indica que para ciertos países y ciertos puestos de trabajo, las empresas retribuyen mucho mejor a sus empleados que a las empresas externas que contratan para realizar las tareas. Por otro lado, el salario medio más bajo es para el tipo de contrato PT (media jornada) que no alcanza los 40,000 USD anuales. Así, se puede decir que las empresas favorecen mucho más a los empleados capaces de comprometerse con ellas con salarios mucho más altos.
""")

st.subheader('Top 10 Empleos en Data')
top10_empleos =pd.DataFrame(df['job_title'].value_counts()[:10])

fig = px.bar(top10_empleos.reset_index(), x='count', y='job_title', template="plotly_dark", color='job_title')

fig.update_layout(
    title='Top 10 Empleos en Data',
    yaxis=dict(title='Título del empleo'),
    xaxis=dict(title='Cantidad de empleados')
)
st.plotly_chart(fig)
st.markdown("""
Los tres empleos más comunes entre los usuarios son Data Engineer, Data Scientist y Data Analyst, los demás al ser más específicos dentro de cada rama, son más inusuales y por tanto, menos usuarios trabajan en ellos.
""")

st.subheader('Top 10 empleos más cotizados')
top10_cotizados = df.groupby('job_title')['salary_in_usd'].mean().reset_index()
top10_cotizados = top10_cotizados.sort_values(by='salary_in_usd', ascending=False).head(10)

fig = px.bar(top10_cotizados, x='salary_in_usd', y='job_title', template="plotly_dark", color='job_title')

fig.update_layout(
    title='Top 10 empleos más cotizados',
    xaxis=dict(title='Salario medio (USD)'),
    yaxis=dict(title='Título del empleo')
)
st.plotly_chart(fig)
st.markdown("""
Dentro de los diez empleos con mejor cotización, Data Science Tech Lead se sitúa el primero, un salario medio anual de más de 375,000 USD. En el último puesto se encontraría Applied Scientist, con un salario medio anual de más de 190,000 USD. Si se compara esta gráfica con la anterior, el top 10 de empleos en el sector de Data, se puede comprobar que los empleos aquí mostrados son más especializados, lo cuál puede indicar una mayor necesidad por falta de demanda, que se traduciría en sueldos más elevados.
""")

st.subheader('Top 10 empleos remotos')
top10_remotos = df.groupby('job_title')['remote_ratio'].mean().reset_index()

fig = px.pie(top10_remotos[:10].sort_values(by='remote_ratio', ascending=False),
             names='job_title',values='remote_ratio',color='job_title',template='plotly_dark')

fig.update_layout(
    title='Top 10 empleos remotos')
st.plotly_chart(fig)
st.markdown("""
En la gráfica se comprueba que aquellos empleos con un ratio remoto medio de entre el 70% y el 90% son Applied Data Scientist, Applied Machine Learning Scientist and AI Scientist. En los demás, el ratio remoto medio disminuye considerablemente, indicando que son trabajos donde al menos se necesita una modalidad híbrida para ser realizados eficientemente.
""")

st.subheader('Correlaciones entre Variables')
le = LabelEncoder()
df['experience_level'] = le.fit_transform(df['experience_level'])
df['employment_type'] = le.fit_transform(df['employment_type'])
df['employee_residence'] = le.fit_transform(df['employee_residence'])
df['company_location'] = le.fit_transform(df['company_location'])
df['company_size'] = le.fit_transform(df['company_size'])
df['job_specialization'] = le.fit_transform(df['job_specialization'])

df_corr=df.corr('pearson',numeric_only=True)

fig = go.Figure(data=go.Heatmap(z=df_corr.values, x=df_corr.columns, y=df_corr.columns))
fig.update_layout(
    width=800,
    height=800,
    title='Mapa de calor',
    template='plotly_dark'
)
st.plotly_chart(fig)
st.markdown("""
Tras observar la gráfica de correlaciones, se observan diferentes correlaciones positivas no significativas. La primera se observa entre la experiencia y el salario en dólares. Esta falta de significatividad se puede deber a diferentes puestos de empleo que fueron identificados como valores atípicos, que mostraban salarios muy altos dependiendo del país o la demanda, lo cuál hace que la correlación entre el empleado y el salario disminuya, si para experiencias similares hay diferencias salariales muy dispares. Finalmente, las dos siguientes son entre el salario, la residencia del empleado y la localización de la empresa. La localización de la empresa coincide en su mayoría con la localización del empleado, por lo que ambas parecen tener la misma correlación con el salario. Esto quiere indicar que la localización o residencia tienen un gran impacto en el salario que cobre el empleado, no obstante, la correlación entre las variables puede verse en gran medida detrimentada devido a los elevados sueldos de ciertos empleos, que no encaja con el salario que se percibe en los demás países.

Para el resto de variables, no se observa ninguna correlación, lo cual puede indicar que no exista una relación lineal entre ellas o que se necesitan más datos para establecer una relación más concreta.
""")    


image1 = Image.open('img/dslg.png')
st.sidebar.image(image1)