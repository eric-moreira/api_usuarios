from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE= os.getenv('DATABASE')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'{DATABASE}'

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'tabela_de_contatos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(200))

    def __repr__(self):
        return f'<Usuario {self.nome}>'

'''
with app.app_context():
    db.create_all()
    novo_usuario = Usuario(nome='João', telefone='123456789', endereco='Rua A, 123')
    db.session.add(novo_usuario)
    db.session.commit()
    usuarios = Usuario.query.all()
    print(usuarios)
'''

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    # Define get usuarios all
    usuarios = Usuario.query.all()
    output = []
    for usuario in usuarios:
        usuario_data = {}
        usuario_data['id'] = usuario.id
        usuario_data['nome'] = usuario.nome
        usuario_data['telefone'] = usuario.telefone
        usuario_data['endereco'] = usuario.endereco
        output.append(usuario_data)
    return jsonify({'usuarios': output})

@app.route('/usuarios/<usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    # Define get usuario by id
    usuario = Usuario.query.get_or_404(usuario_id)
    output = {}
    output['id'] = usuario.id
    output['nome'] = usuario.nome
    output['telefone'] = usuario.telefone
    output['endereco'] = usuario.endereco
    return jsonify({'usuario': output})

@app.route('/usuarios', methods=['POST'])
def add_usuario():
    # Define add usuario
    data = request.get_json()
    new_usuario = Usuario(nome=data['nome'], telefone=data['telefone'], endereco=data['endereco'])
    db.session.add(new_usuario)
    db.session.commit()
    return jsonify({'message': 'New usuario created!'})

@app.route('/usuarios/<usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    # Define delete usuario
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'The usuario has been deleted!'})


if __name__ == '__main__':
    app.run(debug=True)






