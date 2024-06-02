#
#   MÓDULO CRAWLER
#   Aqui, estão as funções relacionadas à varredura que será feita.
#

# Importando bibliotecas necessárias
from duckduckgo_search import DDGS

# Importando módulos necessários
import validation, gemini
from log import Log

# Função que lê arquivo de texto e retorna um dicionário a ser preenchido após a varredura
def Names_To_Track(txt_name):
    # Lendo arquivo com nomes de pessoas a serem localizadas
    pessoas = []
    try:
        with open(txt_name, 'r', encoding='utf-8') as file:
            linhas = file.readlines()
        for linha in linhas:
            pessoas.append({'Nome Completo':linha.replace('\n', ''), 'Nome Publico':'','Curso':'', 'Linkedin ID': '', 'Linkedin URL': ''})
    except:
        Log('error', 'Arquivo de nomes nao encontrado.')
        return None
    return pessoas

# Função que utiliza a API de busca para encontrar os perfis no Linkedin e retorna uma lista com os resultados
# Busca: {Nome} + Graduação UFMG + inurl:linkedin
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
        # Imprimindo status de progresso
        if cont > 0:
            perc = (cont/len(nomes))*100
        else:
            perc = 0
        
        Log('info', f"{perc:.0f}% - Procurando por {pessoa['Nome Completo']}:")
        
        # Gerando combinações de nome público utilizando NLP
        possiveis_nomes = gemini.Gerar_Variacoes(pessoa['Nome Completo'])
        
        rejeitados = []
        
        # Para cada uma das combinações
        for n in possiveis_nomes:
            
            # Pesquisando variação
            results = Search_Name(n, busca)
            Log('debug', f"Pesquisando por {n} {busca}")
            
            if len(results) > 0:
                # Separando o primeiro link que contém um perfil nos resultados da busca
                r = ''
                Log('debug', f"Resultados: {', '.join(results)}")
                for i in range(len(results)):
                    if "br.linkedin.com/in/" in results[i]:
                        r = results[i]
                        break
                # Verificando se um perfil foi encontrado nos resultados de busca
                if r:
                    # Separando da url o ID do perfil
                    profile_id = r.rsplit("/in/", 1)[-1].strip()
                    
                    if(profile_id not in rejeitados):
                        Log('detail', f"Perfil encontrado: {profile_id}")
                        
                        # Verificando se o nome do perfil encontrado coincide com o nome buscado
                        nome_publico, nome_formacao = validation.checar_perfil(driver, profile_id, pessoa['Nome Completo'], possiveis_nomes, ["UFMG", "Universidade Federal de Minas Gerais"])
                        
                        if nome_publico and nome_formacao:
                            # Se as verificações forem bem sucedidas, preencher dados obtidos
                            Log('detail', "O perfil passou na validacao.")
                            
                            pessoa['Nome Publico'] = nome_publico
                            pessoa['Curso'] = nome_formacao
                            pessoa['Linkedin ID'] = profile_id
                            pessoa['Linkedin URL'] = r
                            break
                        else:
                        # Se não, pular para a próxima iteração
                            rejeitados.append(profile_id)
                            Log('detail', "O perfil nao passou na validacao.")
                    else:
                        Log('detail', f"Perfil já descartado.")
                else:
                    Log('detail', f"Perfil nao encontrado.")
            else: 
                Log('detail', f"A pesquisa nao retornou resultados.")
        
        if pessoa['Linkedin ID']:
            Log('info', f"{pessoa['Nome Completo']} ENCONTRADO.")
        else:
            Log('warning', f"{pessoa['Nome Completo']} NAO ENCONTRADO.")
        
        cont += 1
    return nomes
    







