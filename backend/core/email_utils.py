import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import logging

# Carregar .env
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
SIMULATE_EMAILS = os.getenv("SIMULATE_EMAILS", "true").lower() in ("1", "true", "yes")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("email_utils")


def enviar_arquivos_por_smtp(destinatario: str, assunto: str, corpo: str, anexos: list[str]) -> bool:
    """
    Envia e-mails via SMTP com anexos.
    - Usa as variáveis do .env
    - Se SIMULATE_EMAILS=True, apenas imprime o que enviaria
    """
    if SIMULATE_EMAILS:
        logger.info("[SIMULAÇÃO] Enviando e-mail para %s com anexos: %s", destinatario, anexos)
        return True

    if not all([SMTP_SERVER, SMTP_USER, SMTP_PASSWORD]):
        logger.error("❌ Configurações SMTP ausentes. Verifique seu .env.")
        return False

    try:
        msg = EmailMessage()
        msg["From"] = SMTP_FROM
        msg["To"] = destinatario
        msg["Subject"] = assunto
        msg.set_content(corpo)

        # Adicionar anexos
        for caminho in anexos or []:
            try:
                with open(caminho, "rb") as f:
                    dados = f.read()
                    msg.add_attachment(
                        dados,
                        maintype="application",
                        subtype="pdf",
                        filename=os.path.basename(caminho),
                    )
            except Exception as e:
                logger.warning(f"⚠️ Erro ao anexar {caminho}: {e}")

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls(context=context)
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.send_message(msg)

        logger.info("📨 Mensagem enviada para o servidor SMTP (entregue).")
        return True

    except Exception as e:
        logger.exception("❌ Erro ao enviar e-mail via SMTP: %s", e)
        return False
