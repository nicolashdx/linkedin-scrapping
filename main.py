#
#   ARQUIVO PRINCIPAL
#   Por aqui, os módulos são utilizados.
#

# Importando bibliotecas necessárias
import pandas as pd
from time import time

# Importando módulos necessários
import webdriver, credentials, crawler
from log import Log

Log.Init()

Log('info', 'Execução iniciada.')

# Inicializando WebDriver do Selenium através da função que recebe o caminho até o driver
driver = webdriver.Init("webdriver-win64/chromedriver.exe")

if(driver):
    Log('debug', 'Driver Selenium inicializado')

# Automação de login em conta pessoal
if webdriver.Login_Linkedin(driver, credentials.Linkedin_Account("login.txt")):
    Log('debug', 'Login efetuado com sucesso.')
else:
    Log('error', "Falha ao efetuar o login.")


# Importando lista de nomes a partir de um arquivo de texto
names = crawler.Names_To_Track("names.txt")

if names:
    Log('debug', 'Nomes a buscar importados com sucesso.')
else:
    Log('debug', 'Falha ao importar nomes buscados')

# Busca que será feita junto a cada nome
query = 'UFMG linkedin'

# Marcando tempo de início
start_time = time()
Log('info', 'VARREDURA INICIADA.')

# Função principal que retorna dicionário com os resultados da varredura:
# Pessoa = {Nome, Nome público, Curso de formação, ID Linkedin, Url do perfil}
result = crawler.Crawling(driver, names, query)

# Marcando tempo de fim
end_time = time()
Log('info', 'VARREDURA FINALIZADA.')

# Fechando o WebDriver
webdriver.Close(driver)
Log('debug', 'Driver Selenium encerrado.')

# Imprimindo o tempo de execução da varredura
duracao = end_time-start_time
min = duracao//60
seg = duracao%60
Log('info', f'TEMPO DE EXECUÇÃO DA VARREDURA: {min:.0f} minutos e {seg:.0f} segundos.')

# Exportando para csv
df = pd.DataFrame(result)
df.to_csv("output.csv", index=False)
Log('info', 'Dados exportados com sucesso.')

Log('info', 'Encerrando programa.')