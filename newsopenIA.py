import os
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define a chave da API da OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_response_from_openai():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Ou "gpt-4" se você tiver acesso
            messages=[
                {"role": "system", "content": "Me dê um resumo das 10 principais notícias de tecnologia."}
            ],
            temperature=0.7,  # Ajuste conforme necessário
            max_tokens=150
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Erro ao obter resposta da OpenAI: {e}")
        return "Não foi possível obter uma resposta da IA."

def send_email(news):
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    # Configuração do assunto e corpo do email
    subject = "Resumo Semanal"
    body = f"Olá,\n\nAqui está a resposta da IA:\n\n{news}\n\nAtenciosamente,\nSeu Bot de Notícias"

    # Configuração da mensagem
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Conexão com o servidor de email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, password)
            smtp.sendmail(sender_email, receiver_email, msg.as_string())
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar o email: {e}")

def job():
    response = get_response_from_openai()
    send_email(response)

# Agenda a execução do job toda sexta-feira às 9h
schedule.every().friday.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
