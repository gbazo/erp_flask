# MINI ERP

## Descrição

O MINI ERP é um sistema de gestão simples e eficiente desenvolvido para pequenas e médias empresas. Ele permite gerenciar o inventário, vendas, clientes, e mais, tudo em uma interface amigável e intuitiva.

## Funcionalidades

### 1. **Gestão de Inventário**
   - Adição, edição e exclusão de produtos no inventário.
   - Visualização de todos os produtos em uma tabela organizada.
   - Controle de estoque com a possibilidade de ajustes manuais.
   - Geração de relatórios em PDF do inventário.

### 2. **Gestão de Vendas**
   - Interface de Ponto de Venda (PDV) para vendas rápidas e fáceis.
   - Suporte para vendas com código de barras.
   - Opção de vendas identificadas (clientes) ou vendas rápidas (sem identificação).
   - Registro de todas as vendas no sistema, com detalhes de produtos e quantidades.

### 3. **Gestão de Clientes**
   - Cadastro, edição e exclusão de clientes.
   - Visualização de todos os clientes em uma tabela organizada.
   - Armazenamento de informações importantes, como nome, CNPJ, endereço, telefone e e-mail.

### 4. **Configurações do Sistema**
   - **Configurações de Tema**: Personalize a aparência do sistema com temas claros e escuros, além de escolher cores específicas.
   - **Cadastro de Empresa**: Armazene e gerencie as informações da empresa, como nome, CNPJ, endereço, telefone e e-mail, diretamente no sistema.
   - **Backup Manual**: Realize backups manuais do banco de dados diretamente pelo sistema, garantindo a segurança dos dados.

### 5. **Segurança**
   - Autenticação de usuários com login e senha.
   - Diferentes níveis de acesso (em desenvolvimento).
   - Criptografia de senhas no banco de dados utilizando bcrypt.

### 6. **Relatórios**
   - Geração de relatórios em PDF de inventário, vendas e clientes.
   - Filtros avançados para geração de relatórios personalizados.

### 7. **Funcionalidades Futuras**
   - **Gestão de Usuários e Permissões**: Controle detalhado sobre o que cada usuário pode acessar e modificar.
   - **Programas de Fidelidade**: Sistema de pontos para clientes.
   - **Integração com Sistemas de Pagamento**: Automatização de transações online.
   - **Backup Automático**: Implementação de backups automáticos em intervalos regulares.
   - **Gestão de Estoque Avançada**: Alertas de reposição, controle de lotes e validade.

## Requisitos

- Python 3.x
- Flask
- MySQL
- Flask-MySQLdb
- Flask-WeasyPrint
- Bcrypt

## Licença

Este projeto está licenciado sob a Licença Creative Commons Attribution-NonCommercial 4.0 International. Isso significa que você pode usar, compartilhar e adaptar o material para fins não comerciais, desde que atribua o crédito apropriado ao autor original.
