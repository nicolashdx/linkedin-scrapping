#
#   MÓDULO DE VALIDAÇÃO DE PERFIL
#   Aqui, estão as funções que utilizam o código fonte de uma página
#   web para verificar se um perfil pertence a pessoa que é buscada.
#

# Importando bibliotecas necessárias
from bs4 import BeautifulSoup
import time
from unidecode import unidecode
from difflib import SequenceMatcher

# Constantes de ajuste
CMP_SCORE_MIN = 0.7

# Função que remove o acento e caracteres especiais de uma string. Exemplo: "transação" para "transacao"
def remover_acentos(string):
    return unidecode(string)

def comparar_nomes(nome_completo, possivel_nome):
    # Inicializa um objeto SequenceMatcher com as duas strings
    seq_matcher = SequenceMatcher(None, nome_completo, possivel_nome)
    # Obtém o score de semelhança entre as duas strings
    score = seq_matcher.ratio()
    if score >= CMP_SCORE_MIN:
        return True
    else:
        return False

def info_nome(soup):
    # Obtendo o HTML de extração do nome 
    try:
        nome_div = soup.find('section', class_="scaffold-layout-toolbar").find('div').find('div').find('div').find_all('div')[2].find('div')
        nome = nome_div.get_text().strip()
        return nome
    except:
        return ''

# Funções que checam perfil acadêmico de usuário, comparam se uma instituição está presente e retorna booleano
def info_academica_1(item_educacao):
    # Extraindo o nome da Instituição de Ensino
    nome_instituicao_loc = item_educacao.find('div', {'class':'display-flex align-items-center mr1 hoverable-link-text t-bold'}).find('span',{'aria-hidden':'true'})
    nome_instituicao = nome_instituicao_loc.get_text().strip()

    # Separando o Tipo da Formação do Nome do Formação
    tipo_nome_formacao_loc = item_educacao.find('span',{'class':'t-14 t-normal'}).find('span',{'aria-hidden':'true'})
    tipo_nome_formacao = tipo_nome_formacao_loc.get_text().strip().split(',')

    # Tipo da Formação
    tipo_formacao = tipo_nome_formacao[0].strip()

    # Nome da Formação
    nome_formacao = tipo_nome_formacao[1].strip()

    # Extraindo a duração da Formação
    duracao_formacao_loc = item_educacao.find('span',{'class':'t-14 t-normal t-black--light'}).find('span',{'aria-hidden':'true'})
    duracao_formacao = duracao_formacao_loc.get_text().strip()
    
    # Retornando as informações
    return nome_instituicao, tipo_formacao, nome_formacao, duracao_formacao

def info_academica_2(item_educacao):
    # Extraindo o nome da Instituição de Ensino
    nome_instituicao_loc = item_educacao.find('span', {'class':'mr1 hoverable-link-text t-bold'}).find('span',{'aria-hidden':'true'})
    nome_instituicao = nome_instituicao_loc.get_text().strip()

    # Extraindo a duração da Formação (caso esteja disponível)
    try:
        duracao_formacao_loc = item_educacao.find('span',{'class':'t-14 t-normal t-black--light'}).find('span',{'aria-hidden':'true'})
        duracao_formacao = duracao_formacao_loc.get_text().strip()
    except:
        duracao_formacao = ''
    
    # Campos não disponíveis `nome_formacao` e `tipo_formacao`
    nome_formacao = ''
    tipo_formacao = ''
    
    # Retornando as informações
    return nome_instituicao, tipo_formacao, nome_formacao, duracao_formacao

# Função para extrair as informações referente à Formação Acadêmica mais recente
def checar_formacao_academica(driver, instituicoes):
    # Lendo a página do início ao fim
    inicio = time.time()
    posicao_inicial_rolamento = 0
    posicao_final_rolamento = 1000

    while True:
        driver.execute_script(f"window.scrollTo({posicao_inicial_rolamento},{posicao_final_rolamento})")

        posicao_inicial_rolamento = posicao_final_rolamento
        posicao_final_rolamento += 1000

        # Aguardando 2 segundos
        time.sleep(2)

        fim = time.time()

        # Executar o script por 5 segundos
        if round(fim - inicio) > 5:
            break

    # Salvando o código fonte da página em uma variável
    src_educacao = driver.page_source

    # Utilizando o código fonte para gerar um objeto Beautiful Soup
    soup_educacao = BeautifulSoup(src_educacao,'lxml')
    
    # Obtendo o HTML de extração das formações acadêmicas
    try:
        educacao = soup_educacao.find('div',{'class':'scaffold-finite-scroll__content'}).find('ul').find_all('li')
    except:
        return None
            
    # Retornando as informações extraídas
    formacoes = []

    for edc in educacao:
        if(edc.find('div', {'class':'display-flex align-items-center mr1 hoverable-link-text t-bold'})):
            try:
                try:
                    nome_instituicao, tipo_formacao, nome_formacao, duracao_formacao = info_academica_1(edc)
                except:
                    nome_instituicao, tipo_formacao, nome_formacao, duracao_formacao = info_academica_2(edc)
                formacoes.append({'instituicao': nome_instituicao, 'tipo': tipo_formacao, 'area': nome_formacao, 'duracao': duracao_formacao})
            except:
                nome_instituicao, tipo_formacao, nome_formacao, duracao_formacao = '', '', '', ''
    for nome in instituicoes:
        for f in formacoes:
            if(remover_acentos(nome).upper() == remover_acentos(f['instituicao']).upper()):
                return nome_formacao
    
    return ''

# Função que compara o nome pesquisado ao nome encontrado. Se semelhantes, retorna o nome.
def checar_nome(driver, nome_completo):
    # Verificando se a página em questão se trata de um perfil ativo
    if "linkedin.com/in" in driver.current_url:
        # Salvando o código fonte da página em uma variável
        src = driver.page_source

        # Utilizando o código fonte para gerar um objeto Beautiful Soup
        soup = BeautifulSoup(src,'lxml')
        
        nome = info_nome(soup)
        
        # Comparando os nomes, se semelhantes, retorna o nome
        if comparar_nomes(nome_completo, nome):
            return nome

    # Caso as condicionais não se cumpram, retorna vazio
    return ''
    

def checar_perfil(driver, perfil_id, nome_completo, instituicoes):
    # Acessando a página referente às formações acadêmicas
    formacao_url = f"https://www.linkedin.com/in/{perfil_id}/details/education/"
    driver.get(formacao_url)
    time.sleep(2)
    
    nome_publico = checar_nome(driver, nome_completo)
    if not nome_publico:
        return '', ''
    
    curso = checar_formacao_academica(driver, instituicoes)
    if not curso:
        return '', ''

    return nome_publico, curso