from flask import Flask
import random
import psycopg2
from copy import deepcopy
from flask import jsonify, request
import flask_restful
import json

app = Flask(__name__)

def GetData():
    conn = None
    try:
        data=[]
        conn = psycopg2.connect(user="postgres", password="a", database="postgres", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute("select name from \"EtiyaDB\".teams t ")
        row = cur.fetchall()

        for item in row:
            data.append(item[0])
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        data.append(str(error))
    finally:
        if conn is not None:
            conn.close()
    return data

@app.route('/DataKaydet', methods=['POST'])
def DataKaydet():
    data = request.json
    conn = None
    try:
        conn = psycopg2.connect(user="postgres", password="a", database="postgres", host="localhost", port="5432")
        cur = conn.cursor()

        for key, value in data["teams"].items():
            cur.execute('INSERT INTO \"EtiyaDB\".teams (name, power) VALUES (%s, %s)', (key, value))

        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return false
    finally:
        if conn is not None:
            conn.close()

    return "veriler kaydedildi."

@app.route('/Fikstur')
def index():
    sonuc = []
    butunTakimlar = {}
    takimlar = GetData()

    #takimlar = ["Besiktas","Fenerbahce", "Galatasaray", "Konya Spor", "Malatya Spor", "Kayseri Spor", "Goztepe Spor","Gaziantep Spor","Basaksehir Spor", "Denizli Spor"]
    #gucleri = [30, 5, 25, 13, 12, 10, 24, 8, 16, 21]
    random.shuffle(takimlar)
    for i in takimlar:
        butunTakimlar[takimlar.index(i)] = i

    takimsayisi = len(takimlar)
    takimliste = []
    eslesmeler = []

    if takimsayisi % 2 == 0:
        for i in range(0, takimsayisi, 2):
            takimliste.append([i, i + 1])
    eslesmeler.append(deepcopy(takimliste))

    i = 0
    j = 0
    for hs in range(2, takimsayisi):
        while i < (takimsayisi / 2):
            if (i - 1) != -1:
                takimliste[i - 1][1] = takimliste[i][1]
            else:
                j = takimliste[i][1]
            i += 1
        i = int(takimsayisi / 2) - 1
        while i > 0:
            if takimliste[i][0] != 0:
                if (i + 1) != (takimsayisi / 2):
                    takimliste[i + 1][0] = takimliste[i][0]
                else:
                    takimliste[i][1] = takimliste[i][0]
            i -= 1
        takimliste[1][0] = j
        eslesmeler.append(deepcopy(takimliste))

    for hs in range(1, takimsayisi):
        sonuc.append((str(hs) + ". Hafta"))
        sonuc.append("----------")
        for a in range(int(takimsayisi / 2)):
            sonuc.append(butunTakimlar[eslesmeler[hs - 1][a][0]] + " - " + butunTakimlar[eslesmeler[hs - 1][a][1]])
        sonuc.append("----------")

    hs = 0
    for i in range(takimsayisi, (takimsayisi * 2 - 1)):
        sonuc.append((str(i) + ". Hafta"))
        sonuc.append("----------")
        for a in range(int(takimsayisi / 2)):
            sonuc.append(butunTakimlar[eslesmeler[hs][a][1]] + " - " + butunTakimlar[eslesmeler[hs][a][0]])
        sonuc.append("----------")
        hs += 1

    return jsonify(sonuc)





