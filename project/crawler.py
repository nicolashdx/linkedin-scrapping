import requests

def Names_To_Track(txt_name):
    # Lendo arquivo com nomes de pessoas a serem localizadas
    pessoas = []

    with open(txt_name, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    for linha in linhas:
        pessoas.append({'Name':linha.replace('\n', ''), 'Public Name':'','Curso':'', 'Linkedin ID': '', 'Linkedin URL': ''})

    return pessoas


def Search_Name(nome, params, API_KEY, SEARCH_ENGINE_ID):
    query_string = f'{nome} {params}'
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query_string}"
    response = requests.get(url)
    data = response.json()
    if 'items' in data:
        return data['items']
    else:
        return []









