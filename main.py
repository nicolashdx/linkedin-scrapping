from project import webdriver, credentials, validation, crawler

import pandas as pd

driver = webdriver.WebDriver_Init(".\\WebDriver\\gchromedriver.exe")

account = credentials.Linkedin_Account("login.txt")

if webdriver.Login_Linkedin(driver, account['username'], account['password']):
    print("Login efetuado com sucesso!")
else:
    print("Falha ao efetuar o login.")

names = crawler.Names_To_Track("names.txt")

API_KEY = credentials.Google_API_Key()
SEARCH_ENGINE_ID = credentials.Google_SearchEngine_ID()

query = 'UFMG inurl:"linkedin"'

for p in names:
    results = crawler.Search_Name(p['Name'], query, API_KEY, SEARCH_ENGINE_ID)
    if len(results) > 0:
        for r in results:
            if "br.linkedin.com/in/" in r['link']:
                profile_id = r['link'].split('/')[-1] if(len(r['link'].split('/')[-1])>0) else r['link'].split('/')[-2]
                if(validation.checar_formacao_academica(driver, profile_id, ["UFMG", "Universidade Federal de Minas Gerais"])):
                    p['Linkedin ID'] = profile_id
                    p['Linkedin URL'] = r['link']
                    break
    else:
        p['Linkedin URL'] = ''
        p['Linkedin ID'] = ''

# Exportando para csv
df = pd.DataFrame(names)
df.to_csv("output.csv", index=False)