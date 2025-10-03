import os
import base64
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")


def enviar_email(destinatario, assunto, conteudo_html, arquivo_pdf=None, filename=None):
    """
    Envia um e-mail com ou sem anexo (PDF).
    
    :param destinatario: E-mail de destino
    :param assunto: Assunto do e-mail
    :param conteudo_html: Corpo do e-mail em HTML
    :param arquivo_pdf: Caminho do PDF a ser anexado
    :param filename: Nome do arquivo PDF
    :return: True se enviado com sucesso, False caso contrário
    """
    try:
        message = Mail(
            from_email=EMAIL_SENDER,
            to_emails=destinatario,
            subject=assunto,
            html_content=conteudo_html
        )

        if arquivo_pdf and filename:
            with open(arquivo_pdf, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                attachment = Attachment(
                    FileContent(encoded),
                    FileName(filename),
                    FileType("application/pdf"),
                    Disposition("attachment")
                )
                message.attachment = attachment

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"📧 Email enviado para {destinatario} (status {response.status_code})")
        return True

    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        return False
