# Monitoramento de Ativos B3

Sistema web para monitoramento de ativos da B3 com envio de alertas por email quando os preços atingem valores mínimos ou máximos definidos pelo usuário.

## 🚀 Funcionalidades

- Cadastro e autenticação de usuários
- Busca e cadastro de ativos da B3 para monitoramento
- Definição de valores mínimos e máximos para cada ativo
- Configuração do período de checagem dos preços
- Envio automático de emails quando os limites são atingidos
- Visualização de gráficos históricos dos preços
- Interface responsiva e amigável

## 🛠️ Tecnologias Utilizadas

- Python 3.8+
- Django 5.1.2
- Django REST Framework
- JWT para autenticação
- MySQL
- Bootstrap 5
- Select2 para busca de ativos
- yfinance para dados da B3
- Matplotlib para geração de gráficos

## ⚙️ Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/marques203/monitoramento_ativos_B3.git
```
2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate
```
3. Instale as dependências:

```bash
pip install -r requirements.txt
```
4. Configure as variáveis de ambiente no arquivo `.env`:

```
SECRET_KEY=sua_chave_secreta
DB_NAME=nome_do_banco_de_dados
DB_USER=nome_do_usuario_do_banco_de_dados
DB_PASSWORD=senha_do_usuario_do_banco_de_dados
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_email
DEFAULT_FROM_EMAIL=seu_email@gmail.com
```

5. Execute as migrações:

```bash
python manage.py migrate
```
6. Inicie o servidor:

```bash
python manage.py runserver
```

## 📱 Telas do Sistema

### Página Inicial
- Login e cadastro de usuários
- Informações sobre o projeto
- Dados de contato

### Dashboard de Monitoramento
- Lista de ativos cadastrados
- Formulário para adicionar novos ativos
- Gráficos históricos de preços
- Controles para iniciar/parar monitoramento

## 🔒 Segurança

- Autenticação via JWT
- Senhas criptografadas
- Proteção CSRF
- Validação de dados de entrada

## 📧 Sistema de Alertas

O sistema verifica periodicamente os preços dos ativos cadastrados usando a API do Yahoo Finance (yfinance). Quando um preço atinge os limites configurados, um email é enviado automaticamente para o usuário contendo:

- Nome do ativo
- Preço atual
- Limite atingido (máximo ou mínimo)
- Data e hora do evento

## 📊 Visualização de Dados

- Gráficos interativos usando Matplotlib
- Histórico de 30 dias de preços
- Indicadores visuais dos limites configurados
- Atualização em tempo real