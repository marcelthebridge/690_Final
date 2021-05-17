
from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import abort, request, escape, make_response
import numpy as np
import pandas as pd
import pickle
import json
import viz

app = Flask(__name__)
#filename = 'Project2Data.csv'
#model = pickle.load(open(filename, 'rb'))
engine = create_engine('sqlite+pysqlite:///app.db', echo=True)

with engine.connect() as conn:
    if not engine.dialect.has_table(conn, 'resourcetable'):
        conn.execute(text("CREATE TABLE resourcetable (Name string, County string, Category string, Type string, General string, Industry string, Audience string, Stage string, Venture string)"))


@app.route('/submitdata', methods=['PUT'])
def submitdata():

    print(1)
    global engine
    if request.method == "PUT":
        if request.data:
            print(json.loads(request.data))
            data = json.loads(request.data)
            try:
                with engine.connect() as conn:
                    print('Adding Record')
                    conn.execute(text(
                        "INSERT INTO resourcetable (Name, County, Category, Type, General, Industry, Audience, Stage, "
                        "Venture)VALUES(:Name, :County, :Category, :Type, :General, :Industry, :Audience, :Stage, "
                        ":Venture)"),
                                 {"Name": data['Name'], "County": data['County'], "Category": data['Category'],
                                  "Type": data['Type'], "General": data['General'],
                                "Industry": data['Industry'], "Audience": data['Audience'], "Stage": data['Stage'],
                                "Venture": data['Venture']})
                    conn.commit()
                return 'resource recorded'
            except:
                abort(405)
        else:
            abort(405)
    else:
        abort(405)


@app.route('/gettable', methods=['GET'])
def gettable():
    global engine
    if request.method == "GET":
        with engine.connect() as conn:
            results = conn.execute(text("SELECT * FROM resource"))
            return {'data': [{'Name': r[0], 'County': r[1], 'Category': r[2], 'Type': r[3], 'General': r[4],
                              'Industry': r[5], 'Audience': r[6], 'Stage': r[7], 'Venture': r[8]} for r in
                             results.fetchall()]}
    else:
        abort(405)


@app.errorhandler(405)
def malformed_query(error):
    """
    Redirects 405 errors
    """
    resp = make_response("Malformed Query")
    return resp


if __name__ == "__main__":
    app.run(host='localhost')
