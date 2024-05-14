import google.generativeai as genai
from ast import literal_eval
from itertools import combinations, product

import credentials

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

def Gerar_Variacoes(nome_completo):
    combinacoes = Combinacoes_Nome(nome_completo)

    GOOGLE_API_KEY = credentials.Google_Gemini_API_Key()
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    br = "\n"

    query = f"Use Processamento de Linguagem Natural para ordenar, do mais ao menos provável, 5 das possíveis variações que poderiam ser usadas como nome na plataforma Linkedin:\n{br.join(combinacoes)}\nApresente o resultado em uma lista em python, sem textos ou caracteres desnecessários"

    response = model.generate_content(query)
    result = response.text.replace('\n', '')
    result = result[result.find('['):result.find(']')+1]
    try:
        nomes = literal_eval(result)
        return nomes
    except:
        return None



