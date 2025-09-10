
#Librerias 
import pandas as pd 
import seaborn as sns
import plotly as plt
import os
import xlrd

#Paths
path_datos = r'C:\Users\Usuario\Desktop\PRUEBA_OFFCORSSE\PRUEBA_ML_OFFCORSSE\data\Base Encuesta.xls'

#Lectura de datos 

df_encuesta = pd.read_excel(path_datos, sheet_name= 'Bk', engine= 'xlrd')
df_personal = pd.read_excel(path_datos, sheet_name= 'Data', engine= 'xlrd')

#Dimension bases de datos
#Tamaño
df_encuesta.shape
df_personal.shape

#Columnas
df_personal.columns
df_encuesta.columns


#Acercamiento a los datos 

#Analisis df_encuestas

#Tipos de datos 
df_encuesta.dtypes 

#Analsis nulos
"""Se encuentan 2 variables con el 100% de datos nulos, por lo cual se eliminaran en la limpieza""" 
df_encuesta.isnull().sum()

#Analisis duplicados
"No se observan id's duplicados en la base de encuestas"
df_encuesta.duplicated(subset= 'ID').value_counts()


#Analisis variables categoricas df_encuestas
df_encuesta_cat = df_encuesta.copy()

#Separamos variables categoricas que son las mas predominantes
df_encuesta_cat = df_encuesta.select_dtypes('object')

df_encuesta_cat.dtypes


for column in df_encuesta_cat.columns:   
    
        #plt.figure(figsize=(10, 6))
        sns.pieplot(data=df_encuesta_cat)
        plt.title(f'Pie {column}')
        plt.xlabel('Attrition')
        plt.ylabel(column)
        plt.show()







