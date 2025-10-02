import os
import re

# retorna caminhos importantes
def _paths():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "template.pdf")
    RESULTADOS_PATH = os.path.join(BASE_DIR, "resultados")
    os.makedirs(RESULTADOS_PATH, exist_ok=True)
    return BASE_DIR, RESULTADOS_PATH, TEMPLATE_PATH


def formatar_numero(numero: str) -> str:
    """
    Formata número para o padrão brasileiro:
    +55 (DD) 9XXXX-XXXX ou +55 (DD) XXXX-XXXX
    """
    numero = re.sub(r"\D", "", numero)  # mantém só dígitos

    if numero.startswith("55"):  # já tem código do Brasil
        numero = numero[2:]

    if len(numero) == 11:  # celular
        ddd, parte1, parte2 = numero[:2], numero[2:7], numero[7:]
        return f"+55 ({ddd}) {parte1}-{parte2}"
    elif len(numero) == 10:  # fixo
        ddd, parte1, parte2 = numero[:2], numero[2:6], numero[6:]
        return f"+55 ({ddd}) {parte1}-{parte2}"

    return numero
