#
#   MÓDULO GEMINI
#   Aqui, está a parte de predição e otimização de busca utilizando NLP.
#

# Importando bibliotecas necessárias
import google.generativeai as genai
from ast import literal_eval
from itertools import combinations, product

# Importando módulos necessários
import credentials
from log import Log


# Função que recebe um nome completo e retorna todas as combinações possíveis de nome e sobrenome
def Combinacoes_Nome(nome_completo):
    partes_nome = nome_completo.split()

    # Primeiro nome é a primeira parte
    primeiro_nome = partes_nome[0]

    # Sobrenomes são as partes restantes
    sobrenomes = partes_nome[1:]

    # Concatenando partes como 'da' e 'Silva' para 'da Silva'
    for i in range(0, len(sobrenomes)-1):
        if not any(caractere.isupper() for caractere in sobrenomes[i]):
            s = sobrenomes[i]
            sobrenomes.remove(s)
            sobrenomes[i] = f"{s} {sobrenomes[i]}"

    combinacoes = []
    tamanho = len(sobrenomes)
    # Gera todas as combinações possíveis de índices das partes do nome
    for i in range(1, tamanho+1):
        for comb in combinations(sobrenomes, i):
            combinacoes.append(primeiro_nome + " " + " ".join(comb))

    return combinacoes


# Função que utiliza a API do Gemini para prever qual possível nome é utilizado a partir de NLP.
# A ideia é otimizar o tempo de varredura aumentando a predictibilidade do nome público
def Gerar_Variacoes(nome_completo):
    # Gerando combinações
    combinacoes = Combinacoes_Nome(nome_completo)
    
    # Instanciando Gemini
    GOOGLE_API_KEY = credentials.Google_Gemini_API_Key()
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    # Caractere de "pular linha"
    br = "\n"

    # Pergunta que será enviada ao Gemini
    query = f"A partir da lista informada, use Processamento de Linguagem Natural para ordenar, do mais ao menos provável, as {len(combinacoes)} possíveis variações que poderiam ser usadas como nome na plataforma Linkedin:\n{br.join(combinacoes)}\nApresente o resultado em uma lista em python ordenada, sem textos ou caracteres desnecessários"

    # Filtrando resposta para extrair uma lista com a sintaxe correta da linguagem
    response = ''
    for i in range(5):
        try:
            response = model.generate_content(query)
            result = response.text.replace('\n', '')
            result = result[result.find('['):result.find(']')+1]
            
            break
        except:
            continue 
    try:
        nomes = literal_eval(result)
        Log('debug', f"Variações de nome público: {', '.join(nomes)}")
        return nomes
    # Quando não é possível, retornar valor nulo
    except:
        Log('warning', "Falha ao ordenar variações de nome público.")
        return combinacoes



