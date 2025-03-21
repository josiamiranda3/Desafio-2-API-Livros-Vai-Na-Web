from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
# informa o arquivo principal


def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     titulo TEXT NOT NULL,
                     categoria TEXT NOT NULL,
                     autor TEXT NOT NULL,
                     imagem_url TEXT NOT NULL
                     )
                     """)
        print("Banco de dados inicalizado com sucesso!!")


init_db()
# com o conn vai jogar tudo para o conn
# with e um atalho criando uma porta de abertura e fechamento

# informa a localização e o seu utem que irá utilizar


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route("/doar", methods=['POST'])
# vai rodar
def doar():

    dados = request.get_json()
    # ferramenta com uso + definido precisando chamer em cima e agora
    # criação das variveis com os nomes que irão chegar (REQUEST-irão dar a permissão)
    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    imagem_url = dados.get("imagem_url")

    if not titulo or not categoria or not autor or not imagem_url:
     # if not all([titulo,categoria,autor,imagem_url]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    with sqlite3.connect('database.db') as conn:
        conn.execute(
            """ INSERT INTO livros(titulo,categoria,autor,imagem_url) VALUES(?,?,?,?)""", (titulo, categoria, autor, imagem_url))
        conn.commit()
        # salvar os dados que foram inseridos no banco de dados
        # '{titulo}','{categoria}','{autor}','{imagem_url}'
        return jsonify({'mensagem': 'Livros cadastrados com sucesso'}), 201


@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as conn:
        livros = conn.execute("SELECT * FROM  livros").fetchall()

    livros_formatados = []

    for livro in livros:
        dicionario_livros = {
            "id": livro[0],
            "titulo": livro[1],
            "categoria": livro[2],
            "autor": livro[3],
            "imagem_url": livro[4]
        }
        livros_formatados.append(dicionario_livros)
    return jsonify(livros_formatados)


@app.route('/livros/<int:livro_id>', methods=['DELETE'])
def deletar_livro(livro_id):
    with sqlite3.connect('database.db') as conn:
        conexao_cursor = conn.cursor()
        conexao_cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
        conn.commit()
    if conexao_cursor.rowcount == 0:
        # sendo um comando para verificar se realmente esta certo o valor da tabela e não 0
        return jsonify({"erro": "Livro não encontrado"}), 400
    return jsonify({"Mensagem": "Livro excluido com Sucesso"}), 200


if __name__ == "__main__":
    app.run(debug=True)
