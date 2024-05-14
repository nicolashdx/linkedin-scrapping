def Linkedin_Account(txt_name):
    with open(txt_name, 'r') as file:
        linhas = file.readlines()
    return {"username": linhas[0].strip(), "password": linhas[1].strip()}

def Google_API_Key():
    return open('api_key').read()

def Google_SearchEngine_ID():
    return open('search_engine_id').read()

def Google_Gemini_API_Key():
    return open('gemini_api_key').read()
