import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# GitHub Secrets에서 설정값 불러오기
SMTP_SERVER = os.environ.get("SMTP_SERVER", "relay.skbroadband.com") # 백엔드 주소
SMTP_PORT = int(os.environ.get("SMTP_PORT", 25))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
FROM_EMAIL = os.environ.get("FROM_EMAIL")
TO_EMAIL = os.environ.get("TO_EMAIL")

def send_test_mail():
    if not SMTP_USER or not SMTP_PASS:
        print("❌ 에러: GitHub Secrets에 SMTP_USER 또는 SMTP_PASS가 설정되지 않았습니다.")
        return

    try:
        print(f"🔄 {SMTP_SERVER}:{SMTP_PORT} 서버 접속 시도 중...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15)
        server.ehlo()
        
        print("🔑 계정 인증(AUTH LOGIN) 진행 중...")
        server.login(SMTP_USER, SMTP_PASS)
        
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = "[GitHub Actions] relay.xxx.com:25 자동 발송 테스트"
        
        body_text = "GitHub Actions 가상 서버에서 성공적으로 SMTP 전송을 완료했습니다!"
        msg.attach(MIMEText(body_text, 'plain', 'utf-8'))
        
        print("🚀 메일 발송 중...")
        server.sendmail(FROM_EMAIL, [TO_EMAIL], msg.as_string())
        server.quit()
        
        print(f"✅ 성공: {TO_EMAIL} 주소로 메일 발송이 완료되었습니다!")
    except Exception as e:
        print(f"❌ 발송 실패: {e}")
        exit(1) # 실패 시 GitHub Actions에 에러 상태 전달

if __name__ == "__main__":
    send_test_mail()
