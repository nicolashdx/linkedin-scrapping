import webdriver, credentials, crawler

import pandas as pd

driver = webdriver.WebDriver_Init("webdriver-linux64/chromedriver")

if webdriver.Login_Linkedin(driver, credentials.Linkedin_Account("login.txt")):
    print("Login efetuado com sucesso!")
else:
    print("Falha ao efetuar o login.")

names = crawler.Names_To_Track("names.txt")[:4]

query = 'Graduação UFMG inurl:"linkedin"'

result = crawler.Crawling(driver, names, query)

# Exportando para csv
df = pd.DataFrame(result)
df.to_csv("output.csv", index=False)