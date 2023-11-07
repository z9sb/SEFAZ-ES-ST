import imaplib
import email
from email.header import decode_header
from main import main
from datetime import datetime

#diretório para download
root_dir = r"C:\\Users\\raysl_3a68bgu\\OneDrive\\Documentos\\Python\\outlook\\Arquivos\\"

# Configurações do servidor IMAP do Outlook.com
username = "contabilidadebento.xml@hotmail.com"
password = "xml1266@"
server = "imap-mail.outlook.com"

# Conectando-se ao servidor IMAP
mail = imaplib.IMAP4_SSL(server)
mail.login(username, password)

# Selecionando a caixa de entrada
mail.select("inbox")

# Pesquisando emails com anexos
status, messages = mail.search(None, "ALL")
messages = list(reversed(messages[0].split()))

for mail_id in messages:
    _, msg_parts = mail.fetch(mail_id, "(RFC822)")
    msg = email.message_from_bytes(msg_parts[0][1])
    subject, encoding = decode_header(msg["Subject"])[0]
    print(encoding)
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")
    from_ = msg.get("From")
    date = msg.get("Date")

    print(f"Subject: {subject}")
    print(f"From: {from_}")
    print(f"Date: {date}")
    if 'UTC' in date:
        date_email = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z (UTC)")
    else:
        date_email = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
    
    if date_email.month != datetime.now().month:
        break
    
    # Verificando anexos
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue

        filename = part.get_filename()
        if filename:
            print(f"Anexo: {filename}")
            try:
                with open(f"{root_dir}{filename}", "wb") as f:
                    f.write(part.get_payload(decode=True))
            except:
                pass
# Fechando a conexão
mail.close()
mail.logout()
main(root_dir)