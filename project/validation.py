from bs4 import BeautifulSoup
import time

from unidecode import unidecode

def remover_acentos(string):
    return unidecode(string)

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
def checar_formacao_academica(driver, perfil_id, instituicoes):
    # Acessando a página referente às formações acadêmicas
    formacao_url = 'https://www.linkedin.com/in/{}/details/education/'.format(perfil_id)
    driver.get(formacao_url)
    
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
                return True
    
    return False