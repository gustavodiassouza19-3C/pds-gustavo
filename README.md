# API Petshop

Projeto da disciplina de Programacao no Desenvolvimento de Sistemas.

Este repositorio vai crescer durante todo o trimestre. Comecamos com uma API
simples usando Flask e sqlite3, e ao longo das aulas ela vai ganhar ORM,
separacao em camadas, login e, no final, um front-end em React.

**Nao apague nem recomece o projeto a cada aula.** O codigo evolui aqui dentro.

## Como rodar

### No GitHub Codespaces (recomendado)

1. Clique em **Code > Codespaces > Create codespace on main**.
2. Espere a preparacao terminar. O Flask ja e instalado automaticamente.
3. No terminal, entre na pasta do back-end e crie o banco:

```
cd backend
python criar_banco.py
```

4. Suba o servidor:

```
python app.py
```

### Na sua maquina

```
cd backend
pip install -r requirements.txt
python criar_banco.py
python app.py
```

O servidor sobe em `http://localhost:5000`.

## Como testar as rotas

Abra o arquivo `backend/requisicoes.http` e clique em **Send Request** acima de
cada requisicao. A resposta aparece ao lado.

O arquivo `petshop.db` nao vai para o GitHub, ele esta no `.gitignore`. Sempre
que voce abrir o projeto em um lugar novo, rode `python criar_banco.py` para
recriar o banco com os dados de exemplo.

## Modelo de dados

**donos**

| campo    | tipo    | observacao     |
|----------|---------|----------------|
| id       | INTEGER | chave primaria |
| nome     | TEXT    | obrigatorio    |
| telefone | TEXT    | obrigatorio    |

**pets**

| campo   | tipo    | observacao                      |
|---------|---------|---------------------------------|
| id      | INTEGER | chave primaria                  |
| nome    | TEXT    | obrigatorio                     |
| especie | TEXT    | obrigatorio                     |
| idade   | INTEGER | obrigatorio                     |
| dono_id | INTEGER | chave estrangeira para donos.id |

## Contrato das rotas

As rotas de **donos** ja estao prontas no `app.py`. Use elas como modelo.
As rotas de **pets** sao a sua tarefa.

### GET /pets

Lista todos os pets. A resposta traz o **nome do dono**, e nao apenas o
`dono_id`. Para isso voce precisa usar JOIN na consulta.

Resposta `200`:

```json
[
    {
        "id": 1,
        "nome": "Rex",
        "especie": "cachorro",
        "idade": 4,
        "dono_id": 1,
        "dono_nome": "Ana Paula Ribeiro"
    }
]
```

### GET /pets?dono_id=1

A mesma rota acima aceita um filtro opcional por query param. Se o `dono_id`
for enviado, retorna apenas os pets daquele dono. Se nao for enviado, retorna
todos.

### GET /pets/{id}

Busca um pet pelo id.

Resposta `200`: o objeto do pet.

Resposta `404`: `{"erro": "Pet nao encontrado"}`

### POST /pets

Cadastra um pet.

Corpo da requisicao:

```json
{
    "nome": "Bidu",
    "especie": "cachorro",
    "idade": 2,
    "dono_id": 1
}
```

Resposta `201`: o pet criado, com o `id` gerado pelo banco.

Resposta `400`: `{"erro": "Informe nome, especie, idade e dono_id"}`

### PUT /pets/{id}

Atualiza um pet. Recebe os mesmos campos do POST.

Resposta `200`: o pet atualizado.

Resposta `404`: `{"erro": "Pet nao encontrado"}`

### DELETE /pets/{id}

Remove um pet.

Resposta `200`: `{"mensagem": "Pet removido com sucesso"}`

Resposta `404`: `{"erro": "Pet nao encontrado"}`

## Entrega

Quando terminar, salve o trabalho no GitHub:

```
git add .
git commit -m "aula01: api base"
git push
```

Confira no site do GitHub se os arquivos aparecem la antes de sair do
laboratorio.

## Estrutura do repositorio

```
pds-seunome/
├── .devcontainer/           configuracao do Codespaces
├── backend/                 a API
│   ├── app.py               as rotas
│   ├── criar_banco.py       cria as tabelas e os dados de exemplo
│   ├── requisicoes.http     requisicoes de teste
│   └── requirements.txt
├── exercicios/              exercicios avulsos de cada aula
└── README.md
```
