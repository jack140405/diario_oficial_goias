import os
from dotenv import load_dotenv

# Carrega o arquivo .env automaticamente
load_dotenv()


# Controle se o navegador roda visível ou oculto
HEADLESS = os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")
