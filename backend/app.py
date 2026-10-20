
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petshop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# MODELO DONO
class Dono(db.Model):
    __tablename__ = "donos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    # Relacionamento entre dono e pets
    pets = db.relationship("Pet", backref="dono")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone
        }


# MODELO PET
class Pet(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    dono_id = db.Column(
        db.Integer,
        db.ForeignKey("donos.id"),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "especie": self.especie,
            "idade": self.idade,
            "dono_id": self.dono_id,
            "dono_nome": self.dono.nome
        }


# ROTAS DE DONOS

@app.route("/donos", methods=["GET"])
def listar_donos():
    donos = Dono.query.all()
    return jsonify([dono.to_dict() for dono in donos])


@app.route("/donos/<int:dono_id>", methods=["GET"])
def buscar_dono(dono_id):
    dono = db.session.get(Dono, dono_id)

    if dono is None:
        return jsonify({"erro": "Dono nao encontrado"}), 404

    return jsonify(dono.to_dict())


@app.route("/donos", methods=["POST"])
def criar_dono():
    dados = request.get_json(silent=True) or {}

    if not dados.get("nome") or not dados.get("telefone"):
        return jsonify({
            "erro": "Informe nome e telefone"
        }), 400

    novo_dono = Dono(
        nome=dados["nome"],
        telefone=dados["telefone"]
    )

    db.session.add(novo_dono)
    db.session.commit()

    return jsonify(novo_dono.to_dict()), 201


@app.route("/donos/<int:dono_id>", methods=["PUT"])
def atualizar_dono(dono_id):
    dados = request.get_json(silent=True) or {}

    if not dados.get("nome") or not dados.get("telefone"):
        return jsonify({
            "erro": "Informe nome e telefone"
        }), 400

    dono = db.session.get(Dono, dono_id)

    if dono is None:
        return jsonify({"erro": "Dono nao encontrado"}), 404

    dono.nome = dados["nome"]
    dono.telefone = dados["telefone"]

    db.session.commit()

    return jsonify(dono.to_dict())


@app.route("/donos/<int:dono_id>", methods=["DELETE"])
def remover_dono(dono_id):
    dono = db.session.get(Dono, dono_id)

    if dono is None:
        return jsonify({"erro": "Dono nao encontrado"}), 404

    if dono.pets:
        return jsonify({
            "erro": "Nao e possivel remover um dono que possui pets"
        }), 400

    db.session.delete(dono)
    db.session.commit()

    return jsonify({
        "mensagem": "Dono removido com sucesso"
    })


# ROTAS DE PETS

# GET /pets
# GET /pets?dono_id=1
@app.route("/pets", methods=["GET"])
def listar_pets():
    dono_id = request.args.get("dono_id")

    if dono_id is not None:
        try:
            dono_id = int(dono_id)
        except (ValueError, TypeError):
            return jsonify({"erro": "dono_id invalido"}), 400

        pets = Pet.query.filter_by(dono_id=dono_id).all()
    else:
        pets = Pet.query.all()

    return jsonify([pet.to_dict() for pet in pets])


# GET /pets/<id>
@app.route("/pets/<int:pet_id>", methods=["GET"])
def buscar_pet(pet_id):
    pet = db.session.get(Pet, pet_id)

    if pet is None:
        return jsonify({"erro": "Pet nao encontrado"}), 404

    return jsonify(pet.to_dict())


# POST /pets
@app.route("/pets", methods=["POST"])
def criar_pet():
    dados = request.get_json(silent=True) or {}

    campos = ["nome", "especie", "idade", "dono_id"]

    if not all(campo in dados for campo in campos):
        return jsonify({
            "erro": "Informe nome, especie, idade e dono_id"
        }), 400

    if not dados["nome"] or not dados["especie"]:
        return jsonify({
            "erro": "Informe nome, especie, idade e dono_id"
        }), 400

    try:
        idade = int(dados["idade"])
        dono_id = int(dados["dono_id"])
    except (ValueError, TypeError):
        return jsonify({
            "erro": "idade e dono_id devem ser numeros inteiros"
        }), 400

    if idade < 0:
        return jsonify({"erro": "idade invalida"}), 400

    dono = db.session.get(Dono, dono_id)

    if dono is None:
        return jsonify({"erro": "Dono nao encontrado"}), 404

    novo_pet = Pet(
        nome=dados["nome"],
        especie=dados["especie"],
        idade=idade,
        dono_id=dono_id
    )

    db.session.add(novo_pet)
    db.session.commit()

    return jsonify(novo_pet.to_dict()), 201


# PUT /pets/<id>
@app.route("/pets/<int:pet_id>", methods=["PUT"])
def atualizar_pet(pet_id):
    dados = request.get_json(silent=True) or {}

    campos = ["nome", "especie", "idade", "dono_id"]

    if not all(campo in dados for campo in campos):
        return jsonify({
            "erro": "Informe nome, especie, idade e dono_id"
        }), 400

    if not dados["nome"] or not dados["especie"]:
        return jsonify({
            "erro": "Informe nome, especie, idade e dono_id"
        }), 400

    pet = db.session.get(Pet, pet_id)

    if pet is None:
        return jsonify({"erro": "Pet nao encontrado"}), 404

    try:
        idade = int(dados["idade"])
        dono_id = int(dados["dono_id"])
    except (ValueError, TypeError):
        return jsonify({
            "erro": "idade e dono_id devem ser numeros inteiros"
        }), 400

    if idade < 0:
        return jsonify({"erro": "idade invalida"}), 400

    dono = db.session.get(Dono, dono_id)

    if dono is None:
        return jsonify({"erro": "Dono nao encontrado"}), 404

    pet.nome = dados["nome"]
    pet.especie = dados["especie"]
    pet.idade = idade
    pet.dono_id = dono_id

    db.session.commit()

    return jsonify(pet.to_dict())


# DELETE /pets/<id>
@app.route("/pets/<int:pet_id>", methods=["DELETE"])
def remover_pet(pet_id):
    pet = db.session.get(Pet, pet_id)

    if pet is None:
        return jsonify({"erro": "Pet nao encontrado"}), 404

    db.session.delete(pet)
    db.session.commit()

    return jsonify({
        "mensagem": "Pet removido com sucesso"
    })


if __name__ == "__main__":
    app.run(debug=True)
