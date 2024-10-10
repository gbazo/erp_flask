"""
Este módulo define o aplicativo Flask para um sistema de gestão, incluindo rotas para autenticação, 
gestão de inventário, clientes, vendas, relatórios, configurações e backup.

O aplicativo usa MySQL para armazenamento de dados e Bcrypt para hashing de senhas. 
Também utiliza Flask-WeasyPrint para geração de PDFs.
"""

from flask import Flask, jsonify, redirect, render_template, request, url_for, session, flash
from flask_weasyprint import HTML, render_pdf
from flask_mysqldb import MySQL
from pypix.pix import Pix
import mercadopago
import bcrypt
import time
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'gbazo'
app.config['MYSQL_PASSWORD'] = 'gbazo'
app.config['MYSQL_DB'] = 'erp_flask'

mysql = MySQL(app)

# Initialize Mercado Pago client with your access token
sdk = mercadopago.SDK("TEST-5673567343902508-090208-409c1b6d4bdae826c6fe809fc78253dc-64227987")

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    """
    Gerencia o processo de autenticação de usuários na aplicação.

    Este endpoint suporta os métodos GET e POST para lidar com o fluxo de login dos usuários.

    - Em uma requisição GET, a função simplesmente renderiza a página de login para o usuário, permitindo que ele insira suas credenciais.
    
    - Em uma requisição POST, a função processa as credenciais fornecidas pelo usuário:
        1. Recebe o nome de usuário e a senha enviados pelo formulário.
        2. Verifica no banco de dados se o nome de usuário existe e se a senha fornecida corresponde ao hash armazenado.
        3. Se as credenciais forem válidas:
            - Cria uma sessão para o usuário, armazenando seu nome de usuário e ID na sessão.
            - Redireciona o usuário para a página inicial (ou outra página definida).
        4. Se as credenciais forem inválidas:
            - Exibe uma mensagem de erro informando que a tentativa de login falhou.
            - Redireciona de volta para a página de login, permitindo que o usuário tente novamente.

    Returns:
        render_template: Retorna a página de login em requisições GET ou em caso de falha na autenticação.
        redirect: Redireciona para a página inicial em caso de sucesso na autenticação.

    Exceptions:
        - Nenhuma exceção específica é capturada nesta função, mas falhas na conexão com o banco de dados ou outros erros inesperados podem resultar em uma resposta de erro do servidor.

    Side Effects:
        - Modifica a sessão do usuário no lado do servidor ao armazenar o 'username' e 'user_id' em caso de autenticação bem-sucedida.
    """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, password_hash FROM usuarios WHERE username = %s", [username])
        usuario = cursor.fetchone()

        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario[1].encode('utf-8')):
            session['username'] = username
            session['user_id'] = usuario[0]
            return redirect(url_for('inicio'))
        else:
            flash('Login falhou. Por favor, verifique seu nome de usuário e senha.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/')
def index():
    
    """
    Redireciona o usuário para a página apropriada com base no estado de autenticação.

    Este endpoint é utilizado como a rota raiz da aplicação e serve para determinar a página de destino do usuário dependendo de seu status de autenticação:

    - Se o usuário já estiver autenticado (ou seja, se existir uma sessão com 'username'), ele será redirecionado para a página inicial da aplicação.
    
    - Se o usuário não estiver autenticado (não houver 'username' na sessão), ele será redirecionado para a página de login.

    Returns:
        redirect: Um redirecionamento HTTP para:
            - A página inicial da aplicação (`url_for('inicio')`) se o usuário estiver autenticado.
            - A página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Nenhum efeito colateral explícito além da verificação da sessão do usuário e do redirecionamento apropriado.

    Exceptions:
        - Esta função assume que a sessão está configurada corretamente. Qualquer falha na configuração da sessão ou problemas com a função de redirecionamento podem causar erros inesperados.
    """

    if 'username' in session:
        return redirect(url_for('inicio'))
    return redirect(url_for('login'))

@app.route('/inicio')
def inicio():
    
    """
    Renderiza a página inicial da aplicação com as informações da empresa.

    Esta função é responsável por carregar e exibir a página inicial da aplicação, 
    apresentando os dados básicos da empresa armazenados no banco de dados.

    - A função acessa o banco de dados para recuperar as informações da empresa, como nome, CNPJ, endereço, telefone e email.
    - Essas informações são passadas para o template `inicio.html`, onde são exibidas ao usuário.

    Returns:
        render_template: Renderiza o template `inicio.html`, fornecendo como contexto os dados da empresa recuperados do banco de dados.

    Side Effects:
        - Realiza uma consulta ao banco de dados para buscar as informações da empresa, o que pode falhar se houver problemas na conexão com o banco de dados ou na execução da query.

    Exceptions:
        - Qualquer problema na conexão com o banco de dados ou na execução da consulta pode gerar exceções que não são tratadas explicitamente nesta função. Tais exceções resultariam em um erro de servidor.
    """

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nome, cnpj, endereco, telefone, email FROM empresa LIMIT 1")
    empresa = cursor.fetchone()
    return render_template('inicio.html', empresa=empresa)

@app.route('/estoque_compras')
def estoque_compras():

    """
    Renderiza a página de gestão de estoque e compras.

    Esta função é responsável por exibir a página que permite ao usuário visualizar e gerenciar o estoque de produtos e realizar operações relacionadas a compras.

    Returns:
        render_template: Renderiza o template `estoque_compras.html`, que contém a interface para gerenciar o estoque e as compras.
    """

    return render_template('estoque_compras.html')

@app.route('/fornecedores')
def fornecedores():

    """
    Renderiza a página de gerenciamento de fornecedores.

    Esta função é responsável por exibir a página onde o usuário pode visualizar, adicionar, editar ou remover fornecedores da base de dados.

    Returns:
        render_template: Renderiza o template `fornecedores.html`, que contém a interface para a gestão de fornecedores.
    """

    return render_template('fornecedores.html')

@app.route('/rh')
def rh():

    """
    Renderiza a página de recursos humanos.

    Esta função é responsável por exibir a página onde o usuário pode gerenciar informações relacionadas aos funcionários, incluindo cadastro, controle de ponto, benefícios e outras funções do RH.

    Returns:
        render_template: Renderiza o template `rh.html`, que contém a interface para a gestão de recursos humanos.
    """

    return render_template('rh.html')

@app.route('/logout')
def logout():
    """
    Encerra a sessão do usuário e redireciona para a página de login.

    Esta função é responsável por efetuar o logout do usuário, removendo suas informações da sessão ativa. Ao encerrar a sessão, o usuário é redirecionado para a página de login.

    - Remove o `username` e `user_id` da sessão, efetivamente desconectando o usuário.
    - Redireciona o usuário para a página de login, onde ele pode autenticar-se novamente, se desejar.

    Returns:
        redirect: Um redirecionamento HTTP para a página de login (`url_for('login')`).

    Side Effects:
        - Modifica a sessão do usuário no lado do servidor ao remover as chaves 'username' e 'user_id'.
    
    Exceptions:
        - Se a sessão não estiver configurada corretamente ou se o redirecionamento falhar, a função pode resultar em um erro de servidor, embora não trate exceções explicitamente.
    """
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    """
    Permite o cadastro de novos usuários no sistema.

    Esta função gerencia o fluxo de registro de novos usuários. Está disponível apenas para usuários autenticados:

    - Em uma requisição GET, a função renderiza o formulário de cadastro de novos usuários.
    
    - Em uma requisição POST, a função processa os dados enviados pelo formulário:
        1. Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
        2. Coleta o nome de usuário, senha e email enviados pelo formulário.
        3. Gera um hash seguro para a senha usando bcrypt.
        4. Insere o novo usuário no banco de dados com o nome de usuário, hash da senha e email.
        5. Confirma o cadastro com uma mensagem de sucesso e redireciona o usuário para a página de login.

    Returns:
        render_template: Renderiza o template `cadastrar.html` para exibir o formulário de cadastro.
        redirect: Redireciona para a página de login (`url_for('login')`) se o cadastro for bem-sucedido ou se o usuário não estiver autenticado.

    Side Effects:
        - Modifica o banco de dados ao inserir um novo registro na tabela `usuarios`.
        - Gera um hash seguro para a senha do usuário usando bcrypt.
        - Exibe uma mensagem flash de sucesso após o cadastro.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados, falhas na inserção de dados ou na geração do hash da senha. Essas exceções não são tratadas explicitamente na função.
    """
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO usuarios (username, password_hash, email) VALUES (%s, %s, %s)", (username, hashed, email))
        mysql.connection.commit()

        flash('Usuário cadastrado com sucesso.')

    return render_template('cadastrar.html')

@app.route('/inventario')
def inventario():
    """
    Exibe a página de inventário com todos os produtos cadastrados no sistema.

    Esta função é responsável por apresentar uma lista de todos os produtos disponíveis no banco de dados. A funcionalidade de inventário está disponível apenas para usuários autenticados:

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Realiza uma consulta no banco de dados para recuperar todos os produtos cadastrados.
    - Renderiza a página de inventário, passando a lista de produtos para o template.

    Returns:
        render_template: Renderiza o template `inventario.html`, que exibe a lista de produtos cadastrados.
        redirect: Redireciona para a página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Realiza uma consulta ao banco de dados para recuperar informações sobre os produtos.
    
    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da consulta SQL. Estas exceções não são tratadas explicitamente na função.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    return render_template('inventario.html', produtos=produtos)

@app.route('/inventario/add', methods=['POST'])
def add_produto():
    """
    Adiciona um novo produto ao inventário.

    Esta função permite que usuários autenticados adicionem novos produtos ao inventário do sistema:

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Recebe os dados do produto a partir do formulário submetido via POST, incluindo nome, quantidade, preço e código de barras.
    - Insere o novo produto no banco de dados, armazenando as informações fornecidas.
    - Redireciona o usuário de volta para a página de inventário após a inserção bem-sucedida.

    Returns:
        redirect: Redireciona para a página de inventário (`url_for('inventario')`) após a adição bem-sucedida do produto. Redireciona para a página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Realiza uma inserção no banco de dados para armazenar as informações do novo produto.
        - Modifica o estado do banco de dados ao adicionar um novo registro na tabela `produtos`.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da inserção SQL. Essas exceções não são tratadas explicitamente na função.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    nome = request.form['nome']
    quantidade = request.form['quantidade']
    preco = request.form['preco']
    cod_barras = request.form['codBarras']
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO produtos (nome, quantidade, preco, cod_barras) VALUES (%s, %s, %s, %s)", (nome, quantidade, preco, cod_barras))
    mysql.connection.commit()
    
    return redirect(url_for('inventario'))

@app.route('/inventario/edit', methods=['POST'])
def editar_produto():
    """
    Edita os dados de um produto no inventário.

    Esta função permite que usuários autenticados atualizem as informações de um produto existente no inventário:

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Recebe os dados atualizados do produto a partir do formulário submetido via POST, incluindo ID do produto, nome, quantidade, preço e código de barras.
    - Atualiza o registro correspondente no banco de dados com os novos valores fornecidos.
    - Redireciona o usuário de volta para a página de inventário após a atualização bem-sucedida.

    Returns:
        redirect: Redireciona para a página de inventário (`url_for('inventario')`) após a edição bem-sucedida do produto. Redireciona para a página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Realiza uma atualização no banco de dados para modificar as informações de um produto existente.
        - Modifica o estado do banco de dados ao atualizar um registro na tabela `produtos`.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da atualização SQL. Essas exceções não são tratadas explicitamente na função.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        nome = request.form['nome']
        quantidade = request.form['quantidade']
        preco = request.form['preco']
        cod_barras = request.form['codBarras']
        
        update_query = "UPDATE produtos SET nome=%s, quantidade=%s, preco=%s, cod_barras=%s WHERE id=%s"
        cursor.execute(update_query, (nome, quantidade, preco, cod_barras, produto_id))
        mysql.connection.commit()
        
        return redirect(url_for('inventario'))

@app.route('/inventario/delete/<int:produto_id>')
def excluir_produto(produto_id):
    """
    Exclui um produto do inventário.

    Esta função permite que usuários autenticados removam um produto do inventário do sistema:

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Recebe o ID do produto a ser excluído a partir do parâmetro da URL.
    - Executa uma operação de exclusão no banco de dados, removendo o produto correspondente ao ID fornecido.
    - Redireciona o usuário de volta para a página de inventário após a exclusão bem-sucedida.

    Args:
        produto_id (int): ID do produto a ser excluído do inventário.

    Returns:
        redirect: Redireciona para a página de inventário (`url_for('inventario')`) após a exclusão bem-sucedida. Redireciona para a página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Realiza uma exclusão no banco de dados, removendo um registro da tabela `produtos`.
        - Modifica o estado do banco de dados ao excluir o registro correspondente.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da exclusão SQL. Essas exceções não são tratadas explicitamente na função.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    delete_query = "DELETE FROM produtos WHERE id=%s"
    cursor.execute(delete_query, (produto_id,))
    mysql.connection.commit()
    return redirect(url_for('inventario'))

@app.route('/vendas')
def vendas():
    """
    Exibe a página de vendas da aplicação.

    Esta função é responsável por apresentar a interface de vendas, onde os usuários autenticados podem realizar operações relacionadas às vendas de produtos.

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Renderiza a página de vendas, permitindo que o usuário visualize e interaja com a interface de vendas.

    Returns:
        render_template: Renderiza o template `vendas.html`, que exibe a interface para gerenciamento de vendas.
        redirect: Redireciona para a página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Nenhum efeito colateral direto, além do redirecionamento do usuário, se necessário.

    Exceptions:
        - Não há tratamento explícito de exceções nesta função, mas falhas na renderização do template ou problemas de sessão podem causar erros de servidor.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('vendas.html')

@app.route('/clientes')
def clientes():
    """
    Exibe a página de clientes com a lista de todos os clientes cadastrados no sistema.

    Esta função é responsável por apresentar uma lista de todos os clientes registrados no banco de dados. A funcionalidade de visualização de clientes está disponível apenas para usuários autenticados:

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Realiza uma consulta ao banco de dados para recuperar todos os registros da tabela `clientes`.
    - Renderiza a página de clientes, passando a lista de clientes para o template.

    Returns:
        render_template: Renderiza o template `clientes.html`, que exibe a lista de clientes cadastrados.
        redirect: Redireciona para a página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Realiza uma consulta ao banco de dados para recuperar informações sobre os clientes.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da consulta SQL. Estas exceções não são tratadas explicitamente na função.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    return render_template('clientes.html', clientes=clientes)

@app.route('/cliente/add', methods=['POST'])
def add_cliente():
    """
    Adiciona um novo cliente ao banco de dados.

    Esta função processa a adição de um novo cliente ao sistema:

    - Recebe os dados do formulário submetido via POST, incluindo nome, endereço e telefone do cliente.
    - Insere um novo registro na tabela `clientes` do banco de dados com as informações fornecidas.
    - Redireciona o usuário de volta para a página de clientes após a adição bem-sucedida.

    Returns:
        redirect: Redireciona para a página de clientes (`url_for('clientes')`) após a inserção bem-sucedida do novo cliente.

    Side Effects:
        - Realiza uma inserção no banco de dados, adicionando um novo registro à tabela `clientes`.
        - Modifica o estado do banco de dados ao adicionar o novo cliente.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da inserção SQL. Essas exceções não são tratadas explicitamente na função.
    """
    nome = request.form['nome']
    endereco = request.form['endereco']
    telefone = request.form['telefone']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO clientes (nome, endereco, telefone) VALUES (%s, %s, %s)", (nome, endereco, telefone))
    mysql.connection.commit()

    return redirect(url_for('clientes'))

@app.route('/cliente/edit', methods=['POST'])
def edit_cliente():
    """
    Edita as informações de um cliente existente no banco de dados.

    Esta função permite a atualização dos dados de um cliente específico:

    - Recebe os dados atualizados do formulário submetido via POST, incluindo o ID do cliente, nome, endereço e telefone.
    - Atualiza o registro correspondente no banco de dados com os novos valores fornecidos.
    - Redireciona o usuário de volta para a página de clientes após a atualização bem-sucedida.

    Returns:
        redirect: Redireciona para a página de clientes (`url_for('clientes')`) após a edição bem-sucedida do cliente.

    Side Effects:
        - Realiza uma atualização no banco de dados, modificando o registro do cliente na tabela `clientes`.
        - Modifica o estado do banco de dados ao atualizar as informações do cliente.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da atualização SQL. Essas exceções não são tratadas explicitamente na função.
    """
    cliente_id = request.form['cliente_id']
    nome = request.form['nome']
    endereco = request.form['endereco']
    telefone = request.form['telefone']

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE clientes SET nome=%s, endereco=%s, telefone=%s WHERE cod=%s", (nome, endereco, telefone, cliente_id))
    mysql.connection.commit()

    return redirect(url_for('clientes'))

@app.route('/cliente/delete/<int:cliente_id>')
def delete_cliente(cliente_id):
    """
    Exclui um cliente do banco de dados.

    Esta função permite que um cliente seja removido do sistema, baseado em seu ID:

    - Recebe o ID do cliente a ser excluído a partir do parâmetro da URL.
    - Executa uma operação de exclusão no banco de dados, removendo o cliente correspondente ao ID fornecido.
    - Redireciona o usuário de volta para a página de clientes após a exclusão bem-sucedida.

    Args:
        cliente_id (int): ID do cliente a ser excluído.

    Returns:
        redirect: Redireciona para a página de clientes (`url_for('clientes')`) após a exclusão bem-sucedida.

    Side Effects:
        - Realiza uma exclusão no banco de dados, removendo um registro da tabela `clientes`.
        - Modifica o estado do banco de dados ao excluir o registro correspondente.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da exclusão SQL. Essas exceções não são tratadas explicitamente na função.
    """
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM clientes WHERE cod=%s", (cliente_id,))
    mysql.connection.commit()

    return redirect(url_for('clientes'))

@app.route('/buscar_produto')
def buscar_produto():
    """
    Busca um produto pelo código de barras e retorna suas informações.

    Esta função permite que um usuário autenticado busque um produto específico no banco de dados usando seu código de barras:

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Recebe o código de barras como um argumento de consulta na URL (`cod_barras`).
    - Realiza uma consulta no banco de dados para buscar o produto correspondente ao código de barras fornecido.
    - Retorna as informações do produto em formato JSON, incluindo ID, nome e preço.
    - Se o produto não for encontrado, retorna uma mensagem de erro com um código de status HTTP 404.

    Returns:
        jsonify: Um JSON contendo o ID, nome e preço do produto se encontrado. Caso contrário, retorna um JSON com uma mensagem de erro e um código de status 404.

    Side Effects:
        - Realiza uma consulta ao banco de dados para buscar informações sobre o produto.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da consulta SQL. Essas exceções não são tratadas explicitamente na função.
    """
    if 'username' not in session:
        return redirect(url_for('login'))

    cod_barras = request.args.get('cod_barras')

    cursor = mysql.connection.cursor()
    query = "SELECT id, nome, preco FROM produtos WHERE cod_barras = %s"
    cursor.execute(query, [cod_barras])

    produto = cursor.fetchone()

    if produto:
        return jsonify({'id': produto[0], 'nome': produto[1], 'preco': produto[2]})
    else:
        return jsonify({'erro': 'Produto não encontrado'}), 404

@app.route('/finalizar_venda', methods=['POST'])
def finalizar_venda():
    """
    Finaliza uma venda e registra os produtos vendidos no banco de dados.

    Esta função processa a finalização de uma venda, registrando os detalhes da transação no banco de dados:

    - Recebe os dados da venda em formato JSON do frontend, incluindo a lista de produtos vendidos e, opcionalmente, o código do cliente.
    - Calcula o total da venda somando os preços multiplicados pelas quantidades dos produtos.
    - Insere o registro da venda na tabela `vendas` e obtém o ID gerado para a venda.
    - Insere os detalhes de cada produto vendido na tabela `itens_venda`, associando-os ao ID da venda.
    - Em caso de sucesso, a transação é confirmada (commit) e retorna um JSON indicando o sucesso da operação e o ID da venda.
    - Em caso de erro, a transação é revertida (rollback), e um JSON com a mensagem de erro e status HTTP 500 é retornado.

    Returns:
        jsonify: Um JSON contendo:
            - 'sucesso': Booleano indicando se a operação foi bem-sucedida.
            - 'venda_id': O ID da venda registrada, se bem-sucedida.
            - 'erro': Uma mensagem de erro, se a operação falhou, com status HTTP 500.

    Side Effects:
        - Realiza múltiplas operações de inserção no banco de dados, incluindo registros em `vendas` e `itens_venda`.
        - Modifica o estado do banco de dados ao registrar a venda e os itens vendidos.

    Exceptions:
        - Em caso de falha, a transação é revertida e a função retorna um JSON com a descrição do erro.
        - Possíveis falhas incluem problemas de conexão com o banco de dados, falhas na execução das inserções SQL, ou erros ao processar os dados da venda.
    """
    dados_venda = request.json
    produtos = dados_venda.get('produtos')
    cliente_cod = dados_venda.get('cliente_cod')

    try:
        cursor = mysql.connection.cursor()

        total_venda = 0
        for produto in produtos:
            preco = produto['preco']
            quantidade = produto['quantidade']

            if preco is None:
                preco = 0  # Evita a multiplicação de None por um número

            total_venda += preco * quantidade

        cursor.execute(
            "INSERT INTO vendas (total, cliente_cod) VALUES (%s, %s)",
            (total_venda, cliente_cod if cliente_cod else None)
        )
        venda_id = cursor.lastrowid

        for produto in produtos:
            produto_id = produto['id']
            quantidade = produto['quantidade']
            preco = produto['preco']

            if preco is None:
                preco = 0  # Evita a inserção de None no banco de dados

            cursor.execute(
                "INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco) VALUES (%s, %s, %s, %s)",
                (venda_id, produto_id, quantidade, preco)
            )

        mysql.connection.commit()

        return jsonify({'sucesso': True, 'venda_id': venda_id})

    except Exception as e:
        mysql.connection.rollback()
        print(f"Erro ao processar a venda: {str(e)}")  # Isso imprimirá o erro detalhado
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

@app.route('/relatorios')
def relatorios():
    """
    Exibe a página de relatórios da aplicação.

    Esta função é responsável por apresentar a interface onde usuários autenticados podem visualizar e gerar relatórios sobre diversas atividades e dados no sistema.

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Renderiza a página de relatórios, fornecendo uma interface para o usuário acessar as funcionalidades de geração de relatórios.

    Returns:
        render_template: Renderiza o template `relatorios.html`, que exibe a interface de relatórios.
        redirect: Redireciona para a página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Nenhum efeito colateral direto, além do redirecionamento do usuário, se necessário.

    Exceptions:
        - Não há tratamento explícito de exceções nesta função, mas falhas na renderização do template ou problemas de sessão podem causar erros de servidor.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('relatorios.html')

@app.route('/relatorio_inventario')
def relatorio_inventario():
    """
    Gera um relatório PDF do inventário.

    Esta função permite que usuários autenticados gerem um relatório em formato PDF contendo a lista completa de produtos cadastrados no inventário:

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Recupera todos os produtos do banco de dados.
    - Renderiza os dados do inventário em um template HTML específico para o relatório.
    - Converte o HTML renderizado em um documento PDF e o retorna como resposta.

    Returns:
        PDF: Um documento PDF gerado a partir do template `relatorio_inventario.html`, contendo a lista de produtos no inventário.
        redirect: Redireciona para a página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Realiza uma consulta ao banco de dados para recuperar informações sobre os produtos.
        - Gera um PDF a partir do HTML renderizado, utilizando a função `render_pdf`.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados, falhas na renderização do template HTML, ou erros na geração do PDF. Essas exceções não são tratadas explicitamente na função.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    html = render_template('relatorio_inventario.html', produtos=produtos)
    return render_pdf(HTML(string=html))

@app.route('/relatorio_vendas', methods=['GET'])
def relatorio_vendas():
    """
    Gera um relatório PDF das vendas realizadas no sistema.

    Esta função permite que usuários autenticados gerem um relatório em formato PDF contendo a lista de vendas realizadas, possivelmente filtradas por um intervalo de datas:

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Recebe os parâmetros de data de início (`dataInicio`) e data de fim (`dataFim`) como argumentos de consulta (opcionais).
    - Se as datas forem fornecidas, filtra as vendas para incluir apenas aquelas realizadas no intervalo especificado.
    - Realiza uma consulta ao banco de dados para recuperar as vendas com base nos critérios fornecidos.
    - Renderiza os dados de vendas em um template HTML específico para o relatório.
    - Converte o HTML renderizado em um documento PDF e o retorna como resposta.

    Args:
        dataInicio (str): Data de início do filtro de vendas, no formato 'YYYY-MM-DD' (opcional).
        dataFim (str): Data de fim do filtro de vendas, no formato 'YYYY-MM-DD' (opcional).

    Returns:
        PDF: Um documento PDF gerado a partir do template `relatorio_vendas.html`, contendo a lista de vendas.
        redirect: Redireciona para a página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Realiza uma consulta ao banco de dados para recuperar informações sobre as vendas.
        - Gera um PDF a partir do HTML renderizado, utilizando a função `render_pdf`.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados, falhas na renderização do template HTML, ou erros na geração do PDF. Essas exceções não são tratadas explicitamente na função.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')

    query = "SELECT id, data_venda, total FROM vendas"
    params = []

    if data_inicio and data_fim:
        query += " WHERE data_venda BETWEEN %s AND %s"
        params.extend([data_inicio, data_fim])
    
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    vendas = cursor.fetchall()

    html = render_template('relatorio_vendas.html', vendas=vendas)
    return render_pdf(HTML(string=html))

@app.route('/relatorio_clientes')
def relatorio_clientes():
    """
    Gera um relatório PDF com a lista de clientes cadastrados no sistema.

    Esta função permite que usuários autenticados gerem um relatório em formato PDF contendo a lista completa de clientes:

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Realiza uma consulta ao banco de dados para recuperar todos os registros da tabela `clientes`.
    - Renderiza os dados dos clientes em um template HTML específico para o relatório.
    - Converte o HTML renderizado em um documento PDF e o retorna como resposta.

    Returns:
        PDF: Um documento PDF gerado a partir do template `relatorio_clientes.html`, contendo a lista de clientes cadastrados.
        redirect: Redireciona para a página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Realiza uma consulta ao banco de dados para recuperar informações sobre os clientes.
        - Gera um PDF a partir do HTML renderizado, utilizando a função `render_pdf`.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados, falhas na renderização do template HTML, ou erros na geração do PDF. Essas exceções não são tratadas explicitamente na função.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    html = render_template('relatorio_clientes.html', clientes=clientes)
    return render_pdf(HTML(string=html))

@app.route('/configs')
def configs():
    """
    Exibe a página de configurações da aplicação.

    Esta função é responsável por apresentar a interface de configurações, onde os usuários autenticados podem ajustar as preferências e configurações do sistema:

    - Verifica se o usuário está autenticado. Se não estiver, redireciona para a página de login.
    - Renderiza a página de configurações, fornecendo ao usuário acesso às diversas opções de configuração disponíveis.

    Returns:
        render_template: Renderiza o template `configs.html`, que exibe a interface de configurações.
        redirect: Redireciona para a página de login (`url_for('login')`) se o usuário não estiver autenticado.

    Side Effects:
        - Nenhum efeito colateral direto, além do redirecionamento do usuário, se necessário.

    Exceptions:
        - Não há tratamento explícito de exceções nesta função, mas falhas na renderização do template ou problemas de sessão podem causar erros de servidor.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('configs.html')

@app.route('/pagamento')
def pagamento():
    """
    Exibe a página de pagamento para uma venda específica.

    Esta função carrega os detalhes de uma venda, incluindo os itens vendidos e as informações da empresa, para exibir a página de pagamento:

    - Recebe o ID da venda como argumento de consulta (`venda_id`).
    - Verifica se o `venda_id` foi fornecido. Se não, retorna uma mensagem de erro 404.
    - Carrega as informações da venda a partir do banco de dados.
    - Carrega as informações da empresa, presumindo que a empresa tenha um ID fixo de 1.
    - Carrega os itens vendidos associados à venda especificada.
    - Renderiza a página de pagamento com os detalhes da venda, itens vendidos e informações da empresa.

    Returns:
        render_template: Renderiza o template `pagamento.html`, que exibe os detalhes da venda, os itens vendidos e as informações da empresa.
        str, int: Retorna uma mensagem de erro e o status HTTP 404 se a venda ou os dados da empresa não forem encontrados.

    Side Effects:
        - Realiza múltiplas consultas ao banco de dados para recuperar as informações da venda, itens vendidos, e os dados da empresa.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução das consultas SQL. Essas exceções não são tratadas explicitamente na função, mas resultariam em um erro do servidor.
    """
    venda_id = request.args.get('venda_id')

    if not venda_id:
        return "Venda não encontrada", 404

    cursor = mysql.connection.cursor()

    # Carrega a venda e seus itens para exibição
    cursor.execute("SELECT id, total FROM vendas WHERE id = %s", (venda_id,))
    venda = cursor.fetchone()

    cursor.execute("SELECT nome, cnpj, endereco, telefone, email FROM empresa WHERE id = 1")  # Supondo que a empresa tenha ID 1
    empresa = cursor.fetchone()

    if not empresa:
        return "Dados da empresa não encontrados", 404

    if not venda:
        return "Venda não encontrada", 404

    cursor.execute("SELECT p.nome, iv.quantidade, iv.preco FROM itens_venda iv JOIN produtos p ON iv.produto_id = p.id WHERE iv.venda_id = %s", (venda_id,))
    itens_venda = cursor.fetchall()

    return render_template('pagamento.html', venda=venda, empresa=empresa, itens_venda=itens_venda)

@app.route('/processar_pagamento', methods=['POST'])
def processar_pagamento():
    """
    Processa o pagamento de uma venda.

    Esta função recebe os dados de pagamento enviados pelo frontend e atualiza o banco de dados com as informações do pagamento para uma venda específica:

    - Recebe os dados do pagamento em formato JSON, incluindo o ID da venda (`venda_id`), código do cliente (`cliente_cod`), e a forma de pagamento (`forma_pagamento`).
    - Atualiza o registro da venda no banco de dados para incluir o código do cliente e a forma de pagamento.
    - (Opcional) Adiciona lógica adicional para processar o pagamento conforme a forma selecionada.
    - Confirma a transação (commit) se o processamento for bem-sucedido.
    - Em caso de erro, a transação é revertida (rollback) e um JSON com a mensagem de erro e status HTTP 500 é retornado.

    Returns:
        jsonify: Um JSON indicando:
            - 'sucesso': Booleano indicando se a operação foi bem-sucedida.
            - 'erro': Uma mensagem de erro, se a operação falhou, com status HTTP 500.

    Side Effects:
        - Realiza uma atualização no banco de dados para registrar as informações do pagamento.
        - Modifica o estado do banco de dados ao atualizar a venda com o código do cliente e a forma de pagamento.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados, falhas na execução da atualização SQL, ou erros ao processar os dados do pagamento. Essas exceções são tratadas revertendo a transação e retornando um JSON com a descrição do erro.
    """
    dados_pagamento = request.json
    venda_id = dados_pagamento.get('venda_id')
    cliente_cod = dados_pagamento.get('cliente_cod')
    forma_pagamento = dados_pagamento.get('forma_pagamento')

    try:
        cursor = mysql.connection.cursor()

        # Atualiza a venda com o código do cliente e a forma de pagamento, se fornecidos
        cursor.execute(
            "UPDATE vendas SET cliente_cod = %s, forma_pagamento = %s WHERE id = %s",
            (cliente_cod, forma_pagamento, venda_id)
        )
        
        # Aqui você pode adicionar lógica para processar o pagamento conforme a forma selecionada

        mysql.connection.commit()

        return jsonify({'sucesso': True})

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'sucesso': False, 'erro': str(e)}), 500

@app.route('/salvar_configuracoes', methods=['POST'])
def salvar_configuracoes():
    """
    Salva ou atualiza as configurações do sistema, como tema e cor.

    Esta função recebe os dados de configuração enviados pelo frontend e insere ou atualiza as configurações no banco de dados:

    - Recebe os dados em formato JSON, incluindo a chave da configuração (`chave`), o valor da configuração (`valor`), e a cor (`cor`).
    - Insere uma nova configuração no banco de dados ou, se a chave já existir, atualiza o valor e a cor associados.
    - Confirma a transação (commit) após a inserção ou atualização bem-sucedida.

    Returns:
        jsonify: Um JSON indicando o sucesso da operação com o status `sucesso`.

    Side Effects:
        - Realiza uma inserção ou atualização no banco de dados para armazenar ou modificar as configurações do sistema.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da inserção ou atualização SQL. Essas exceções não são tratadas explicitamente na função, mas resultariam em um erro do servidor.
    """
    dados = request.json
    chave = dados.get('chave')
    valor = dados.get('valor')
    cor = dados.get('cor')

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO configuracoes (chave, valor, cor)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE valor=%s, cor=%s
    """, (chave, valor, cor, valor, cor))
    mysql.connection.commit()

    return jsonify({'status': 'sucesso'})

@app.route('/carregar_configuracoes', methods=['GET'])
def carregar_configuracoes():
    """
    Carrega as configurações do sistema, como tema e cor.

    Esta função busca as configurações atuais do sistema no banco de dados, especificamente a configuração relacionada ao tema:

    - Realiza uma consulta no banco de dados para recuperar o valor e a cor associados à chave 'tema'.
    - Se a configuração for encontrada, retorna um JSON contendo as informações do tema.
    - Se a configuração não for encontrada, retorna um JSON com `tema` definido como `None`.

    Returns:
        jsonify: Um JSON contendo as configurações atuais do sistema:
            - 'tema': Um dicionário com as chaves 'valor' e 'cor', contendo as configurações do tema.
            - Se a configuração não existir, retorna `{'tema': None}`.

    Side Effects:
        - Realiza uma consulta ao banco de dados para recuperar as configurações do sistema.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da consulta SQL. Essas exceções não são tratadas explicitamente na função, mas resultariam em um erro do servidor.
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT chave, valor, cor FROM configuracoes WHERE chave = 'tema'")
    tema = cursor.fetchone()

    if tema:
        return jsonify({'tema': {'valor': tema[1], 'cor': tema[2]}})
    else:
        return jsonify({'tema': None})

@app.route('/resetar_configuracoes', methods=['POST'])
def resetar_configuracoes():
    """
    Reseta as configurações do sistema para os valores padrão.

    Esta função redefine as configurações do sistema, especificamente o tema, para os valores padrão:

    - Atualiza a configuração com a chave 'tema' no banco de dados, definindo o valor para 'claro' e a cor para '#4CAF50'.
    - Confirma a transação (commit) após a atualização bem-sucedida.

    Returns:
        jsonify: Um JSON indicando o sucesso da operação com o status `sucesso`.

    Side Effects:
        - Realiza uma atualização no banco de dados, modificando a configuração do tema para seus valores padrão.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da atualização SQL. Essas exceções não são tratadas explicitamente na função, mas resultariam em um erro do servidor.
    """
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE configuracoes SET valor = 'claro', cor = '#4CAF50' WHERE chave = 'tema'")
    mysql.connection.commit()
    return jsonify({'status': 'sucesso'})

@app.route('/salvar_empresa', methods=['POST'])
def salvar_empresa():
    """
    Salva ou atualiza as informações da empresa no banco de dados.

    Esta função recebe os dados da empresa enviados pelo frontend e realiza uma inserção ou atualização das informações no banco de dados:

    - Recebe os dados em formato JSON, incluindo nome, CNPJ, endereço, telefone e email da empresa.
    - Insere um novo registro na tabela `empresa` ou, se um registro com o mesmo CNPJ já existir, atualiza as informações do registro existente.
    - Confirma a transação (commit) após a inserção ou atualização bem-sucedida.

    Returns:
        jsonify: Um JSON indicando o sucesso da operação com o status `sucesso`.

    Side Effects:
        - Realiza uma inserção ou atualização no banco de dados para armazenar ou modificar as informações da empresa.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da inserção ou atualização SQL. Essas exceções não são tratadas explicitamente na função, mas resultariam em um erro do servidor.
    """
    dados = request.json
    nome = dados.get('nome')
    cnpj = dados.get('cnpj')
    endereco = dados.get('endereco')
    telefone = dados.get('telefone')
    email = dados.get('email')

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO empresa (nome, cnpj, endereco, telefone, email)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE nome=%s, cnpj=%s, endereco=%s, telefone=%s, email=%s
    """, (nome, cnpj, endereco, telefone, email, nome, cnpj, endereco, telefone, email))
    mysql.connection.commit()

    return jsonify({'status': 'sucesso'})

@app.route('/carregar_empresa', methods=['GET'])
def carregar_empresa():
    """
    Carrega as informações da empresa do banco de dados.

    Esta função recupera as informações da empresa, como nome, CNPJ, endereço, telefone e email, e as retorna em formato JSON:

    - Realiza uma consulta ao banco de dados para obter o registro da empresa.
    - Se os dados da empresa forem encontrados, retorna um JSON contendo as informações da empresa.
    - Se nenhum dado for encontrado, retorna um JSON com valor `None`.

    Returns:
        jsonify: Um JSON contendo as informações da empresa:
            - 'nome': Nome da empresa.
            - 'cnpj': CNPJ da empresa.
            - 'endereco': Endereço da empresa.
            - 'telefone': Telefone da empresa.
            - 'email': Email da empresa.
            - Se nenhum dado for encontrado, retorna `None`.

    Side Effects:
        - Realiza uma consulta ao banco de dados para recuperar as informações da empresa.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados ou falhas na execução da consulta SQL. Essas exceções não são tratadas explicitamente na função, mas resultariam em um erro do servidor.
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nome, cnpj, endereco, telefone, email FROM empresa LIMIT 1")
    empresa = cursor.fetchone()

    if empresa:
        return jsonify({
            'nome': empresa[0],
            'cnpj': empresa[1],
            'endereco': empresa[2],
            'telefone': empresa[3],
            'email': empresa[4]
        })
    else:
        return jsonify(None)

@app.route('/fazer_backup', methods=['POST'])
def fazer_backup():
    """
    Realiza o backup do banco de dados do sistema.

    Esta função cria um arquivo de backup do banco de dados atual, usando o comando `mysqldump`, e o armazena em um diretório designado para backups com um nome de arquivo que inclui um timestamp:

    - Verifica se o diretório de backups existe; caso contrário, cria-o.
    - Gera um nome de arquivo de backup que inclui a data e a hora atuais no formato `YYYYMMDDHHMMSS`.
    - Executa o comando `mysqldump` para gerar o backup do banco de dados e salvar o arquivo no diretório de backups.
    - Verifica se o arquivo de backup foi criado com sucesso.
    - Retorna um JSON indicando o sucesso da operação e o caminho do arquivo de backup.
    - Em caso de erro, retorna um JSON com uma mensagem de erro.

    Returns:
        jsonify: Um JSON indicando o sucesso ou falha da operação:
            - 'status': Indica se a operação foi bem-sucedida ('sucesso') ou se houve uma falha ('erro').
            - 'arquivo': O caminho do arquivo de backup, se a operação foi bem-sucedida.
            - 'mensagem': Uma mensagem de erro, se a operação falhou.

    Side Effects:
        - Cria um diretório de backups se ele não existir.
        - Gera um arquivo de backup no sistema de arquivos.

    Exceptions:
        - Possíveis falhas incluem problemas na execução do comando `mysqldump`, erros ao criar diretórios ou manipular arquivos, ou outras exceções não tratadas explicitamente na função. Essas exceções resultam em um JSON de erro sendo retornado.
    """
    try:
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        backup_file = os.path.join(backup_dir, f'backup_{time.strftime("%Y%m%d%H%M%S")}.sql')

        command = f'mysqldump -u {app.config["MYSQL_USER"]} -p{app.config["MYSQL_PASSWORD"]} {app.config["MYSQL_DB"]} > {backup_file}'
        os.system(command)

        if os.path.exists(backup_file):
            return jsonify({'status': 'sucesso', 'arquivo': backup_file})
        else:
            return jsonify({'status': 'erro', 'mensagem': 'Falha ao criar o arquivo de backup.'})
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)})

@app.route('/gerar_qrcode_pix_old', methods=['GET'])
def gerar_qrcode_pix_old():
    """
    Gera um código QR Pix para o pagamento de uma venda específica.

    Esta função recebe o ID de uma venda como parâmetro de consulta, busca as informações da venda no banco de dados, e gera um código QR Pix EMV conforme os dados da transação.

    - Verifica se o ID da venda foi fornecido. Se não, retorna um erro 400.
    - Busca o valor total da venda no banco de dados com base no ID fornecido.
    - Se a venda não for encontrada, retorna um erro 404.
    - Gera o código QR Pix usando os dados da venda, incluindo a chave Pix, a descrição, o nome do recebedor, a cidade, e um identificador único da transação (TXID).
    - Formata o valor corretamente para ser utilizado na transação.
    - Monta o código EMV Pix de acordo com as especificações e adiciona o CRC16 para validação.
    - Retorna o código QR Pix gerado em formato JSON.

    Returns:
        jsonify: Um JSON indicando:
            - 'status': 'sucesso' se o código QR foi gerado com sucesso, ou 'erro' se ocorreu um problema.
            - 'qrcode': O código EMV Pix gerado se a operação for bem-sucedida.
            - 'mensagem': Uma mensagem de erro detalhada se a operação falhar.

    Side Effects:
        - Realiza uma consulta ao banco de dados para recuperar o valor da venda.
        - Gera e retorna um código QR Pix para o pagamento.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados, erros ao acessar os dados da venda, ou erros ao gerar o código EMV Pix. Essas exceções são tratadas e resultam em uma resposta de erro JSON.
    """
    venda_id = request.args.get('venda_id')
    
    if not venda_id:
        print("Erro: ID da venda não fornecido.")
        return jsonify({'status': 'erro', 'mensagem': 'ID da venda não fornecido'}), 400

    try:
        # Obter informações da venda no banco de dados
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT total FROM vendas WHERE id = %s", (venda_id,))
        venda = cursor.fetchone()
        
        if not venda:
            print(f"Erro: Venda com ID {venda_id} não encontrada.")
            return jsonify({'status': 'erro', 'mensagem': 'Venda não encontrada'}), 404

        valor = venda[0]
        print(f"Valor da venda: {valor}")
        
        chave_pix = "f8b9c7cd-7262-4e50-a07a-0f7db1caaa17"  # Coloque aqui a sua chave Pix
        descricao = f"Pagamento da venda {venda_id}"
        cidade = "SAO PAULO"
        nome_recebedor = "ERPFLASK"
        identificador = f"TXID{venda_id}"  # Um identificador único para a transação

        # Garantir que a cidade tenha exatamente 11 caracteres (incluindo os dígitos que indicam o tamanho)
        cidade = cidade[:9].ljust(9)  # Ajusta para que tenha exatamente 9 caracteres
        cidade_length = len(cidade)
        cidade_emv = f"{cidade_length:02d}{cidade}"

        # Configurar o Pix
        pix = Pix()
        pix.set_merchant_name(nome_recebedor)
        pix.set_merchant_city(cidade)
        pix.set_pixkey(chave_pix)

        # Ajustando o valor para remover as casas decimais extras se o valor for inteiro
        valor_formatado = "{:.2f}".format(valor).rstrip('0').rstrip('.')
        pix.set_amount(valor_formatado)

        pix.set_description(descricao)
        pix.set_txid(identificador)

        # Geração manual da Merchant Account Information (MAI)
        mai = pix.get_value("00", "br.gov.bcb.pix") + \
                pix.get_value("01", chave_pix) + \
                (pix.get_value("02", descricao) if descricao else "")

        # Gerar o código EMV Pix completo
        emv_pix = (
            pix.get_value("00", "01") +  # Payload Format Indicator
            pix.get_value("26", mai) +  # Merchant Account Information
            pix.get_value("52", "0000") +  # Merchant Category Code
            pix.get_value("53", "986") +  # Transaction Currency (BRL)
            pix.get_value("54", valor_formatado) +  # Transaction Amount formatado
            pix.get_value("58", "BR") +  # Country Code
            pix.get_value("59", nome_recebedor) +  # Merchant Name
            pix.get_value("60", cidade) +  # Merchant City directly without length prefix
            pix.get_value("62", pix.get_value("05", identificador))  # Correct Additional Data Field Template (TXID)
        )
        emv_pix += pix.get_crc16(emv_pix)  # Adiciona o CRC16 ao final

        print(f"EMV Pix: {emv_pix}")

        return jsonify({'status': 'sucesso', 'qrcode': emv_pix})

    except Exception as e:
        print(f"Erro ao gerar QR Code Pix: {str(e)}")
        return jsonify({'status': 'erro', 'mensagem': 'Erro ao gerar QR Code Pix'}), 500

# geração do pix via mercado pago
@app.route('/gerar_qrcode_pix', methods=['GET'])
def gerar_qrcode_pix():
    venda_id = request.args.get('venda_id')
    
    if not venda_id:
        print("Erro: ID da venda não fornecido.")
        return jsonify({'status': 'erro', 'mensagem': 'ID da venda não fornecido'}), 400

    try:
        # Obter informações da venda no banco de dados
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT total FROM vendas WHERE id = %s", (venda_id,))
        venda = cursor.fetchone()
        
        if not venda:
            print(f"Erro: Venda com ID {venda_id} não encontrada.")
            return jsonify({'status': 'erro', 'mensagem': 'Venda não encontrada'}), 404

        valor = venda[0]
        print(f"Valor da venda: {valor}")
        
        descricao = f"Pagamento da venda {venda_id}"

        # Cria o pagamento via Mercado Pago
        payment_data = {
            "transaction_amount": float(valor),
            "description": descricao,
            "payment_method_id": "pix",
            "payer": {
                "email": "test_user@test.com",  # Pode ser um email de teste ou do cliente real
                "first_name": "Test",
                "last_name": "User",
                "identification": {
                    "type": "CPF",
                    "number": "19119119100"  # Pode ser um CPF de teste ou do cliente real
                }
            }
        }

        print("Enviando dados para o Mercado Pago...")
        payment = sdk.payment().create(payment_data)
        payment_response = payment["response"]

        print(f"Resposta do Mercado Pago: {payment_response}")

        # Verifica se o QR code foi gerado com sucesso
        if "qr_code" in payment_response["point_of_interaction"]["transaction_data"]:
            print("QR Code gerado com sucesso")
            return jsonify({'status': 'sucesso', 'qrcode': payment_response["point_of_interaction"]["transaction_data"]["qr_code"]})
        else:
            print(f"Erro ao processar pagamento: {payment_response.get('status_detail')}")
            return jsonify({'status': 'erro', 'mensagem': payment_response.get('status_detail', 'Erro ao processar pagamento')}), 500

    except Exception as e:
        print(f"Erro ao gerar QR Code Pix: {str(e)}")
        return jsonify({'status': 'erro', 'mensagem': 'Erro ao gerar QR Code Pix'}), 500

@app.route('/gerar_recibo', methods=['GET'])
def gerar_recibo():
    """
    Gera os dados necessários para a criação de um recibo de venda.

    Esta função recebe o ID de uma venda e a forma de pagamento como parâmetros de consulta, busca as informações da venda e da empresa no banco de dados, e retorna os dados estruturados em formato JSON para gerar um recibo:

    - Verifica se o ID da venda foi fornecido. Se não, retorna um erro 400.
    - Realiza uma consulta no banco de dados para obter o valor total e a data da venda com base no ID fornecido.
    - Se a venda não for encontrada, retorna um erro 404.
    - Realiza uma consulta no banco de dados para obter as informações da empresa (nome, endereço e CNPJ).
    - Se os dados da empresa não forem encontrados, retorna um erro 404.
    - Retorna os dados necessários para o recibo, incluindo o total da venda, a forma de pagamento, e as informações da empresa, em formato JSON.

    Returns:
        jsonify: Um JSON contendo:
            - 'status': 'sucesso' se os dados do recibo foram recuperados com sucesso, ou 'erro' se ocorreu um problema.
            - 'total': O valor total da venda.
            - 'forma_pagamento': A forma de pagamento utilizada na venda.
            - 'empresa': Um dicionário contendo as informações da empresa (nome, endereço, CNPJ).
            - 'mensagem': Uma mensagem de erro detalhada se a operação falhar.
            - 'detalhes': Detalhes técnicos do erro, se houver uma exceção.

    Side Effects:
        - Realiza consultas ao banco de dados para recuperar os detalhes da venda e da empresa.

    Exceptions:
        - Possíveis falhas incluem problemas de conexão com o banco de dados, erros ao acessar os dados da venda ou da empresa. Essas exceções são tratadas e resultam em uma resposta de erro JSON.
    """
    venda_id = request.args.get('venda_id')
    forma_pagamento = request.args.get('forma_pagamento')
    
    if not venda_id:
        return jsonify({'status': 'erro', 'mensagem': 'ID da venda não fornecido'}), 400

    try:
        cursor = mysql.connection.cursor()
        # Ajuste a consulta SQL para refletir as colunas corretas
        cursor.execute("SELECT total, data_venda FROM vendas WHERE id = %s", (venda_id,))
        venda = cursor.fetchone()
        
        if not venda:
            return jsonify({'status': 'erro', 'mensagem': 'Venda não encontrada'}), 404

        cursor.execute("SELECT nome, endereco, cnpj FROM empresa LIMIT 1")
        empresa = cursor.fetchone()
        
        if not empresa:
            return jsonify({'status': 'erro', 'mensagem': 'Dados da empresa não encontrados'}), 404

        # Retornar os dados necessários para o recibo
        return jsonify({
            'status': 'sucesso',
            'total': venda[0],
            'forma_pagamento': forma_pagamento,
            'empresa': {
                'nome': empresa[0],
                'endereco': empresa[1],
                'cnpj': empresa[2]
            }
        })

    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': 'Erro ao gerar recibo', 'detalhes': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)