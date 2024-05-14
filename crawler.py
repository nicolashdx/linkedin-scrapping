import requests
import credentials, validation, gemini

def Names_To_Track(txt_name):
    # Lendo arquivo com nomes de pessoas a serem localizadas
    pessoas = []

    with open(txt_name, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    for linha in linhas:
        pessoas.append({'Nome Completo':linha.replace('\n', ''), 'Nome Publico':'','Curso':'', 'Linkedin ID': '', 'Linkedin URL': ''})

    return pessoas

def Search_Name(nome, params):
    API_KEY = credentials.Google_API_Key()
    SEARCH_ENGINE_ID = credentials.Google_SearchEngine_ID()

    query_string = f'{nome} {params}'
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query_string}"
    response = requests.get(url)
    data = response.json()
    if 'items' in data:
        return data['items']
    else:
        return []

def Crawling(driver, nomes, busca):
    cont = 0
    for pessoa in nomes:
        possiveis_nomes = gemini.Gerar_Variacoes(pessoa['Nome Completo'])
        for n in possiveis_nomes:
            results = Search_Name(n, busca)
            if len(results) > 0:
                r = results[0]
                if "br.linkedin.com/in/" in r['link']:
                    profile_id = r['link'].split('/')[-1] if(len(r['link'].split('/')[-1])>0) else r['link'].split('/')[-2]
                    
                    nome_publico = validation.checar_nome(driver, profile_id, n)
                    if not nome_publico:
                        continue
                    
                    nome_formacao = validation.checar_formacao_academica(driver, profile_id, ["UFMG", "Universidade Federal de Minas Gerais"])
                    if not nome_formacao:
                        continue
                    
                    pessoa['Nome Publico'] = nome_publico
                    pessoa['Curso'] = nome_formacao
                    pessoa['Linkedin ID'] = profile_id
                    pessoa['Linkedin URL'] = r['link']
                    break
        cont += 1
        perc = (cont/len(nomes))*100
        print(f"{perc:.0f}% - {pessoa['Nome Completo']}")
    return nomes
    







