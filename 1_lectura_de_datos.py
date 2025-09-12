
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



def norm_categorias_preguntas(df) : 
        
        df_cat_est = df.copy()
        
        for col in df_cat_est.columns:
                
                df_cat_est[col] = df_cat_est[col].str.split('-').str[0].str.strip()
        
        return df_cat_est

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
df_encuesta_renom = df_encuesta_renom.drop(columns=['Q2','Q3','Q4','Q5','Q6','Q7'])

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
df_encuesta_estandar = norm_categorias_preguntas(df_encuesta_estandar)
df_encuesta_estandar





#3.Inspeccion preiliminar df_personal

#Tamaño
df_personal.shape
"Se identifica varios codigos referentes a columnas descriptivas, estos se eliminaran"
df_personal.columns 

#Estandarizamos los nombres de las columnas
df_personal.columns = df_personal.columns.str.lower()

#Tipo de datos
"Se observa que la mayoria de las variables numericas hacen referencia a los codigos"
df_personal.dtypes

"Cambiamos el tipo de dato a variables potenciales y eliminamos las variables referengtes a los codigos"
df_personal['docidentidad'] = df_personal['docidentidad'].astype('object')
df_personal['id'] = df_personal['id'].astype('object')
df_personal['jefeinmediato'] = df_personal['jefeinmediato'].astype('object')
df_personal_int = df_personal.select_dtypes(['int','float'])


list_var_codigo = df_personal_int.columns
df_personal = df_personal.drop(columns= list_var_codigo)

#Analisis datos nulos
"Se identifican nulos en variables no potenciales, se procede a eliminarlas"
df_personal.isnull().sum()
df_personal = df_personal.dropna(axis=1)
df_personal.columns

#Analisis duplicados
df_personal.duplicated(subset= 'docidentidad').value_counts() #No hay duplicados





#4.Estandarizacion de formato y analisis columnas
df_personal_estn = df_personal.copy()

#Chequeo estructura de base
df_personal_estn.head(10)
df_personal_estn.columns


#Estandarizamos datos a minusculas

df_personal_estn_min = estandarizacion_min_asc(df_personal_estn)
df_personal_estn_min.dtypes

#Analisis composicion categorias variables 

for column in df_personal_estn_min.columns:
        print('----------------------------------------')
        print('----------------------------------------') 
        print(f'Categorias columna : {column}')        
        print(df_personal_estn_min[column].value_counts())
        print('----------------------------------------')
        print('----------------------------------------')  


#Eliminacion de variables poco representativas
"""En el analisis se observan variables repetitivas en la BD y otras poco representativas que no son de interes"""

df_personal_estn_min = df_personal_estn_min.drop(columns= ['primernombre','nombres','primerapellido','fechatermina','item type',
                                                   'tipodocumento','ciudadexpedicion','nombreestadolaboral','estadocivil',
                                                   'centrocosto','nombrezonaeconomica','empresanombre','empresanombre','nombretipoperiodo',
                                                   'sucursal','nombresucursal','nombreubicaciongeografica','nombreciudadresidencia','nombreunidad'
                                                   'nombrecentrocosto'
                                                   ])

#Reestructuracion de variables potencialmente influtentes en el proyecto

"Agrupar variable nombrelineacosto, nombreunidad, nombrecargo, nombreubicacionfisica"

"Evaluar si son necesarios el tipo de contrato, ele estado civil, jornada, vinculacion"

df_personal_agrp = df_personal_estn_min.copy()

df_personal_agrp['nombrelineacosto'] = df_personal_estn_min['nombrelineacosto'].replace({'mano de obra directa':'mano de obra',
                                                                                         'mano de obra indirecta' : 'mano de obra'})

df_personal_agrp['nombrecargo'] = df_personal_estn_min['nombrecargo'].str.split(' ').str[0]


#Creacion de variables importantes edad(con su respectiva clasificacion) y tiempo en la empresa (con su clasificacion por rango)

fecha_actual = pd.to_datetime("today").normalize()

df_personal_agrp['edad'] = (fecha_actual.year - df_personal_agrp["fechanacimiento"].dt.year) 

df_personal_agrp['edad'].describe()


df_personal_agrp['grupoedad'] = pd.cut(df_personal_agrp['edad'],
                                       bins = [df_personal_agrp['edad'].min(),30,50,df_personal_agrp['edad'].max()],
                                       labels = ['joven','adulto','mayor'])

df_personal_agrp['tiempo_empresa'] = (fecha_actual.year -df_personal_agrp['fechaingreso'].dt.year)
df_personal_agrp['tiempo_empresa'].describe()


