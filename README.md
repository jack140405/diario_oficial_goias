# 📄 Diário Oficial de Goiás - Busca e Envio Automático

Sistema automatizado para baixar edições do Diário Oficial de Goiás, filtrar por palavra-chave e enviar os resultados por e-mail com anexos PDF.

## 🧰 Tecnologias
- Python (Flask)
- React (Vite)
- SMTP / Email
- Selenium + PyMuPDF


## 🚀 Como rodar localmente
```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py

## 🌐 Frontend
cd frontend
npm install
npm run dev
