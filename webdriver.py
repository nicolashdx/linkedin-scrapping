from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

def WebDriver_Init(webdriver_path):
    srv = Service(webdriver_path) 
    opt = webdriver.ChromeOptions()
    return webdriver.Chrome(service=srv, options=opt)

def WebDriver_Close(driver):
    time.sleep(1)
    driver.close()

def Login_Linkedin(driver, account):
    # Abrindo a página de Login do LinkedIn
    driver.get('https://www.linkedin.com/login/')
    time.sleep(1) # aguardar 1 segundos para a página abrir

    # Inserindo o usuário
    usuario = driver.find_element('id','username') # acessando o campo usuário
    usuario.send_keys(account['username']) # enviando a string com o usuário

    # Inserindo a senha
    senha = driver.find_element('id','password') # acessando o campo senha
    senha.send_keys(account['password']) # enviando a string com a senha

    # Clicando no botão 'Entrar' para acessar a conta no LinkedIn
    driver.find_element("xpath","//button[@type='submit']").click()

    # Checando se o login foi bem sucedido. Se sim, retorna True, se não, retorna False
    url = driver.current_url

    if "login" in url:
        return False
    else:
        return True
