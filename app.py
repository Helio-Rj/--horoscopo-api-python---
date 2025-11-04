# =================================================================
# PROGRAMA: Consulta de Horóscopo com Tradução
# OBJETIVO: Buscar horóscopo diário de uma API e traduzir para português
# =================================================================

# Importa a biblioteca requests, que permite fazer requisições HTTP
# Docs: https://requests.readthedocs.io/
import requests

# =================================================================
# CONFIGURAÇÃO INICIAL
# =================================================================

# Define o signo desejado (em inglês, pois a API é em inglês)
# Signos válidos: aries, taurus, gemini, cancer, leo, virgo,
#                 libra, scorpio, sagittarius, capricorn, aquarius, pisces
signo = "libra"

# Monta a URL da API usando f-string (formatação de string do Python)
# - f"..." permite inserir variáveis dentro da string usando {variavel}
# - A URL base é: https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily
# - O parâmetro sign recebe o signo escolhido
url = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={signo}"

# =================================================================
# REQUISIÇÃO À API
# =================================================================

# Faz a requisição GET para a API
# - requests.get(url) envia uma requisição HTTP GET para o servidor
# - O resultado é armazenado na variável 'resposta'
resposta = requests.get(url)

# Verifica se a requisição foi bem-sucedida
# - status_code 200 significa "OK" em HTTP
# - Outros códigos comuns: 404 (não encontrado), 500 (erro no servidor)
if resposta.status_code == 200:
    # Converte a resposta de JSON para um dicionário Python
    dados = resposta.json()

    # Extrai o texto do horóscopo dos dados retornados
    # - dados['data'] acessa o objeto principal
    # - ['horoscope_data'] pega o texto do horóscopo
    horoscopo = dados['data']['horoscope_data']

    # =================================================================
    # TRADUÇÃO DO TEXTO
    # =================================================================

    # Bloco try/except para tentar traduzir o texto
    # Se algo der errado, o programa não para, apenas mostra o texto original
    try:
        # Imports necessários para tradução
        # - googletrans: biblioteca de tradução gratuita
        # - asyncio: para lidar com operações assíncronas
        from googletrans import Translator  # pip install googletrans==4.0.0-rc1
        import asyncio

        # Cria um objeto tradutor
        translator = Translator()

        # Tenta traduzir o texto
        # - src='en': idioma de origem (inglês)
        # - dest='pt': idioma de destino (português)
        possible_coro = translator.translate(horoscopo, src='en', dest='pt')

        # TRATAMENTO ESPECIAL: Diferentes versões do tradutor
        # Algumas versões da biblioteca retornam uma 'coroutine' (objeto assíncrono)
        # Precisamos tratar os dois casos possíveis
        if asyncio.iscoroutine(possible_coro):
            # Se for uma coroutine, usa asyncio.run para executar
            traducao = asyncio.run(possible_coro)
        else:
            # Se não for, usa o resultado diretamente
            traducao = possible_coro

        # Extrai o texto traduzido do objeto de tradução
        # - getattr(obj, 'atributo', 'valor_padrao') é uma forma segura de
        #   acessar atributos que podem não existir
        # - Se não encontrar.text, converte o objeto para string
        horoscopo_pt = getattr(traducao, 'text', str(traducao))

        # Exibe o resultado traduzido
        # - signo.capitalize(): primeira letra maiúscula
        print(f"Horóscopo de hoje para {signo.capitalize()} (em Português):\n{horoscopo_pt}")

    except Exception as e:
        # Se algo der errado na tradução:
        # 1. Mostra uma mensagem de aviso com o erro
        # 2. Exibe o texto original em inglês
        print("(Aviso) Não foi possível traduzir automaticamente:", str(e))
        print(f"Horóscopo de hoje para {signo.capitalize()}:\n{horoscopo}")

# Se a requisição à API falhou:
else:
    # Mostra o código de erro HTTP
    # Ex: 404 = não encontrado, 500 = erro no servidor
    print("Erro ao buscar horóscopo:", resposta.status_code)

# =================================================================
# NOTAS DE APRENDIZADO:
# 1. APIs ‘Web’: usamos 'requests' para comunicação HTTP
# 2. JSON: Formato comum para dados na ‘web’, convertido para dict
# 3. Try/Except: Tratamento de erros para código mais robusto
# 4. F-strings: formatação moderna de ‘strings’ no Python
# 5. Async/Await: Básico de programação assíncrona
# =================================================================
