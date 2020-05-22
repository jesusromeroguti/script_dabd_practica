#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Script que genera les taules de la practica final de dabd i les omple amb milers de dades.

import psycopg2
import random
from random import randint
import datetime
from faker import Faker
#fake = Faker('es_ES')
fake = Faker('es_CA')
faker = Faker('es_ES')

# Poner 10000 de momento lo pruebo con 1000
num_tuples = 1000
num_taules = 13
num_directors = num_repartiment = 500
codis = random.sample(range(10000000), num_taules*num_tuples)
sexes = ["H", "M"]
generes = ["Acció", "Aventures", "Ciencia-Ficcio", "Fantasia",
            "Comedia", "Drama", "Terror", "Thriller", "Western",
            "Historic", "Policiac", "Post-apocaliptic", "Bel·lic",
            "Biografic", "Infantil", "Animacio", "Arts Marcials", "Musical" ]

tarifas = ["HD", "4K"]
# tarifas["HD"] = [2, "HD", 5]
# tarifas["4K"] = [4, "4K", 7]
#acc_id  = random.sample(range(10000000), 10000000)

# print(co)

index = 0

def crear_persona(cur):
    # print('Creant la taula persona. % persones seran introduides.' % num_tuples)
    print('Creant la taula persona. {0} persones seran introduides.'.format(num_tuples))
    cur.execute("DROP TABLE IF EXISTS persona")
    cur.execute("""CREATE TABLE persona(codi bigint NOT NULL PRIMARY KEY,
        nom varchar(50) NOT NULL, data_naixement date,
        sexe char, nacionalitat varchar(100))""")

    for i in range(num_tuples):
        print(i+1, end = '\r')
        codi = codis[i]
        nom = fake.first_name() + ' ' + fake.last_name() + ' ' + fake.last_name()
        data_naixement = faker.date()
        sexe = "H"
        nacionalitat = faker.country()
        while nacionalitat == "Côte d'Ivoire":
            nacionalitat = faker.country()
        try:
            cur.execute("INSERT INTO persona VALUES ('%s', '%s', '%s', '%s', '%s')" % (codi, nom, data_naixement, sexe, nacionalitat))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s, %s, %s, %s). Informacio: %s" % (codi, nom, data_naixement, sexe, nacionalitat, e))
        conn.commit()

def crear_director(cur):
    print('Creant la taula director. {0} directors seran introduides.'.format(num_directors))
    cur.execute("DROP TABLE IF EXISTS director")
    cur.execute("""CREATE TABLE director(codi_per bigint NOT NULL REFERENCES persona ON UPDATE CASCADE,
        num_films_dirigits int NOT NULL, PRIMARY KEY(codi_per))""")
    # Obtenim tots els codis de la taula persona
    cur.execute("SELECT codi FROM persona")
    c_per = cur.fetchall()
    for i in range(num_directors):
        print(i+1, end = '\r')
        # Puede que no se exactamente asi y falte algo
        codi_per = c_per[i][0]
        num_films_dirigits = random.randint(1, 50)
        try:
            cur.execute("INSERT INTO director VALUES ('%s', '%s')" % (codi_per, num_films_dirigits))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s). Informacio: %s" % (codi_per, num_films_dirigits, e))
        conn.commit()
        index = i

def crear_repartiment(cur):
    print('Creant la taula repartiment. {0} repartiments seran introduits.'.format(num_repartiment))
    cur.execute("DROP TABLE IF EXISTS repartiment")
    cur.execute("""CREATE TABLE repartiment(codi_per bigint NOT NULL REFERENCES persona ON UPDATE CASCADE,
        num_films_participa int NOT NULL, PRIMARY KEY(codi_per))""")

    # Obtenim tots els codis de la taula persona
    cur.execute("SELECT codi FROM persona")
    c_per = cur.fetchall()
    #for i in range(num_persona):
    for i in reversed(range(num_repartiment)):
        print(i+1, end = '\r')
        # Puede que no se exactamente asi y falte algo
        codi_per = c_per[i][0]
        num_films_participa = random.randint(1, 50)
        try:
            cur.execute("INSERT INTO repartiment VALUES ('%s', '%s')" % (codi_per, num_films_participa))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s). Informacio: %s" % (codi_per, num_films_participa, e))
        conn.commit()

def crear_genere(cur):
    print('Creant la taula genere. {0} generes seran introduits.'.format(len(generes)))
    cur.execute("DROP TABLE IF EXISTS genere")
    cur.execute("""CREATE TABLE genere(nom varchar(20) NOT NULL PRIMARY KEY)""")

    for i in range(len(generes)):
        print(i+1, end = '\r')
        nom = generes[i]
        try:
            cur.execute("INSERT INTO genere VALUES ('%s')" % (nom))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s). Informacio: %s" % (nom, e))
        conn.commit()

# MIRAR DE UTILIZAR UN DICCIONARIO
def crear_tarifa(cur):
    print('Creant la taula tarifa. {0} tarifes seran introduides.'.format(len(tarifas)))
    cur.execute("DROP TABLE IF EXISTS tarifa")
    cur.execute("""CREATE TABLE tarifa(nom_tarifa varchar(2) NOT NULL PRIMARY KEY, num_user_simul integer NOT NULL,
        qualitat varchar(25) NOT NULL, preu integer NOT NULL)""")

    for i in range(len(tarifas)):
        print(i+1, end = '\r')
        if tarifas[i] == "HD":
            nom_tarifa = tarifas[i]
            num_user_simul = 2
            qualitat = "High Definition (1080)"
            preu = 5
        else:
            nom_tarifa = "4K"
            num_user_simul = 4
            qualitat = "4xHigh Definition (4098)"
            preu = 7
        try:
            cur.execute("INSERT INTO tarifa VALUES ('%s', '%s', '%s', '%s' )" % (nom_tarifa, num_user_simul, qualitat, preu))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s, %s, %s). Informacio: %s" % (nom_tarifa, num_user_simul, qualitat, preu, e))
        conn.commit()

# Arreglar nombres duplicados
def crear_usuari(cur):
    print('Creant la taula usuari. {0} usuaris seran introduits.'.format(num_tuples))
    cur.execute("DROP TABLE IF EXISTS usuari")
    cur.execute("""CREATE TABLE usuari(nom_usuari varchar(35) NOT NULL PRIMARY KEY, email varchar(50) NOT NULL,
        data_registre date NOT NULL, data_naixement date, descompte_aplicat int, nom_tarifa varchar(2) NOT NULL REFERENCES tarifa ON UPDATE CASCADE)""")

    nom_usuaris = []
    emails = ["@hotmail.com", "@yahoo.com", "@gmail.com", "@outlook.com", "@hotmail.com", "@yahoo.com", "@gmail.es"]
    for i in range(num_tuples):
        nom_usuaris.append(faker.user_name())

    for i in range(num_tuples):
        print(i+1, end = '\r')
        email = nom_usuaris[i] + emails[randint(0,6)]
        nom_usuari = nom_usuaris[i]
        data_registre = faker.date_between(start_date='-2y', end_date='today')
        data_naixement = faker.date()
        descompte_aplicat = randint(0,35)
        nom_tarifa = tarifas[randint(0,1)]
        try:
            cur.execute("INSERT INTO usuari VALUES ('%s', '%s', '%s', '%s', '%s', '%s'  )" % (nom_usuari, email, data_registre, data_naixement, descompte_aplicat, nom_tarifa))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s, %s, %s, %s, %s). Informacio: %s" % (nom_usuari, email, data_registre, data_naixement, descompte_aplicat, nom_tarifa, e))
        conn.commit()
# Establim connexio i cridem a les funcions per crear i omplir les taules
try:
    # conn = psycopg2.connect(user="est_h7793896",
    #                         password="dbh7793896",
    #                         host="ahto.epsevg.upc.edu",
    #                         database="est_h7793896",
    #                         port="5432")
    conn = psycopg2.connect(user="userdabd",
                            password="userdabd",
                            host="localhost",
                            database="dabd",
                            port="5432")
    cur = conn.cursor()
    print("Connexio amb la base de dades establerta.")
    # crear_persona(cur)
    # crear_director(cur)
    # crear_repartiment(cur)
    # crear_genere(cur)
    crear_tarifa(cur)
    print("Cambio de funcion")
    crear_usuari(cur)

except(Exception, psycopg2.Error) as err:
    print("Error durant el proces de connexio amb la base de dades: ", err)

# Revisar i puede que lo quite i lo deje sin finally
finally:
    if conn:
        cur.close()
        conn.close()
        print("Connexio amb la base de dades tancada.")
