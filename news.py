import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define a chave da API da NewsAPI
news_api_key = os.getenv('NEWS_API_KEY')
news_api_url = "https://newsapi.org/v2/top-headlines"

def get_response_from_newsapi():
    try:
        response = requests.get(news_api_url, params={
            'apiKey': news_api_key,
            'category': 'technology',
            'language': 'pt',
            'pageSize': 10
        })
        data = response.json()

        if response.status_code == 200 and 'articles' in data:
            articles = data['articles']
            news_summary = "\n\n".join([f"{i+1}. {article['title']} - {article['url']}" for i, article in enumerate(articles)])
            return news_summary.strip()
        else:
            return "Não foi possível obter as notícias no momento."
    except Exception as e:
        print(f"Erro ao obter resposta da NewsAPI: {e}")
        return "Não foi possível obter uma resposta da API."

"""def send_email(news):
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    # Configuração do assunto e corpo do email
    subject = "Resumo Semanal"
    body = f"Olá,\n\nAqui está o resumo das principais notícias de tecnologia:\n\n{news}\n\nAtenciosamente,\nSeu Bot de Notícias"

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
    response = get_response_from_newsapi()
    send_email(response)

# Agenda a execução do job toda sexta-feira às 9h
schedule.every().friday.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)"""

def send_email(news):
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    # Verifica se as credenciais estão carregadas corretamente
    if not sender_email or not receiver_email or not password:
        print("Credenciais de e-mail não carregadas corretamente. Verifique seu arquivo .env.")
        return

    # Configuração do assunto e corpo do email
    subject = "Resumo Semanal"
    body = f"Olá,\n\nAqui está o resumo das principais notícias de tecnologia:\n\n{news}\n\nAtenciosamente,\nSeu Bot de Notícias"

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
    except smtplib.SMTPAuthenticationError as e:
        print("Erro de autenticação SMTP: Verifique se a senha do aplicativo está correta.")
        print(e)
    except smtplib.SMTPException as e:
        print(f"Erro ao enviar o email: {e}")

def job():
    response = get_response_from_newsapi()
    send_email(response)

if __name__ == "__main__":
    job()