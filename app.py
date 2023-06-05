from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

MYSQLDB_HOST = "db4free.net"
MYSQLDB_USUARIO = "bertin11"
MYSQLDB_PASSWORD = "bertin11"
MYSQLDB_BD = "bertin_bd"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQLDB_USUARIO}:{MYSQLDB_PASSWORD}@{MYSQLDB_HOST}/{MYSQLDB_BD}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class articulo(db.Model):

    __tablename__ = 'articulos'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    tipoarticulo = db.Column(db.Integer, nullable=False)
    foto = db.Column(db.String(100), nullable=False)

    def __init__(self, marca, modelo, tipoarticulo,  foto):
        self.marca = marca
        self.modelo = modelo
        self.tipoarticulo = tipoarticulo
        self.foto = foto


""" db.create_all() """


class articuloSchema(ma.Schema):
    class Meta:
        fields = ('id', 'marca', 'modelo', 'tipoarticulo',  'foto')


articulo_schema = articuloSchema()
articulos_schema = articuloSchema(many=True)


@app.route('/articulos', methods=['POST'])
def create_articulo():
    marca = request.json['marca']
    modelo = request.json['modelo']
    tipoarticulo = request.json['tipoarticulo']

    foto = request.json['foto']

    new_articulo = articulo(marca, modelo, tipoarticulo, foto)

    db.session.add(new_articulo)
    db.session.commit()

    return articulo_schema.jsonify(new_articulo)


@app.route('/articulos', methods=['GET'])
def get_articulos():
    all_articulos = articulo.query.all()
    result = articulos_schema.dump(all_articulos)
    return jsonify(result)


@app.route('/articulos/<id>', methods=['GET'])
def get_articulo(id):
    articulos = articulo.query.get(id)
    return articulo_schema.jsonify(articulos)


@app.route('/articulos/<id>', methods=['PUT'])
def update_articulo(id):
    articulo = articulo.query.get(id)

    marca = request.json['marca']
    modelo = request.json['modelo']
    tipoarticulo = request.json['tipoarticulo']

    foto = request.json['foto']

    articulo.marca = marca
    articulo.modelo = modelo
    articulo.tipoarticulo = tipoarticulo

    articulo.foto = foto

    db.session.commit()

    return articulo_schema.jsonify(articulo)


@app.route('/articulos/<id>', methods=['DELETE'])
def delete_articulo(id):
    articulo = articulo.query.get(id)
    db.session.delete(articulo)
    db.session.commit()
    return articulo_schema.jsonify(articulo)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'API Rest Python de Bertin Barahona, para mostrar todos los articulos agregar /articulos a la url. Para un articulo especifico /articulos/id'})


if __name__ == "__main__":
    app.run(debug=True)
