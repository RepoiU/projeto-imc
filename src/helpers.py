import os

def _paths():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "template.pdf")
    RESULTADOS_PATH = os.path.join(BASE_DIR, "resultados")

    # cria pasta resultados se não existir
    os.makedirs(RESULTADOS_PATH, exist_ok=True)

    # LOG de debug
    print("📂 BASE_DIR:", BASE_DIR)
    print("📄 TEMPLATE_PATH:", TEMPLATE_PATH)
    print("📂 RESULTADOS_PATH:", RESULTADOS_PATH)

    return BASE_DIR, RESULTADOS_PATH, TEMPLATE_PATH


def formatar_numero(numero: str) -> str:
    import re
    numero = re.sub(r"\D", "", numero)  # só dígitos
    if numero.startswith("55"):
        numero = numero[2:]
    if len(numero) == 11:  # celular
        ddd, parte1, parte2 = numero[:2], numero[2:7], numero[7:]
        return f"+55 ({ddd}) {parte1}-{parte2}"
    elif len(numero) == 10:  # fixo
        ddd, parte1, parte2 = numero[:2], numero[2:6], numero[6:]
        return f"+55 ({ddd}) {parte1}-{parte2}"
    return numero
