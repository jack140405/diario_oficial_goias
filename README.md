Sobre o Projeto

O Diário Oficial Goiás é um sistema desenvolvido para automatizar a busca e filtragem de publicações no site oficial do Diário Oficial de Goiás.
Ele permite:

Buscar automaticamente as edições mais recentes do Diário Oficial.
Procurar por palavras-chave específicas dentro do conteúdo em PDF.
Enviar automaticamente as páginas filtradas por e-mail para o destinatário configurado.
Após o envio, todos os arquivos gerados são removidos automaticamente para manter o projeto limpo.

Tecnologias Utilizadas

Backend:
Python 3.12+
Flask
PyMuPDF (fitz)
Selenium
Requests
SMTP Email (Envio Automático)

Frontend:
React
Vite
Axios
Material UI (opcional para interface)

Estrutura do Projeto

diario_oficial_goias/
│
├── backend/
│   ├── app.py                # Flask API principal
│   ├── core/
|   |   ├── pdf_utils.py      # Extrai, salva e busca de palavras
│   │   ├── email_utils.py    # Funções de envio de e-mail (SMTP)
│   │   ├── downloader.py      # Funções de download 
│   │   └── config.py         # Configurações de ambiente (SMTP, paths)
│   ├── .venv/                # Ambiente virtual Python
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── FormBusca.jsx # Formulário principal de busca
│   │   └── main.jsx          # Inicialização do React
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
├── README.md
└── requirements.txt

 Como Executar o Projeto

 1. Clone o repositório
git clone https://github.com/jack140405/diario_oficial_goias.git
cd diario_oficial_goias

 2. Configurar o Backend (Flask)
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt


Crie um arquivo .env dentro da pasta backend/ com as variáveis de ambiente:

# Configurações SMTP (pode usar Gmail, Outlook, etc.)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=seu_email@gmail.com
SMTP_PASS=sua_senha_de_app
SIMULATE_EMAILS=false


Depois, execute o backend:

python app.py


O servidor Flask será iniciado em:

 http://127.0.0.1:5000

 3. Configurar o Frontend (React)
cd ../frontend
npm install
npm run dev


O frontend rodará em:

 http://localhost:5173

 Funcionalidades Principais
 Função	Descrição
 Busca automática	         Faz scraping do site oficial e identifica as últimas edições publicadas.
 Filtragem inteligente	  Extrai as páginas que contêm a palavra-chave buscada.
 Envio por e-mail	         Envia os arquivos PDF filtrados para o e-mail configurado.
 Limpeza automática	     Remove todos os PDFs baixados após o envio.

 Requisitos:

Python 3.12+

Node.js 18+

Google Chrome instalado (para o Selenium)

Git
