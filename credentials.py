#
#   MÓDULO DE CREDENCIAIS
#   Aqui, estão as credenciais e chaves sensíveis que não podem ser expostas no código em si.
#

# Importando módulos necessários
from log import Log

# Credenciais de login de conta pessoal do Linkedin
def Linkedin_Account(txt_name):
    try:
        with open(txt_name, 'r') as file:
            linhas = file.readlines()
        return {"username": linhas[0].strip(), "password": linhas[1].strip()}
    except:
        Log('error', 'Arquivo de login não encontrado.')
        return {"username": '', "password": ''}

# Chave da API de Custom Search
def Google_API_Key():
    return open('api_key').read()

# Chave da Programmable Search Engine
def Google_SearchEngine_ID():
    return open('search_engine_id').read()

# Chave do Google Gemini
def Google_Gemini_API_Key():
    return open('gemini_api_key').read()
