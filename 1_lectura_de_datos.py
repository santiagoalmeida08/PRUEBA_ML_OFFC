
#Librerias 
import pandas as pd 
import seaborn as sns
import plotly as plt
import os
import unidecode

#Paths
path_datos = r'C:\Users\Usuario\Desktop\PRUEBA_OFFCORSSE\PRUEBA_ML_OFFCORSSE\data\Base Encuesta.xls'
path_repository = r'C:\Users\Usuario\Desktop\PRUEBA_OFFCORSSE\PRUEBA_ML_OFFCORSSE'

#Funciones

def estandarizacion_min_asc(df): 
        
        df_estandar = df.copy()
        
        for col in df_estandar.select_dtypes('object').columns : 
                
                df_estandar[col] =(df[col].astype(str).str.strip().str.lower()
                                          .apply(lambda x: unidecode.unidecode(x)))
                
        return df_estandar


#Lectura de datos 
df_encuesta = pd.read_excel(path_datos, sheet_name= 'Bk', engine= 'xlrd')
df_personal = pd.read_excel(path_datos, sheet_name= 'Data', engine= 'xlrd')


#1.Inspeccion preiliminar df-encuestas

#Tamaño
df_encuesta.shape
df_encuesta.columns

#Tipo de variables
"Las variables de hora,nombre,correo no son de interes, se borra en estandarizacion"
df_encuesta.dtypes
                 
#Analsis nulos
"""Se encuentan 2 variables con el 100% de datos nulos, por lo cual se eliminaran en la limpieza""" 
df_encuesta.isnull().sum()

#Analisis duplicados (id y cedula)
"No se observan id's duplicados en la base de encuestas, sin embargo si tiene duplicados en la encuesta"
df_encuesta.duplicated(subset= 'ID').value_counts()
df_encuesta.duplicated(subset= '¿Cuál es tu número de cédula?').value_counts()
df_encuesta = df_encuesta.drop_duplicates(subset='¿Cuál es tu número de cédula?',keep= 'first')




#2.Estandarizacion df_encuesta (normalizacion de formatos, categorias)

#Reestructuracion de nombres columnas 
"Se reenombran las columnas de forma generica y se genera un diccionario como guia de analisis"
# Crear un diccionario automático
renombres_auto = {col: f"Q{i+1}" for i, col in enumerate(df_encuesta.columns)}
df_diccionario = pd.DataFrame(list(renombres_auto.items()), columns=["PreguntaOriginal", "Alias"])
df_diccionario.to_excel(os.path.join(path_repository,'dic_variables_encuesta.xlsx'))

# Aplicar renombre
df_encuesta = df_encuesta.rename(columns=renombres_auto)
df_encuesta_renom = df_encuesta.copy()

#Borrar columnas innecesarias
df_encuesta_renom = df_encuesta_renom.drop(columns=['Q2','Q3','Q4','Q5','Q6'])

#Transformaos el numero de cedula
df_encuesta_renom['Q1'] = df_encuesta_renom['Q1'].astype('object')
df_encuesta_renom.dtypes

#Estandarizamos los datos a minusculas
df_encuesta_estandar = estandarizacion_min_asc(df_encuesta_renom)
                
#Analizar estructura de preguntas (niveles, composicion)
'Las columnas referentes a preguntas que miden el interes se componen de respuesta_interes - complemento'
for column in df_encuesta_estandar.columns:
        print('----------------------------------------')
        print('----------------------------------------') 
        print(f'Categorias columna : {column}')        
        print(df_encuesta_estandar[column].value_counts())
        print('----------------------------------------')
        print('----------------------------------------')  

#Conservar la respuesta de interes

def norm_categorias_preguntas(df) : 
        
        df_cat_est = df.copy()
        
        for col in df_cat_est.columns:
                
                df_cat_est[col] = df_cat_est[col].str.split('-').str[0].str.strip()
        
        return df_cat_est

df_encuesta_estandar = norm_categorias_preguntas(df_encuesta_estandar)










#Analisis estructura variables categoricas 
df_encuesta_cat = df_encuesta.copy()

#Separamos variables categoricas que son las mas predominantes
df_encuesta_cat = df_encuesta.select_dtypes('object')
df_encuesta_cat.info









df_encuesta_cat.dtypes


for column in df_encuesta_cat.columns:   
    
        #plt.figure(figsize=(10, 6))
        sns.pieplot(data=df_encuesta_cat)
        plt.title(f'Pie {column}')
        plt.xlabel('Attrition')
        plt.ylabel(column)
        plt.show()







