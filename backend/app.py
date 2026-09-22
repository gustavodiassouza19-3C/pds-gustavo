import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

def db():
    return sqlite3.connect("banco.db")

@app.route("/miniaturas", methods=["GET"])
def listar():
    marca_id = request.args.get("marca_id")
    con = db()
    sql = "SELECT m.id, m.modelo, m.escala, m.preco, m.marca_id, b.nome FROM miniaturas m JOIN marcas b ON m.marca_id = b.id"
    
    if marca_id:
        linhas = con.execute(sql + " WHERE m.marca_id = ?", (marca_id,)).fetchall()
    else:
        linhas = con.execute(sql).fetchall()
    con.close()
    
    return jsonify([
        {"id": l[0], "modelo": l[1], "escala": l[2], "preco": l[3], "marca_id": l[4], "marca_nome": l[5]} 
        for l in linhas
    ]), 200

@app.route("/miniaturas/<int:id>", methods=["GET"])
def buscar(id):
    con = db()
    l = con.execute("SELECT m.id, m.modelo, m.escala, m.preco, m.marca_id, b.nome FROM miniaturas m JOIN marcas b ON m.marca_id = b.id WHERE m.id = ?", (id,)).fetchone()
    con.close()
    
    if not l:
        return jsonify({"erro": "Miniatura nao encontrada"}), 404
        
    return jsonify({"id": l[0], "modelo": l[1], "escala": l[2], "preco": l[3], "marca_id": l[4], "marca_nome": l[5]}), 200

@app.route("/miniaturas", methods=["POST"])
def criar():
    d = request.get_json() or {}
    campos = ["modelo", "escala", "preco", "marca_id"]
    if not all(k in d for k in campos):
        return jsonify({"erro": "Informe modelo, escala, preco e marca_id"}), 400
        
    con = db()
    cur = con.execute("INSERT INTO miniaturas (modelo, escala, preco, marca_id) VALUES (?, ?, ?, ?)", (d["modelo"], d["escala"], d["preco"], d["marca_id"]))
    con.commit()
    novo_id = cur.lastrowid
    con.close()
    
    return jsonify({"id": novo_id, **d}), 201

@app.route("/miniaturas/<int:id>", methods=["PUT"])
def atualizar(id):
    d = request.get_json() or {}
    campos = ["modelo", "escala", "preco", "marca_id"]
    if not all(k in d for k in campos):
        return jsonify({"erro": "Informe modelo, escala, preco e marca_id"}), 400
        
    con = db()
    cur = con.execute("UPDATE miniaturas SET modelo=?, escala=?, preco=?, marca_id=? WHERE id=?", (d["modelo"], d["escala"], d["preco"], d["marca_id"], id))
    con.commit()
    encontrado = cur.rowcount > 0
    con.close()
    
    if not encontrado:
        return jsonify({"erro": "Miniatura nao encontrada"}), 404
        
    return jsonify({"id": id, **d}), 200

@app.route("/miniaturas/<int:id>", methods=["DELETE"])
def deletar(id):
    con = db()
    cur = con.execute("DELETE FROM miniaturas WHERE id=?", (id,))
    con.commit()
    encontrado = cur.rowcount > 0
    con.close()
    
    if not encontrado:
        return jsonify({"erro": "Miniatura nao encontrada"}), 404
        
    return jsonify({"mensagem": "Miniatura removida com sucesso"}), 200

if __name__ == "__main__":
    app.run(debug=True)
