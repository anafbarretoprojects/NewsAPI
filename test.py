import unittest
from unittest.mock import patch, MagicMock
from newsopenIA import get_response_from_newsapi, send_email, job

class TestNewsAPI(unittest.TestCase):

    @patch('requests.get')
    def test_get_response_from_newsapi(self, mock_get):
        # Configura o mock para retornar uma resposta simulada
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                'articles': [
                    {'title': 'Notícia 1', 'url': 'http://example.com/1'},
                    {'title': 'Notícia 2', 'url': 'http://example.com/2'}
                ]
            }
        )
        
        response = get_response_from_newsapi()
        expected_response = (
            "1. Notícia 1 - http://example.com/1\n\n"
            "2. Notícia 2 - http://example.com/2"
        )
        self.assertEqual(response, expected_response)
    
    @patch('smtplib.SMTP')
    @patch('os.getenv')
    def test_send_email(self, mock_getenv, mock_smtp):
        # Configura o mock para as variáveis de ambiente
        mock_getenv.side_effect = lambda key: {
            'SENDER_EMAIL': 'sender@example.com',
            'RECEIVER_EMAIL': 'receiver@example.com',
            'EMAIL_PASSWORD': 'password'
        }[key]
        
        # Configura o mock para o SMTP
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value = mock_smtp_instance
        
        # Testa a função de envio de e-mail
        send_email('Resumo das notícias.')
        
        # Verifica se o e-mail foi enviado
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with('sender@example.com', 'password')
        mock_smtp_instance.sendmail.assert_called_once()

    @patch('newsopenIA.get_response_from_newsapi')
    @patch('newsopenIA.send_email')
    def test_job(self, mock_send_email, mock_get_response_from_newsapi):
        # Configura os mocks
        mock_get_response_from_newsapi.return_value = 'Resumo das notícias.'
        
        # Executa o job
        job()
        
        # Verifica se as funções foram chamadas
        mock_get_response_from_newsapi.assert_called_once()
        mock_send_email.assert_called_once_with('Resumo das notícias.')

if __name__ == '__main__':
    unittest.main()
