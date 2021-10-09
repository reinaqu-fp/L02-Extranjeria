# -*- coding: utf-8 -*-
'''
Created on 16 jun. 2019
@author: reinaqu
AUTOR: Toñi Reina
REVISOR: Mariano González, Fermín Cruz
ÚLTIMA MODIFICACIÓN: 16/6/2019

En este ejercicio trabajaremos sobre un fichero en formato CSV que tiene información sobre la
población extranjera empadronada en los distintos distritos y barrios de Sevilla
A continuación se muestran las primeras cinco líneas de dicho fichero. Fíjese que la 
primera línea es la cabecera con los datos de las columnas:

"DISTRITO","SECCION","BARRIO","PAIS_NACIMIENTO","HOMBRES","MUJERES"
" 01"," 001","SANTA CATALINA","ALEMANIA",8,6
" 01"," 001","SANTA CATALINA","ARGELIA",0,1
" 01"," 001","SANTA CATALINA","ARGENTINA",2,4
" 01"," 001","SANTA CATALINA","ARMENIA",0,1


Cada línea se identifica con el número de extranjeros de un pais en un distrito, 
sección y barrio, de forma que: el primer valor se corresponde con el código del distrito;
el segundo es el código de la sección dentro del distrito; el tercero el nombre del barrio;
el cuarto el país de procedencia del extranjero; el quinto el número de hombres de ese país 
empadronados en ese barrio; y, el último, el número de mujeres de ese pais empadronados 
en se barrio.
Siga las instrucciones e implemente las funciones que aparecen a continuación.
   
'''

import csv
from collections import namedtuple

DatosExtranjeros = namedtuple('DatosExtranjeros', 'distrito,seccion,barrio,pais,hombres,mujeres')

# Apartado a - 1 punto ----------------------------------------------------------------------
def lee_datos_extranjeros(fichero):
    '''
    Lee un fichero de entrada y devuelve una lista de tuplas . 
    Tenga en cuenta que los tipos numéricos deben ser de tipo int.
    
    Entrada:
    @param fichero: ruta del fichero csv que contiene los datos en codificación utf-8 
    @type fichero: str

    Salida:
    @return: lista de tuplas con la información de los Extranjeros
    @rtype: [DatosExtranjeros(str,str,str,str,int,int)]   
    '''
    registros = []
    with open(fichero, encoding='utf-8') as f:
        lector=csv.reader(f)
        next(lector)
        for distrito, seccion, barrio, pais, hombres,mujeres in lector:
            hombres=int(hombres)
            mujeres=int(mujeres)
            tupla=DatosExtranjeros(distrito,seccion,barrio,pais, hombres, mujeres)
            registros.append(tupla)
    return registros

# Apartado b - 0,5 puntos ----------------------------------------------------------------------
def numero_nacionalidades_distintas(registros):
    '''
    Devuelve el número de nacionalidades distintas presentes en los registros dados como parámetro. 
    Entrada:
    @param registros: lista de tuplas con la información de extranjeros 
    @type registros: [DatosExtranjeros(str,str,str,str,int,int)]
    Salida:
    @return: número de nacionalidades distintas 
    @rtype: int
    '''
    conj = set(registro.pais for registro in registros)
    return len(conj)

# Apartado c - 0,5 puntos ----------------------------------------------------------------------
def secciones_distritos_con_extranjeros_nacionalidades(registros, paises):
    '''Devuelve una lista de tuplas (distrito, seccion) con las secciones y sus distritos
       en las que hay extranjeros del conjunto de paises dados como parámetros.
       La lista de tuplas estará ordenada por distrito. 
    Entrada:
    @param registros: lista de tuplas con la información de extranjeros 
    @type registros: [DatosExtranjeros(str,str,str,str,int,int)]
    @param paises: conjunto con los nombres de los paises buscados 
    @type: set(str)
    Salida:
    @return: una lista de tuplas (distrito, seccion) ordenada por distritos con
       las secciones y sus distrintos en las que hay extrajeros de los paises
       dados como parámetro. La lista de tuplas estará ordenada por distrito 
    @rtype: list((distrito,seccion))
       
    '''
    conj= set((registro.distrito,registro.seccion) for registro in registros if  registro.pais in paises)
    return sorted(conj)


# Apartado d - 1 punto ----------------------------------------------------------------------
def total_extranjeros_por_pais(registros):
    '''
    Devuelve un diccionario en el que las claves son los países y los valores
    el número total de extranjeros (tanto hombres como mujeres) de ese país. 
    Entrada:
    @param registros: lista de tuplas con la información de extranjeros 
    @type registros: [DatosExtranjeros(str,str,str,str,int,int)]
    Salida:
    @return diccionario[pais:total_extranjeros] con el número total de extranjeros por 
       país 
    @rtype {str:int}
    '''
    res={}
    for registro in registros:
        #la clave es el género
        clave=registro.pais
        if clave not in res:
            res[clave]= registro.hombres+registro.mujeres
        else:
            res[clave]+= registro.hombres+registro.mujeres
        
    return res

# Apartado e - 1,5 puntos ----------------------------------------------------------------------
def top_n_extranjeria (registros, n=3):
    '''
    Devuelve una lista de tuplas (pais, numero_extranjeros) con los n paises
    de los que hay más población extranjera en los registros pasados como parámetro. 
    Entrada:
    @param registros: lista de tuplas con la información de extranjeros 
    @type registros: [DatosExtranjeros(str,str,str,str,int,int)]
    @param n: Número de elementos de la lista resultante
    @type n: int
    Salida:
    @return: lista de tuplas (pais, numero_extranjeros) con los n paises de los que hay
       más población extranjera
    @rtype: (str, int)
   '''
    dicc  = total_extranjeros_por_pais(registros)
    res = sorted(dicc.items(), key=lambda x:x[1], reverse=True)
    return res[:n]

# Apartado f - 1,5 puntos ----------------------------------------------------------------------
def barrio_mas_multicultural(registros):
    '''
    Devuelve el nombre del barrio en el que hay un mayor número de nacionalidades distintas 
    Entrada:
    @param registros: lista de tuplas con la información de extranjeros 
    @type registros: [DatosExtranjeros(str,str,str,str,int,int)]
    Salida:
    @return: el nombre del barrio con más nacionalidades distintas 
    @rtype: str
    '''
    dicc = agrupar_por_barrio(registros)
    res = max(dicc, key=lambda x:len(dicc.get(x)))
    return res

'''función auxiliar para barrio_mas_multicultural
'''
def agrupar_por_barrio(registros):
    '''
    Devuelve un diccionario en el que las claves son los barrios y los valores
    el conjunto de paises de los que hay población extranjera en el barrio
    Entrada:
    @param registros: lista de tuplas con la información de extranjeros -> 
    @type registros: [DatosExtranjeros(str,str,str,str,int,int)]
    Salida:
    @return: diccionario[pais:set(pais)] con el conjunto de paises de los que hay población
       extranjera en el barrio dado por la clave
    @rtype: {str:set(str)}
    '''
    res={}
    for registro in registros:
        #la clave es el barrio
        clave=registro.barrio
        if clave not in res:
            res[clave]= set(registro.pais)
        else:
            res[clave].add(registro.pais)    
    return res

# Apartado g - 2 puntos ----------------------------------------------------------------------
def barrio_con_mas_extranjeros(registros, tipo=None):
    '''
    Devuelve el nombre del barrio en el que hay un mayor número de extranjeros, bien
    sea en total (tanto hombres como mujeres) si tipo tiene el valor None, bien
    sea de hombres si tipo es 'Hombres' o mujeres si el tipo es 'Mujeres'
    Entrada:
    @param registros: lista de tuplas con la información de extranjeros
    @type registros: [DatosExtranjeros(str,str,str,str,int,int)]
    @param tipo: Cadena que representa el tipo de extranjeros a contar, puede tomar los valores None,
        'Hombres' o 'Mujeres'
    @type tipo: str
    Salida:
    @return: nombre del barrio con mayor número de extranjeros, bien hombres, bien mujeres,
        bien total (dependiendo del valor del parámetro tipo)
    @rytpe: str
    '''    
    dicc = contar_por_barrio(registros, tipo)
    res = max(dicc.items(), key=lambda x:x[1])
    return res[0]

'''
Función auxiliar para barrio_con_mas_inmigrantes
'''
def contar_por_barrio(registros,tipo=None):
    '''
    Devuelve un diccionario en el que las claves son los barrios y los valores
    el total de extranjeros dde ese barrio (bien sean totales, hombres o mujeres) 
    Entrada:
    @param registros: lista de tuplas con la información de extranjeros 
    @type registros: [DatosExtranjeros(str,str,str,str,int,int)]
    Salida:
    @return diccionario[barrio:total_extranjeros] con el número de extranjeros (bien total,
       bien hombres, bien mujeres
    @rtype: {str:int}
    '''
    res={}
    for registro in registros:
        #la clave es el barrio
        clave=registro.barrio
        if clave not in res:
            res[clave]= 0
        if tipo =='Hombres':    
            res[clave]+=registro.hombres
        elif tipo == 'Mujeres':
            res[clave]+=registro.mujeres
        else:
            res[clave]+=registro.hombres+registro.mujeres
    
    return res
        

# Apartado h - 2 puntos ----------------------------------------------------------------------   
def pais_mas_representado_por_distrito(registros): 
    '''
    Devuelve un diccionario {distrito:pais} en el que las claves son los distritos y los valores
    el país del que hay más extranjeros en el distrito dado por la clave. 
    Entrada:
    @param registros: lista de tuplas con la información de extranjeros 
    @type registros: [DatosExtranjeros(str,str,str,str,int,int)]
    Salida:
    @return: diccionario[distrito:pais] en el que las claves son los distritos y los valores
    el país del que hay más extranjeros en el distrito dado por la clave
    @rtype: {str:str}
    '''

    dicc = agrupar_por_distrito(registros)
    res = dict()
    for (distrito, registros) in dicc.items():
        res[distrito]= top_n_extranjeria(registros, 1)[0][0]
    return res

'''
   Función auxiliar para pais_mas_representado_por_distrito 
'''
def agrupar_por_distrito(registros):
    '''
    Devuelve un diccionario en el que las claves son los distritos y una lista con 
    los registros de ese distrito
    Entrada:
    @param registros: lista de tuplas con la información de extranjeros 
    @type registros: [DatosExtranjeros(str,str,str,str,int,int)]
    Salida:
    @return: diccionario[distrito:list(DatosExtranjeros)] con los distritos y los
       datos de extranjeros agrupados por distrito
    @rtype: {str:list(DatosExtranjeros)}
    '''
    res=dict()
    for registro in registros:
        #la clave es el barrrio
        clave=registro.distrito
        if clave not in res:
            res[clave]= [registro]
        else:
            res[clave].append(registro)    
    return res
