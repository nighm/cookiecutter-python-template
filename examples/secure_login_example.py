from typing import Optional
from pathlib import Path
import os
import json
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from pydantic import BaseModel, SecretStr
from src.utils.logging import get_logger

# 初始化日志记录器，确保敏感信息不会被记录
logger = get_logger(__name__)

class Credentials(BaseModel):
    """用于安全存储用户凭据的模型"""
    username: str
    password: SecretStr  # 使用SecretStr确保密码不会意外暴露在日志或str()中

class SecureCredentialManager:
    def __init__(self, key_file: str = '.credentials.key'):
        self.key_file = Path(key_file)
        self.credentials_file = Path('.credentials.enc')
        self._init_encryption_key()

    def _init_encryption_key(self) -> None:
        """初始化或加载加密密钥"""
        if not self.key_file.exists():
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        else:
            with open(self.key_file, 'rb') as f:
                key = f.read()
        self.fernet = Fernet(key)

    def save_credentials(self, credentials: Credentials) -> None:
        """安全地保存加密的凭据"""
        data = {
            'username': credentials.username,
            'password': credentials.password.get_secret_value()
        }
        encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
        with open(self.credentials_file, 'wb') as f:
            f.write(encrypted_data)

    def load_credentials(self) -> Optional[Credentials]:
        """加载并解密凭据"""
        try:
            if not self.credentials_file.exists():
                return None
            with open(self.credentials_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = json.loads(self.fernet.decrypt(encrypted_data))
            return Credentials(
                username=decrypted_data['username'],
                password=decrypted_data['password']
            )
        except Exception as e:
            logger.error(f"Failed to load credentials: {str(e)}")
            return None

class AutoLogin:
    def __init__(self, url: str):
        self.url = url
        self.credential_manager = SecureCredentialManager()
        # 从环境变量加载配置
        load_dotenv()
        self.headless = os.getenv('BROWSER_HEADLESS', 'true').lower() == 'true'

    def _init_driver(self):
        """初始化WebDriver，支持无头模式"""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument('--headless')
        return webdriver.Chrome(options=options)

    def login(self, credentials: Optional[Credentials] = None) -> bool:
        """执行自动登录流程"""
        if not credentials:
            credentials = self.credential_manager.load_credentials()
            if not credentials:
                logger.error("No credentials found")
                return False

        try:
            driver = self._init_driver()
            driver.get(self.url)

            # 等待登录表单加载
            wait = WebDriverWait(driver, 10)
            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            password_field = driver.find_element(By.NAME, 'password')

            # 输入凭据
            username_field.send_keys(credentials.username)
            password_field.send_keys(credentials.password.get_secret_value())

            # 提交表单
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()

            # 验证登录成功
            try:
                wait.until(EC.url_changes(self.url))
                logger.info("Login successful")
                return True
            except Exception:
                logger.error("Login failed")
                return False

        except Exception as e:
            logger.error(f"Login process failed: {str(e)}")
            return False
        finally:
            driver.quit()

def main():
    # 示例使用
    login_url = 'https://example.com/login'
    credentials = Credentials(
        username='humm',
        password='hu1334677'
    )

    # 安全保存凭据
    credential_manager = SecureCredentialManager()
    credential_manager.save_credentials(credentials)

    # 执行自动登录
    auto_login = AutoLogin(login_url)
    success = auto_login.login()

    if success:
        print("登录成功！")
    else:
        print("登录失败，请检查凭据或网络连接。")

if __name__ == '__main__':
    main()