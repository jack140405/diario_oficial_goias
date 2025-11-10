import os
from dotenv import load_dotenv

# Carrega o arquivo .env automaticamente
load_dotenv()

# Variáveis do SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM = os.getenv("SENDGRID_FROM", "no-reply@example.com")

# Controle se o navegador roda visível ou oculto
HEADLESS = os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")
