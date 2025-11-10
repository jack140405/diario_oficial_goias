import re, time, os, requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from .config import HEADLESS

URL = "https://diariooficial.abc.go.gov.br/buscanova/"

def obter_edicoes_disponiveis(max_edicoes=30, wait_seconds=3):
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    time.sleep(wait_seconds)
    edicoes_vistas = set()
    tentativas_sem_novos = 0
    while len(edicoes_vistas) < max_edicoes and tentativas_sem_novos < 10:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_seconds)
        anchors = driver.find_elements(By.TAG_NAME, "a")
        novos = [a.get_attribute('href') for a in anchors if a.get_attribute('href')]
        novos = [h for h in novos if re.search(r"/portal/edicoes/download/\d+$", h)]
        qtd_antes = len(edicoes_vistas)
        edicoes_vistas.update(novos)
        if len(edicoes_vistas) == qtd_antes:
            tentativas_sem_novos += 1
        else:
            tentativas_sem_novos = 0
    driver.quit()
    numeros = sorted([int(re.search(r"/download/(\d+)$", link).group(1)) for link in edicoes_vistas], reverse=True)
    return numeros[:max_edicoes]

def baixar_por_numero(numero, pasta_temp):
    url = f"https://diariooficial.abc.go.gov.br/portal/edicoes/download/{numero}"
    nome = os.path.join(pasta_temp, f"DiarioOficial_GO_{numero}.pdf")
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            with open(nome, 'wb') as f:
                f.write(r.content)
            return nome
    except Exception as e:
        print('Erro download', e)
    return None

def baixar_diarios(qtd_edicoes=5, pasta_temp=None):
    if pasta_temp is None:
        pasta_temp = os.path.join(os.path.dirname(__file__), '..', 'temp')
    os.makedirs(pasta_temp, exist_ok=True)
    edicoes = obter_edicoes_disponiveis(qtd_edicoes)
    baixados = []
    for n in edicoes:
        caminho = baixar_por_numero(n, pasta_temp)
        if caminho:
            baixados.append(caminho)
    return baixados
