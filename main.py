from datetime import datetime
import sqlalchemy
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine, text, MetaData, Table, insert, select
from sqlalchemy.orm import Session
import json

class BaseDataTables:
    
    def __init__(self, request, columns, collection):
        
        self.columns = columns

        self.collection = collection
         
        # values specified by the datatable for filtering, sorting, paging
        self.request_values = request.values
         
 
        # results from the db
        self.result_data = None
         
        # total in the table after filtering
        self.cardinality_filtered = 0
 
        # total in the table unfiltered
        self.cadinality = 0
 
        self.run_queries()
    
    def output_result(self):
        
        output = {}

        # output['sEcho'] = str(int(self.request_values['sEcho']))
        output['draw'] = 1
        #output['recordsTotal'] = 2
        #output['recordsFiltered'] = 2
        aaData_rows = []
        
        for row in self.result_data:
            aaData_row = {}
            for i in range(len(self.columns)):
                #print row, self.columns, self.columns[i]
                if isinstance(row[self.columns[i]], str):
                    aaData_row[self.columns[i]] = row[self.columns[i]].replace('"','\\"');
                else:
                    aaData_row[self.columns[i]] = row[self.columns[i]];
            aaData_rows.append(aaData_row)
            
        output['data'] = aaData_rows
        
        return output
    
    def run_queries(self):
        
         self.result_data = self.collection
         self.cardinality_filtered = len(self.result_data)
         self.cardinality = len(self.result_data)

columns = [ 'no', 'name', 'type', 'date']








app = Flask(__name__)

#app.json_encoder = CustomJSONEncoder
app.config.from_pyfile("config.py")
database     = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
app.database = database
connection = database.connect()
metadata = MetaData()
mytable = Table('first', metadata, autoload=True, autoload_with=database)

print(sqlalchemy.__version__)
print(mytable.columns.keys())

#stmt = insert(mytable).values(no=1, name="jame", type=1, date=datetime.now())
#print(stmt)
#connection.execute(stmt)

stmt = select(mytable).where(mytable.c.name == 'jame')

#with Session(database) as session:
    #for row in session.execute(stmt):
        #print(row)
        #print(row.no)
        #print(row.name)

Bootstrap(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/22')
def home2():
    return render_template('index2.html')
	
@app.route('/dt')
def dt():
    print('requested')
    collection = []
    with Session(database) as session:
        for row in session.execute(stmt):
            collection.append(dict(zip(columns, [row.no, row.name, row.type, row.date])));
    
    results = BaseDataTables(request, columns, collection).output_result()
    
    return json.dumps(results, default=str)


@app.route('/sub')
def sub():
    print('sub requested')
    columns1 = [ 'name']


    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return 'No parameter'

    parameters = ''
    for key in parameter_dict.keys():
        parameters += 'key: {}, value: {}\n'.format(key, request.args[key])

    print(parameters)

    collection = []
    collection.append(dict(zip(columns1, ['aaaaaa'])));
    output = {}
    output['html']='<p>aaaaaaaaaaaaaaaa</p>';
    return json.dumps(output, default=str)

@app.route('/add')
def add():
    print('add requested')
    columns1 = [ 'name']


    parameter_dict = request.args.to_dict()
    if len(parameter_dict) == 0:
        return 'No parameter'

    parameters = ''
    output = {}
    for key in parameter_dict.keys():
        parameters += 'key: {}, value: {}\n'.format(key, request.args[key])
        output[key] = request.args[key]

    print(parameters)
    
    return json.dumps(output, default=str)


if __name__ == '__main__':
    app.run(debug=True)