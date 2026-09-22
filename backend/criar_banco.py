import sqlite3

def init_db():
    conn = sqlite3.connect("banco.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS marcas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            pais TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS miniaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            modelo TEXT NOT NULL,
            escala TEXT NOT NULL,
            preco REAL NOT NULL,
            marca_id INTEGER NOT NULL,
            FOREIGN KEY (marca_id) REFERENCES marcas(id)
        )
    """)

    cur.execute("INSERT INTO marcas (nome, pais) VALUES ('Matchbox', 'Reino Unido')")
    cur.execute("INSERT INTO marcas (nome, pais) VALUES ('Jada Toys', 'EUA')")

    cur.execute("INSERT INTO miniaturas (modelo, escala, preco, marca_id) VALUES ('Ford Mustang 1969', '1:64', 32.50, 1)")
    cur.execute("INSERT INTO miniaturas (modelo, escala, preco, marca_id) VALUES ('Dodge Charger 1970', '1:24', 199.90, 2)")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
