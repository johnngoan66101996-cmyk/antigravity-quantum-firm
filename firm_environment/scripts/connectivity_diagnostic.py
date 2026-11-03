"""
Unified Connectivity Diagnostic (v9.0.0-OMEGA)
Проверка всех 4 внешних каналов фирмы: Telegram, Mail.ru, Rutube, VK.
"""

import urllib.request
import json
import imaplib
from typing import Dict, Any

def test_telegram_bot() -> Dict[str, Any]:
    token = '8737293186:AAEnb1YMifUyvbjbPeP6WVUe-QRN0ipUFnU'
    url = f'https://api.telegram.org/bot{token}/getMe'
    try:
        req = urllib.request.urlopen(url, timeout=10)
        data = json.loads(req.read().decode())
        if data.get('ok'):
            bot = data['result']
            return {
                'status': 'ONLINE',
                'bot_username': bot.get('username'),
                'bot_id': bot.get('id'),
                'first_name': bot.get('first_name'),
                'details': 'Связь 100% установлена, готов к приёму команд и лидов'
            }
    except Exception as e:
        return {'status': 'ERROR', 'error': str(e)}
    return {'status': 'UNKNOWN'}

def test_mail_ru() -> Dict[str, Any]:
    # Проверка доступности портов IMAP/SMTP
    try:
        mail = imaplib.IMAP4_SSL('imap.mail.ru', 993, timeout=5)
        mail.logout()
        return {
            'status': 'PORT_REACHABLE',
            'server': 'imap.mail.ru:993 (SSL)',
            'auth_status': 'REQUIRES_APP_PASSWORD',
            'details': 'Порт открыт. Для чтения писем требуется Пароль для внешних приложений'
        }
    except Exception as e:
        return {'status': 'ERROR', 'error': str(e)}

def test_vk_api() -> Dict[str, Any]:
    url = 'https://api.vk.com/method/utils.getServerTime?v=5.199'
    try:
        req = urllib.request.urlopen(url, timeout=10)
        data = json.loads(req.read().decode())
        server_time = data.get('response')
        return {
            'status': 'API_REACHABLE',
            'vk_server_time': server_time,
            'auth_status': 'REQUIRES_ACCESS_TOKEN',
            'details': 'Сервер VK отвечает. Требуется Community или User Access Token'
        }
    except Exception as e:
        return {'status': 'ERROR', 'error': str(e)}

def test_rutube_api() -> Dict[str, Any]:
    url = 'https://rutube.ru/api/video/category/'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=10)
        return {
            'status': 'REACHABLE',
            'http_code': res.getcode(),
            'auth_status': 'REQUIRES_STUDIO_SESSION_OR_COOKIES',
            'details': 'API Rutube доступно. Для автопостинга требуются session cookies или API Studio токен'
        }
    except Exception as e:
        return {'status': 'ERROR', 'error': str(e)}

if __name__ == '__main__':
    print('TELEGRAM:', test_telegram_bot())
    print('MAIL:', test_mail_ru())
    print('VK:', test_vk_api())
    print('RUTUBE:', test_rutube_api())
