#
#   ARQUIVO PRINCIPAL
#   Por aqui, os módulos são utilizados.
#

# Importando bibliotecas necessárias
import pandas as pd
from time import time

# Importando módulos necessários
import webdriver, credentials, crawler

# Inicializando WebDriver do Selenium através da função que recebe o caminho até o driver
driver = webdriver.Init("webdriver-linux64/chromedriver")

# Automação de login em conta pessoal
if webdriver.Login_Linkedin(driver, credentials.Linkedin_Account("login.txt")):
    print("Login efetuado com sucesso!")
else:
    print("Falha ao efetuar o login.")

# Importando lista de nomes a partir de um arquivo de texto
names = crawler.Names_To_Track("names.txt")

# Busca que será feita junto a cada nome
query = 'Graduação UFMG inurl:"linkedin"'

# Marcando tempo de início
start_time = time()

# Função principal que retorna dicionário com os resultados da varredura:
# Pessoa = {Nome, Nome público, Curso de formação, ID Linkedin, Url do perfil}
result = crawler.Crawling(driver, names, query)

# Marcando tempo de fim
end_time = time()

# Fechando o WebDriver
webdriver.Close(driver)

duracao = end_time-start_time
min = duracao//60
seg = duracao%60

# Imprimindo o tempo de execução da varredura
print(f"Tempo de execução: {min:.0f} minutos e {seg:.0f} segundos.")

# Exportando para csv
df = pd.DataFrame(result)
df.to_csv("output.csv", index=False)