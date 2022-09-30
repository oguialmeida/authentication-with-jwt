from flask import Flask, request, jsonify, make_response, request, render_template, session
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'YOU_SECRET_KEY'

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('629752071f4583fc878c39bb38fa06db')
        if not token:
            return jsonify({'Alert!': 'Nenhum token encontrado!'}), 401

        try:

            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Message': 'Token inválido!'}), 403
        return func(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('inicial.html')

@app.route('/public')
def public():
    return 'Publico'

@app.route('/auth')
@token_required
def auth():
    return 'JWT verificado, seja bem vindo :D'


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == 'Guilherme' and request.form['password'] == '123456':
        session['logged_in'] = True

        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=60))
        },
            app.config['SECRET_KEY'])
        return jsonify({'token': token})
    else:
        return make_response('Não foi possível verificar', 403, {'WWW-Authenticate': 'Basic realm: "Falha na autenticação"'})


@app.route('/logout', methods=['POST'])
def logout():
    pass

if __name__ == "__main__":
    app.run(debug=True)
