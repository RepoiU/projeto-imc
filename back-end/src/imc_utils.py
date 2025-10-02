def calcular_imc(peso, altura):
    return round(peso / (altura ** 2), 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso", "Inclua mais carboidratos complexos, proteínas e gorduras boas."
    elif imc < 25:
        return "Peso normal", "Mantenha uma dieta equilibrada e rica em fibras."
    elif imc < 30:
        return "Sobrepeso", "Reduza açúcares, aumente fibras e proteínas magras."
    elif imc < 35:
        return "Obesidade Grau I", "Evite ultraprocessados, controle carboidratos refinados."
    elif imc < 40:
        return "Obesidade Grau II", "Procure acompanhamento nutricional, mantenha dieta com vegetais e proteínas magras."
    else:
        return "Obesidade Grau III", "Necessário acompanhamento médico/nutricional urgente."
