# Meu Projeto

Este projeto utiliza SQLite3 e um bot do Telegram para realizar consultas diversas, como CPF, CEP, nome, telefone, entre outras. 

### Problemas Conhecidos Corrigidos

- A adição de novos IDs requer reinicialização do servidor para reconhecimento imediato.

## Configuração

### Alterar o Token do Bot do Telegram

Para alterar o token do bot do Telegram, edite o arquivo `main.py` e substitua o valor do token pelo novo token fornecido.

### Inicialização do Projeto

Para iniciar o projeto, siga os passos abaixo:

1. **Instale as dependências necessárias**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Crie e inicialize o banco de dados**:
    ```bash
    python initialize_db.py
    ```

3. **Execute o projeto**:
    ```bash
    python main.py
    ```

## Funcionalidades

O bot do Telegram oferece as seguintes funcionalidades:

- `/start`: Inicia a interação com o bot e verifica se o usuário está autorizado.
- `/cpf <número do CPF>`: Consulta informações baseadas no número do CPF.
- `/cep <número do CEP>`: Consulta informações baseadas no número do CEP.
- `/mae <nome completo>`: Consulta informações baseadas no nome da mãe.
- `/nome <nome completo>`: Consulta informações baseadas no nome completo.
- `/email <endereço de email>`: Consulta informações baseadas no endereço de email.
- `/telefone <número do telefone>`: Consulta informações baseadas no número do telefone.
- `/addid <ID do usuário>`: Adiciona um novo usuário autorizado (comando restrito ao administrador).

## Changelog

### Alterações Recentes

#### Atualização de `db.py`

- **Função `init_db`**: Inicializa o banco de dados criando as tabelas `authorized_users` e `user_usage`.
- **Função `load_backup`**: Carrega os dados do banco de dados SQLite.
- **Função `save_backup`**: Salva os dados no banco de dados SQLite.
- **Função `reset_daily_usage`**: Reseta o uso diário dos usuários.

#### Atualização de `addid.py`

- Adiciona novos IDs ao banco de dados em tempo real e salva o backup.

#### Atualização de `polling.py`

- Implementa a verificação periódica de atualizações do banco de dados.

#### Atualização de `main.py`

- Configura o bot para rodar com polling e inicializa o agendador de tarefas diárias.

#### Atualização de `cpf.py`, `cep.py`, `email.py`, `nome.py`, `mae.py`, `telefone.py`

- Verifica a autorização do usuário e o uso diário.
- Consulta a API correspondente e retorna as informações formatadas.
- Salva os dados em cache e envia os resultados ao usuário e ao administrador.
- Implementa a limpeza periódica de arquivos de cache antigos.

#### Atualização de `start.py`

- Verifica se o ID do usuário está no banco de dados e envia uma mensagem de boas-vindas ou instruções de cadastro conforme o caso.

## Estrutura do Projeto

```plaintext
BotPRJ/
├── func/
│   ├── start.py
│   ├── addid.py
│   ├── cpf.py
│   ├── cep.py
│   ├── email.py
│   ├── nome.py
│   ├── mae.py
│   ├── telefone.py
├── mini_db.db
├── db.py
├── initialize_db.py
├── main.py
├── polling.py
├── README.md
└── requirements.txt
