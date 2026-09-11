import sqlite3

BANCO = "petshop.db"

conexao = sqlite3.connect(BANCO)
cursor = conexao.cursor()

# Apaga as tabelas antigas para o script poder ser rodado de novo
cursor.execute("DROP TABLE IF EXISTS pets")
cursor.execute("DROP TABLE IF EXISTS donos")

cursor.execute("""
CREATE TABLE donos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    especie TEXT NOT NULL,
    idade INTEGER NOT NULL,
    dono_id INTEGER NOT NULL,
    FOREIGN KEY (dono_id) REFERENCES donos (id)
)
""")

donos = [
    ("Ana Paula Ribeiro", "45999110001"),
    ("Bruno Cardoso", "45999110002"),
    ("Carla Meneghel", "45999110003")
]

for dono in donos:
    cursor.execute("INSERT INTO donos (nome, telefone) VALUES (?, ?)", dono)

pets = [
    ("Rex", "cachorro", 4, 1),
    ("Mimi", "gato", 2, 1),
    ("Thor", "cachorro", 7, 2),
    ("Nina", "gato", 1, 3),
    ("Pingo", "passaro", 3, 3)
]

for pet in pets:
    cursor.execute(
        "INSERT INTO pets (nome, especie, idade, dono_id) VALUES (?, ?, ?, ?)",
        pet
    )

conexao.commit()
conexao.close()

print("Banco criado com sucesso.")
print(f"Foram inseridos {len(donos)} donos e {len(pets)} pets.")
