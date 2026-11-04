"""
Mail OTP & Notification Reader (v9.0.0-OMEGA)
Автономный модуль чтения и парсинга кодов подтверждения из ящика sugatov86@list.ru.
"""

import imaplib
import email
from email.header import decode_header
import re
from typing import Optional, Dict, Any

EMAIL_ACCOUNT = "sugatov86@list.ru"
APP_PASSWORD = "gJbmrE8TZOtr17VNz8U0"
IMAP_SERVER = "imap.mail.ru"

def get_latest_code(sender_filter: Optional[str] = None) -> Dict[str, Any]:
    """
    Автоматически находит последнее письмо (опционально фильтруя по отправителю,
    например 'gid.ru' или 'rutube') и извлекает проверочный код.
    """
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, 993, timeout=10)
        mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
        mail.select("INBOX")
        
        status, data = mail.search(None, "ALL")
        if not data or not data[0]:
            mail.logout()
            return {"status": "EMPTY"}
            
        mail_ids = data[0].split()
        
        # Сканируем последние 10 писем
        for m_id in reversed(mail_ids[-10:]):
            status, msg_data = mail.fetch(m_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            sender = msg.get("From", "")
            # Фильтр по отправителям Газпром ID / Rutube
            if sender_filter:
                if sender_filter.lower() not in sender.lower():
                    continue
            else:
                if not any(trusted in sender.lower() for trusted in ["gid.ru", "rutube", "pass.media"]):
                    continue
                
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")
                
            # Извлекаем тело письма
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type in ["text/plain", "text/html"]:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode(part.get_content_charset() or "utf-8", errors="ignore") + "\n"
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode(msg.get_content_charset() or "utf-8", errors="ignore")
                    
            # Очищаем от стилей, скриптов и тегов HTML
            clean_body = re.sub(r"<style[^>]*>.*?</style>", "", body, flags=re.DOTALL | re.IGNORECASE)
            clean_body = re.sub(r"<script[^>]*>.*?</script>", "", clean_body, flags=re.DOTALL | re.IGNORECASE)
            clean_body = re.sub(r"<[^>]+>", "\n", clean_body)
            clean_body = re.sub(r"&[a-z]+;", " ", clean_body)
            
            # 1. Поиск кода на отдельной строке (как в письме Rutube: "\n7242\n")
            isolated_codes = re.findall(r"^\s*(\d{4,6})\s*$", clean_body, flags=re.MULTILINE)
            if isolated_codes:
                extracted_code = isolated_codes[0]
            else:
                # 2. Поиск кода рядом с ключевыми словами
                context_match = re.search(r"(?:код|rutube|аккаунт|вход)[\s\S]{1,60}?\b(\d{4,6})\b", clean_body, flags=re.IGNORECASE)
                if context_match:
                    extracted_code = context_match.group(1)
                else:
                    # 3. Общий поиск 4-значных или 6-значных кодов
                    code_matches = re.findall(r"\b(\d{4}|\d{6})\b", clean_body)
                    extracted_code = code_matches[0] if code_matches else None
            
            mail.logout()
            return {
                "status": "FOUND",
                "sender": sender,
                "subject": subject,
                "code": extracted_code,
                "raw_text_preview": (body[:150] if body else subject)
            }
            
        mail.logout()
        return {"status": "NOT_FOUND"}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

if __name__ == "__main__":
    res = get_latest_code()
    print("Результат чтения последнего кода:", res)
