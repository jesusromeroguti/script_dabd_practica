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
num_tuples = 500
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
descomptes = [5,10,15,20,25,30]

nom_usuaris = []
# print(co)

peliculas = ["El Señor de los Anilllos", "E.T. El extraterrestre", "Toro salvaje", "Star Wars", "Taxi Driver", "El Padrino",
             "El bueno, el feo y el malo", "La lista de Schindler", "Blade Runner", "Seven", "Atrápame si puedes", "Drive",
             "Reservoir Dogs", "El club de la lucha", "Kill Bill. Volumen 1",  "El señor de la guerra", "Skyfall", "Deadpool",
             "La vida de Brian", "Spider-Man", "Django desencadenado", "El resplandor", "Sin City", "Pulp Fiction", "Eduardo Manostijeras"
             "Alien, el octavo pasajero", "Guardianes de la galaxia", "La la land", "Grease", "Ed Wood", "La naranja mecánica", "La isla minima",
             "X-men orifgenes: Lobezno", "Forrest Gump", "2001: Una odisea del espacio", "Sherlock Holmes", "Terminator", "Golden Eye",
             "Malditos Bastardos", "Erase una vez en hollywood", "Charlie y la fabrica de chocolate", "Trainspotting", "Espartaco",
             "Rambo", "Rocky Balboa", "Arma Letal", "La jungla de cristal", "El utlimo mohicano", "Al filo del mañana", "Fast and Furious",
             "El protector", "Venganza", "Mision imposible", "Star Trek", "Los vengadores", "Los vengadores: Endgame", "Iron Man", "Thor Ragnarok",
             "Doctor Strange", "Jurassic Park", "Jurassic World", "Kingsman: Servicio secreto", "Ready Player One", "Capitan America", "Wonderwoman",
             "Logan", "Mad Max", "Ip man", "Jhon Wick", "Avatar", "Casablanc", "Doctor Zhivago", "Desafio Total", "El caballero oscuro",
             "Los juegos del hambre", "El coloso en llamas", "Indian Jones", "Origen", "Creed", "Interestellar", "Scarface", "Gladiator",
             "Buscando a nemo", "Dumbo", "La sirenita", "Matrix", "Aladin", "El libro de la selva", "Los pitufos", "El Rey Leon",
             "Mulan", "Hercules", "La Cenicienta", "Blancanieves"]
series = ["Juego de tronos", "La que se avecina", "La casa de papel", "Stranger Things", "Black Mirror", "Pokemon", "Los simposon", "Breaking Bad",
          "Padre de Familina", "Futurama", "Vikings", "Peaky Blinders", "Locke and Key", "Chernobyl", "Medico de guardia", "Los Serrano",
          "Fisica o Quimica", "Outlander", "Los Soprano", "The Good Doctor", "Anatomia de Grey", "Dragon Ball", "Inuyasha", "Detective Conan",
          "Arale", "Ranma", "Prison Break", "Modern Family", "Pequeñas mentirosas", "Mentes Criminales", "Los 100", "Suits", "House of Cards",
          "Mad Men", "Lucifer", "BlackList", "The Wire", "Rick y Morty", "Daredevil", "Doctor Who", "Sex Education", "Homeland", "Ray Donovan",
          "Shameless", "Orange is the new black", "Big bang theory", "Glee", "House", "Bones", "One Piece", "Better Call Saul", "The Boys"]
documentals = ["The Last Dance", "Food, Inc", "Taxi al lado oscuro", "Cosmos", "El gafe", "Inside Job", "No direction home", "Geroge Harrison",
               "Una tragedia americana", "Muerte en Leon", "Apolo 11", "SpaceX: Hacia marte", "Citizen Four", "Super Size Me", "Una verdad incómoda",
               "El viaje del emperador", "Océanos", "La pesadilla de Darwin", "Senna", "El impostor", "Samsara", "Capitalismo", "Amy", "Influencers"]

cataleg = ["El Señor de los Anilllos", "E.T. El extraterrestre", "Toro salvaje", "Star Wars", "Taxi Driver", "El Padrino",
             "El bueno, el feo y el malo", "La lista de Schindler", "Blade Runner", "Seven", "Atrápame si puedes", "Drive",
             "Reservoir Dogs", "El club de la lucha", "Kill Bill. Volumen 1",  "El señor de la guerra", "Skyfall", "Deadpool",
             "La vida de Brian", "Spider-Man", "Django desencadenado", "El resplandor", "Sin City", "Pulp Fiction", "Eduardo Manostijeras"
             "Alien, el octavo pasajero", "Guardianes de la galaxia", "La la land", "Grease", "Ed Wood", "La naranja mecánica", "La isla minima",
             "X-men orifgenes: Lobezno", "Forrest Gump", "2001: Una odisea del espacio", "Sherlock Holmes", "Terminator", "Golden Eye",
             "Malditos Bastardos", "Erase una vez en hollywood", "Charlie y la fabrica de chocolate", "Trainspotting", "Espartaco",
             "Rambo", "Rocky Balboa", "Arma Letal", "La jungla de cristal", "El utlimo mohicano", "Al filo del mañana", "Fast and Furious",
             "El protector", "Venganza", "Mision imposible", "Star Trek", "Los vengadores", "Los vengadores: Endgame", "Iron Man", "Thor Ragnarok",
             "Doctor Strange", "Jurassic Park", "Jurassic World", "Kingsman: Servicio secreto", "Ready Player One", "Capitan America", "Wonderwoman",
             "Logan", "Mad Max", "Ip man", "Jhon Wick", "Avatar", "Casablanc", "Doctor Zhivago", "Desafio Total", "El caballero oscuro",
             "Los juegos del hambre", "El coloso en llamas", "Indian Jones", "Origen", "Creed", "Interestellar", "Scarface", "Gladiator",
             "Buscando a nemo", "Dumbo", "La sirenita", "Matrix", "Aladin", "El libro de la selva", "Los pitufos", "El Rey Leon",
             "Mulan", "Hercules", "La Cenicienta", "Blancanieves", "Juego de tronos", "La que se avecina", "La casa de papel", "Stranger Things",
             "Black Mirror", "Pokemon", "Los simposon", "Breaking Bad",
             "Padre de Familina", "Futurama", "Vikings", "Peaky Blinders", "Locke and Key", "Chernobyl", "Medico de guardia", "Los Serrano",
             "Fisica o Quimica", "Outlander", "Los Soprano", "The Good Doctor", "Anatomia de Grey", "Dragon Ball", "Inuyasha", "Detective Conan",
             "Arale", "Ranma", "Prison Break", "Modern Family", "Pequeñas mentirosas", "Mentes Criminales", "Los 100", "Suits", "House of Cards",
             "Mad Men", "Lucifer", "BlackList", "The Wire", "Rick y Morty", "Daredevil", "Doctor Who", "Sex Education", "Homeland", "Ray Donovan",
             "Shameless", "Orange is the new black", "Big bang theory", "Glee", "House", "Bones", "One Piece", "Better Call Saul", "The Boys",
             "The Last Dance", "Food, Inc", "Taxi al lado oscuro", "Cosmos", "El gafe", "Inside Job", "No direction home", "Geroge Harrison",
             "Una tragedia americana", "Muerte en Leon", "Apolo 11", "SpaceX: Hacia marte", "Citizen Four", "Super Size Me", "Una verdad incómoda",
             "El viaje del emperador", "Océanos", "La pesadilla de Darwin", "Senna", "El impostor", "Samsara", "Capitalismo", "Amy", "Influencers"]


size = len(peliculas) + len(series) + len(documentals)

index = 0
index_codi = 0

def existeix(username):
    b = False
    for i in range(len(nom_usuaris)):
        if username == nom_usuaris[i]:
            b = True
    return b

def crear_persona(cur):
    print('Creant la taula persona. {0} persones seran introduides.'.format(num_tuples))
    cur.execute("DROP TABLE IF EXISTS persona")
    cur.execute("""CREATE TABLE persona(codi bigint NOT NULL PRIMARY KEY,
        nom varchar(50) NOT NULL, data_naixement date,
        sexe char, nacionalitat varchar(100))""")

    for i in range(num_tuples):
        # Repasat index_codi
        index_codi = i
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

# Mejorar nombres duplicados
def crear_usuari(cur):
    print('Creant la taula usuari. {0} usuaris seran introduits.'.format(num_tuples))
    cur.execute("DROP TABLE IF EXISTS usuari")
    cur.execute("""CREATE TABLE usuari(nom_usuari varchar(35) NOT NULL PRIMARY KEY, email varchar(50) NOT NULL,
        data_registre date NOT NULL, data_naixement date, descompte_aplicat int, nom_tarifa varchar(2) NOT NULL REFERENCES tarifa ON UPDATE CASCADE)""")

    emails = ["@hotmail.com", "@yahoo.com", "@gmail.com", "@outlook.com", "@hotmail.com", "@yahoo.com", "@gmail.es"]
    # Mejorar la creacion de usernames random!!
    for i in range(num_tuples):
        # print(i)
        nom = faker.user_name()
        # print(nom)
        if not existeix(nom):
            nom_usuaris.append(nom)
            # print("Lo meto")
        else:
            nom_usuaris.append(faker.user_name())

    for i in range(num_tuples):
        print(i+1, end = '\r')
        email = nom_usuaris[i] + emails[randint(0,6)]
        nom_usuari = nom_usuaris[i]
        data_registre = faker.date_between(start_date='-2y', end_date='today')
        data_naixement = faker.date()
        descompte_aplicat = descomptes[randint(0,5)]
        nom_tarifa = tarifas[randint(0,1)]
        try:
            cur.execute("INSERT INTO usuari VALUES ('%s', '%s', '%s', '%s', '%s', '%s'  )" % (nom_usuari, email, data_registre, data_naixement, descompte_aplicat, nom_tarifa))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s, %s, %s, %s, %s). Informacio: %s" % (nom_usuari, email, data_registre, data_naixement, descompte_aplicat, nom_tarifa, e))
        conn.commit()

def crear_cataleg(cur):
    print('Creant la taula cataleg. {0} elements seran introduits a cataleg.'.format(len(cataleg)))
    cur.execute("DROP TABLE IF EXISTS cataleg")
    cur.execute("""CREATE TABLE cataleg(codi bigint NOT NULL PRIMARY KEY, titol varchar(50),
        data_estrena date, data_afegit date, qualificacio_edat int, num_vist_total int, num_ranking int)""")

    # print(index_codi)
    for i in range(len(cataleg)):
        print(i+1, end = '\r')
        codi = codis[num_tuples+i]
        titol = cataleg[i]
        data_estrena = faker.date()
        data_afegit = faker.date_between(start_date='-2y', end_date='today')
        qualificacio_edat = randint(0,18)
        num_vist_total = randint(0,100)
        num_ranking = randint(0,len(cataleg))
        try:
            cur.execute("INSERT INTO cataleg VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s')" % (codi, titol, data_estrena, data_afegit, qualificacio_edat, num_vist_total, num_ranking))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s, %s, %s, %s, %s, %s). Informacio: %s" % (codi, titol, data_estrena, data_afegit, qualificacio_edat, num_vist_total, num_ranking, e))
        conn.commit()

def crear_serie(cur):
    print('Creant la taula serie. {0} series seran introduides a serie.'.format(len(series)))
    cur.execute("DROP TABLE IF EXISTS serie")
    cur.execute("""CREATE TABLE serie(codi_ser bigint NOT NULL REFERENCES cataleg ON UPDATE CASCADE, num_temp int, num_ep int, PRIMARY KEY(codi_ser))""")

    cur.execute("SELECT codi FROM cataleg")
    c_cat = cur.fetchall()
    for i in range(len(series)):
        codi_ser = c_cat[i][0]
        num_temp = randint(0,15)
        num_ep = randint(0,150)
        try:
            cur.execute("INSERT INTO serie VALUES ('%s', '%s', '%s')" % (codi_ser, num_temp, num_ep))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s, %s). Informacio: %s" % (codi_ser, num_temp, num_ep, e))
        conn.commit()

def crear_pelicula(cur):
    print('Creant la taula pelicula. {0} pelicules seran introduides a pelicula.'.format(len(peliculas)))
    cur.execute("DROP TABLE IF EXISTS pelicula")
    cur.execute("""CREATE TABLE pelicula(codi_pel bigint NOT NULL REFERENCES cataleg ON UPDATE CASCADE, PRIMARY KEY(codi_pel))""")

    # cur.execute("SELECT codi FROM cataleg")
    # c_cat = cur.fetchall()
    # for i in range(len(peliculas)):
    #     codi_pel = c_cat[len(series) + len(documentals) + i][0]
    #     cur.execute("SELECT * FROM serie where codi_ser = '%s'" % (codi_pel))
    #     while bool(cur.fetchone()):
    #         cur.execute("SELECT codi FROM cataleg ORDER BY RANDOM() LIMIT 1")
    #         codi_pel = cur.fetchone()[0]
    #         cur.execute("SELECT * FROM serie WHERE codi_ser='%s'" % (codi_pel))
    #     try:
    #         cur.execute("INSERT INTO cataleg VALUES ('%s')" % (codi_pel))
    #     except psycopg2.IntegrityError as e:
    #         conn.rollback()
    #         print("Error insertant (%s). Informacio: %s" % (codi_pel, e))
    #     conn.commit()

    for i in range(len(peliculas)):
        print(i+1, end = '\r')
        cur.execute("SELECT codi FROM cataleg ORDER BY RANDOM() LIMIT 1")
        codi_cat = cur.fetchone()[0]
        cur.execute("SELECT * from serie where codi_ser = '%s' " % (codi_cat))
        cat1 = bool(cur.fetchone())
        cur.execute("SELECT * from documental where codi_doc = '%s' " % (codi_cat))
        cat2 = bool(cur.fetchone())
        while cat1 or cat2:
            cur.execute("SELECT codi FROM cataleg ORDER BY RANDOM() LIMIT 1")
            codi_cat = cur.fetchone()[0]
            cur.execute("SELECT * from serie where codi_ser = '%s' " % (codi_cat))
            cat1 = bool(cur.fetchone())
            cur.execute("SELECT * from documental where codi_doc = '%s' " % (codi_cat))
            cat2 = bool(cur.fetchone())
        try:
            cur.execute("INSERT INTO pelicula VALUES ('%s')" % (codi_cat))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s). Informacio: %s" % (codi_cat, e))
        conn.commit()


def crear_documental(cur):
    print('Creant la taula documental. {0} series seran introduides a documental.'.format(len(documentals)))
    cur.execute("DROP TABLE IF EXISTS documental")
    cur.execute("""CREATE TABLE documental(codi_doc bigint NOT NULL REFERENCES cataleg ON UPDATE CASCADE, num_temp int, num_ep int, PRIMARY KEY(codi_doc))""")

    cur.execute("SELECT codi FROM cataleg")
    c_cat = cur.fetchall()
    for i in range(len(documentals)):
        codi_doc = c_cat[len(series)+i][0]
        num_temp = randint(0,15)
        num_ep = randint(0,150)
        try:
            cur.execute("INSERT INTO documental VALUES ('%s', '%s', '%s')" % (codi_doc, num_temp, num_ep))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s, %s). Informacio: %s" % (codi_doc, num_temp, num_ep, e))
        conn.commit()

def crear_forma(cur):
    print('Creant la taula forma. {0} elements seran introduits a forma.'.format(200))
    cur.execute("DROP TABLE IF EXISTS forma")
    cur.execute("""CREATE TABLE forma(codi_cat bigint NOT NULL REFERENCES cataleg ON UPDATE CASCADE, codi_per bigint NOT NULL REFERENCES persona ON UPDATE CASCADE, PRIMARY KEY(codi_cat, codi_per))""")

    for i in range(200):
        print(i+1, end = '\r')
        cur.execute("SELECT codi FROM cataleg ORDER BY RANDOM() LIMIT 1")
        codi_cat = cur.fetchone()[0]
        cur.execute("SELECT codi FROM persona ORDER BY RANDOM() LIMIT 1")
        codi_per = cur.fetchone()[0]
        cur.execute("SELECT * from forma where codi_cat = '%s' AND codi_per = '%s'" % (codi_cat, codi_per))
        while bool(cur.fetchone()):
            cur.execute("SELECT codi FROM cataleg ORDER BY RANDOM() LIMIT 1")
            codi_cat = cur.fetchone()[0]
            cur.execute("SELECT codi FROM persona ORDER BY RANDOM() LIMIT 1")
            codi_per = cur.fetchone()[0]
            cur.execute("SELECT * from forma where codi_cat = '%s' AND codi_per = '%s'" % (codi_cat, codi_per))
        try:
            cur.execute("INSERT INTO forma VALUES ('%s', '%s')" % (codi_cat, codi_per))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s). Informacio: %s" % (codi_cat, codi_per, e))
        conn.commit()

def crear_frequencia(cur):
    print('Creant la taula frequencia. {0} elements seran introduits a frequencia.'.format(num_tuples))
    cur.execute("DROP TABLE IF EXISTS frequencia")
    cur.execute("""CREATE TABLE frequencia(codi_cat bigint NOT NULL REFERENCES cataleg ON UPDATE CASCADE,
        nom_usuari varchar(35) NOT NULL REFERENCES usuari ON UPDATE CASCADE, nombre_cops_vist int, PRIMARY KEY(codi_cat, nom_usuari))""")

    for i in range(num_tuples):
        print(i+1, end = '\r')
        nombre_cops_vist = randint(0,20)
        cur.execute("SELECT codi FROM cataleg ORDER BY RANDOM() LIMIT 1")
        codi_cat = cur.fetchone()[0]
        cur.execute("SELECT nom_usuari FROM usuari ORDER BY RANDOM() LIMIT 1")
        nom_usuari = cur.fetchone()[0]
        cur.execute("SELECT * from frequencia where codi_cat = '%s' AND nom_usuari = '%s'" % (codi_cat, nom_usuari))
        while bool(cur.fetchone()):
            cur.execute("SELECT codi FROM cataleg ORDER BY RANDOM() LIMIT 1")
            codi_cat = cur.fetchone()[0]
            cur.execute("SELECT nom_usuari FROM usuari ORDER BY RANDOM() LIMIT 1")
            codi_per = cur.fetchone()[0]
            cur.execute("SELECT * from frequencia where codi_cat = '%s' AND nom_usuari = '%s'" % (codi_cat, nom_usuari))
        try:
            cur.execute("INSERT INTO frequencia VALUES ('%s', '%s', '%s')" % (codi_cat, nom_usuari, nombre_cops_vist))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s, %s). Informacio: %s" % (codi_cat, nom_usuari, nombre_cops_vist, e))
        conn.commit()

def crear_pertany(cur):
    print('Creant la taula pertany. {0} elements seran introduits a pertany.'.format(200))
    cur.execute("DROP TABLE IF EXISTS pertany")
    cur.execute("""CREATE TABLE pertany(codi_cat bigint NOT NULL REFERENCES cataleg ON UPDATE CASCADE,
        nom_genere varchar(20) NOT NULL REFERENCES genere ON UPDATE CASCADE, PRIMARY KEY(codi_cat, nom_genere))""")

    # Solo las peliculas i las series tienen genero.
    # Tendre que filtrar aquellos codi_cat que sean de series o de peliculas solo para utilizarlos como fk
    for i in range(50):
        cur.execute("SELECT codi FROM cataleg ORDER BY RANDOM() LIMIT 1")
        codi_cat = cur.fetchone()[0]
        cur.execute("SELECT * from documental where codi_doc = '%s'" % (codi_cat))
        while bool(cur.fetchone()):
            cur.execute("SELECT codi FROM cataleg ORDER BY RANDOM() LIMIT 1")
            codi_cat = cur.fetchone()[0]
            cur.execute("SELECT * from documental where codi_doc = '%s'" % (codi_cat))
        cur.execute("SELECT nom FROM genere ORDER BY RANDOM() LIMIT 1")
        nom_genere = cur.fetchone()[0]
        cur.execute("SELECT * from pertany where codi_cat = '%s' AND nom_genere = '%s'" % (codi_cat, nom_genere))
        while bool(cur.fetchone()):
            cur.execute("SELECT codi FROM cataleg ORDER BY RANDOM() LIMIT 1")
            codi_cat = cur.fetchone()[0]
            cur.execute("SELECT * from documental where codi_doc = '%s'" % (codi_cat))
            while bool(cur.fetchone()):
                cur.execute("SELECT codi FROM cataleg ORDER BY RANDOM() LIMIT 1")
                codi_cat = cur.fetchone()[0]
                cur.execute("SELECT * from documental where codi_doc = '%s'" % (codi_cat))
            cur.execute("SELECT nom FROM genere ORDER BY RANDOM() LIMIT 1")
            nom_genere = cur.fetchone()[0]
            cur.execute("SELECT * from pertany where codi_cat = '%s' AND nom_genere = '%s'" % (codi_cat, nom_genere))
        try:
            cur.execute("INSERT INTO pertany VALUES ('%s', '%s')" % (codi_cat, nom_genere))
        except psycopg2.IntegrityError as e:
            conn.rollback()
            print("Error insertant (%s, %s). Informacio: %s" % (codi_cat, nom_genere, e))
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
    crear_persona(cur)
    crear_director(cur)
    crear_repartiment(cur)
    crear_genere(cur)
    crear_tarifa(cur)
    crear_usuari(cur)
    crear_cataleg(cur)
    crear_serie(cur)
    crear_documental(cur)
    crear_pelicula(cur)
    crear_forma(cur)
    crear_frequencia(cur)
    crear_pertany(cur)

except(Exception, psycopg2.Error) as err:
    print("Error durant el proces de connexio amb la base de dades: ", err)

# Revisar i puede que lo quite i lo deje sin finally
finally:
    if conn:
        cur.close()
        conn.close()
        print("Connexio amb la base de dades tancada.")
