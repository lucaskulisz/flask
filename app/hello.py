import psycopg2
from flask import Flask, render_template, request, url_for,redirect, jsonify


app = Flask(__name__)
db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'lucaskulisz',
    'host': 'localhost',
    'port': '5432',  # Default PostgreSQL port
}



@app.route("/")
def hello_world():
    #return "<h1>Hello, World again!</h1>"
    courses= ["php","java","javascript","kotlin","solidity"]
    data={
        'titulo':'indexNew',
        'bienvenida':'¡Grettings!',
        'courses':courses,
        'number of courses':len(courses)
    }
    return render_template('index.html', data=data)

@app.route('/contacto/<name>/<int:age>')
def contacto(name,age):
    data={
        'titulo':'contacto',
        'nombre':name,
        'edad':age,
    }
    return render_template('contacto.html', data=data)
def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return 'ok'

@app.route('/cursos')
def listar_cursos():
    data = {}
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT code, name, grades FROM subjects ORDER BY name ASC")
                cursos = cursor.fetchall()
                print(cursos)
                data['cursos'] = cursos
                data['mensaje'] = 'Exito'
    except Exception as ex:
        data['mensaje'] = 'Error...'
    return jsonify(data)

def pagina_no_encontrada(error):
    #return render_template('404.html'), 404
    return redirect(url_for('hello_world'))

if __name__=='__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
