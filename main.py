import webdriver, credentials, crawler

import pandas as pd
from time import time

driver = webdriver.WebDriver_Init("webdriver-linux64/chromedriver")

if webdriver.Login_Linkedin(driver, credentials.Linkedin_Account("login.txt")):
    print("Login efetuado com sucesso!")
else:
    print("Falha ao efetuar o login.")

names = crawler.Names_To_Track("names.txt")

query = 'Graduação UFMG inurl:"linkedin"'

start_time = time()

result = crawler.Crawling(driver, names, query)

end_time = time()

driver.close()

print(f"Duração: {end_time-start_time:.0f} segundos.")

# Exportando para csv
df = pd.DataFrame(result)
df.to_csv("output.csv", index=False)