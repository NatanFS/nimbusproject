# Projeto Geração de Relatório de Meteorologia

Este projeto é uma aplicação para gerar e enviar relatórios meteorológicos baseados em dados fornecidos em diferentes formatos (JSON, CSV, TXT). Utiliza FastAPI para gerenciamento de endpoints e SQLAlchemy para manipulação do banco de dados.

## Funcionalidades

- Recepção de dados meteorológicos via TCP
- Armazenamento de dados de clientes e relatórios meteorológicos no banco de dados
- Geração de relatórios meteorológicos em formato PDF
- Envio de relatórios por e-mail
- Suporte para arquivos de dados nos formatos JSON, CSV e TXT

## Tecnologias Utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- ReportLab
- smtplib
- dotenv

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/NatanFS/nimbusproject.git
    cd nimbusproject
    ```

2. Crie um ambiente virtual e ative-o:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows, use 'venv\\Scripts\\activate'
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

    Caso ocorra algum erro, atualize o pip com o seguinte comando:

    ```bash
    pip install --upgrade pip
    ```

4. Configure as variáveis de ambiente. Seguindo o exemplo do arquivo `.env.example`, crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

    ```env
    DATABASE_URL="sqlite:///./test.db"
    EMAIL_HOST_USER="seu_email@example.com"
    EMAIL_HOST_PASSWORD="sua_senha"
    SMTP_EMAIL_HOST="smtp.example.com"
    SMTP_EMAIL_PORT="587"
    ```

    Para facilitar os testes, preparei um e-mail dedicado somente a esse projeto para realizar os envios. Pode usar as seguintes credenciais:

    E-mail: nimbusproject504@gmail.com
    Senha: lmnl ijta ixal osyo

    Este e-mail será desativado em alguns dias. 

## Execução

### Inicializar o Servidor FastAPI

Para iniciar o servidor FastAPI:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Inicializar o Servidor TCP

O servidor TCP será inicializado automaticamente na porta 5784, junto com o servidor FastAPI.

### Cadastro de Clientes via TCP 

Para cadastrar clientes via TCP, siga o exemplo de comando: 

```bash
echo "joao,email@gmail.com,84999999999,25" | nc 127.0.0.1 5784  
```

A string deve seguir o padrão "Nome,email,telefone,idade".

### Geração de relatórios

Os relatórios são salvos localmente na pasta reports/, na raíz do projeto, criada após a execução do script. Cada relatório segue o formato `report_TELEFONE.pdf`. 

Para testar a geração dos relatórios, adicionei três aquivos `raw.json`, `raw.txt` e `raw.csv` que podem ser utilizados como fonte de dados. Também há o `report-example.pdf`, um exemplo de relatório já gerado.

Para gerar e enviar relatórios, utilize o script `app/send_reports_script.py``. Exemplo de uso:

```bash
python app/send_reports_script.py --phones "84999139194,84999139195" --date "2024-01-01T12:00" --raw "path/to/raw.json" --send_email
```

Caso não deseje enviar o relatório por e-mail, remova a flag `--send_email`.

## Logs das aplicações

O logs do servidor TCP e da geração de relatórios estão sendo salvos nos arquivos `app.log` e `report.log`, respectivamente. Eles serão gerados após a execução do projeto.  
