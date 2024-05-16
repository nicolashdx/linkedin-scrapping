#
#   MÓDULO CRAWLER
#   Aqui, estão as funções relacionadas à varredura que será feita.
#

# Importando bibliotecas necessárias
import requests
from duckduckgo_search import DDGS

# Importando módulos necessários
import credentials, validation, gemini

# Função que lê arquivo de texto e retorna um dicionário a ser preenchido após a varredura
def Names_To_Track(txt_name):
    # Lendo arquivo com nomes de pessoas a serem localizadas
    pessoas = []

    with open(txt_name, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    for linha in linhas:
        pessoas.append({'Nome Completo':linha.replace('\n', ''), 'Nome Publico':'','Curso':'', 'Linkedin ID': '', 'Linkedin URL': ''})

    return pessoas

# Função que utiliza a API de busca do Google para encontrar os perfis no Linkedin e retorna uma lista com os resultados
# Busca: {Nome} + Graduação UFMG + inurl:linkedin
def Google_Search_Name(nome, params):
    API_KEY = credentials.Google_API_Key()
    SEARCH_ENGINE_ID = credentials.Google_SearchEngine_ID()

    query_string = f'{nome} {params}'
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query_string}"
    response = requests.get(url)
    data = response.json()
    if 'items' in data:
        return list(map(lambda r: r['link'], data['items']))
    else:
        return []

def Search_Name(nome, params):
    results = ''
    for i in range(5):
        try:
            results = DDGS().text(f"{nome} {params}", max_results=5)
            break
        except:
            continue
    if results:
        return list(map(lambda r: r['href'], results))
    else:
        return []

# Função principal de varredura que recebe o dicionário com os nomes e o retorna com as informações encontradas.
def Crawling(driver, nomes, busca):
    cont = 0 # Iniciando contador de progresso
    
    # Para cada uma das pessoas na lista de nomes
    for pessoa in nomes:
        # Gerando combinações de nome público utilizando NLP
        possiveis_nomes = gemini.Gerar_Variacoes(pessoa['Nome Completo'])
        print(f"Variações: {len(possiveis_nomes)}")
        
        # Para cada uma das combinações
        for n in possiveis_nomes:
            # Pesquisando variação
            results = Search_Name(n, busca)
            
            if len(results) > 0:
                # Separando o primeiro link que contém um perfil nos resultados da busca
                r = ''
                for i in range(len(results)):
                    if "br.linkedin.com/in/" in results[i]:
                        r = results[i]
                        break
                
                # Verificando se um perfil foi encontrado nos resultados de busca
                if r:
                    # Separando da url o ID do perfil
                    profile_id = r.rsplit("/in/", 1)[-1].strip()
                    
                    # Verificando se o nome do perfil encontrado coincide com o nome buscado
                    nome_publico, nome_formacao = validation.checar_perfil(driver, profile_id, pessoa['Nome Completo'], ["UFMG", "Universidade Federal de Minas Gerais"])
                    # Se não, pular para a próxima iteração
                    if not nome_publico or not nome_formacao:
                        continue
                    
                    # Se as verificações forem bem sucedidas, preencher dados obtidos
                    pessoa['Nome Publico'] = nome_publico
                    pessoa['Curso'] = nome_formacao
                    pessoa['Linkedin ID'] = profile_id
                    pessoa['Linkedin URL'] = r
                    break
        
        # Imprimindo status de progresso
        cont += 1
        perc = (cont/len(nomes))*100
        print(f"{perc:.0f}% - {pessoa['Nome Completo']}")
    return nomes
    







