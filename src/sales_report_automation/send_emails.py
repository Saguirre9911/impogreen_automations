import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def send_email(to_address, subject, body, attachment_path):

    from_address = os.getenv("EMAIL_USER")
    from_password = os.getenv("EMAIL_PASSWORD")  # Usa la contraseña de aplicación aquí

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with open(attachment_path, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name=attachment_path)
        part["Content-Disposition"] = f'attachment; filename="{attachment_path}"'
        msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(from_address, from_password)
        server.sendmail(from_address, to_address, msg.as_string())


def send_emails_to_all():
    unifided_data = pd.read_excel("unifided_data.xlsx")
    for index, row in unifided_data.iterrows():
        email = row["EMAIL"]
        employee_name = row["EMPLEADO"]
        pdf_path = f"{employee_name}.pdf"
        subject = f"Tu recibo de nómina {employee_name} - IMPORTADORA Y DISTRIBUIDORA GREEN SAS"
        body = (
            body
        ) = f"""
Hola {employee_name}!

Te adjuntamos tu planilla digital correspondiente al periodo de nómina.

Nota: Esta notificación se envió desde una dirección que no puede recibir correos electrónicos. Por favor no respondas este correo. ¡Gracias!

Saludos cordiales!

Disclaimer: Este mensaje y los archivos adjuntos al mismo pueden contener información privilegiada o confidencial para uso exclusivo de su destinatario. Cualquier uso no autorizado expresamente queda prohibido y puede ser ilegal. Si usted no es el destinatario o bien si usted ha recibido esta comunicación por error, favor de notificar al remitente y borrar el presente mensaje. Los Datos Personales en nuestra posesión se encuentran protegidos y se tratan de conformidad con las legislaciones y regulaciones aplicables y nuestro Aviso de Privacidad. Únicamente la persona autorizada por Impogreen SAS / Importadora y distribuidora green SAS podrá garantizar que la información aquí contenida – y la interpretación de esta misma – sea aplicable o apropiada a su situación particular.
"""
        send_email(email, subject, body, pdf_path)
        print(f"Email sent to {email} with attachment {pdf_path}")


if __name__ == "__main__":
    send_emails_to_all()
