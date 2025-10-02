import unicodedata
import requests

def normalizar_texto(txt):
    return unicodedata.normalize("NFD", txt).encode("ascii", "ignore").decode("utf-8").lower()

def buscar_municipio_ibge(nome_cidade):
    try:
        url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None

        municipios = resp.json()
        nome_normalizado = normalizar_texto(nome_cidade.strip())
        for m in municipios:
            if normalizar_texto(m["nome"]) == nome_normalizado:
                uf = m["microrregiao"]["mesorregiao"]["UF"]["sigla"]
                return f"{m['nome']} - {uf}"
        return None
    except Exception as e:
        print("Erro IBGE:", e)
        return None
