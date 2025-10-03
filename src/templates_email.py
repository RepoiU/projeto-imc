def template_email(nome, imc, classificacao, recomendacao):
    """
    Gera o corpo do e-mail em HTML para envio do relatório de IMC.
    Usa a logo servida pelo Flask (pasta static/).
    """
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color:#f9f9f9; padding:20px;">
            <div style="max-width:600px; margin:auto; background:#fff; border-radius:8px; padding:20px; border:1px solid #ddd;">
                
                <!-- Cabeçalho -->
                <div style="text-align:center; margin-bottom:20px;">
                    <img src="https://projeto-imc.onrender.com/static/novatra_logo_black.png" 
                         alt="Novatra" 
                         style="max-width:120px; margin-bottom:10px;">
                    <h2 style="color:#2E4053;">Relatório de IMC</h2>
                </div>

                <!-- Corpo -->
                <p>Olá <b>{nome}</b>,</p>
                <p>Segue em anexo o seu relatório de IMC personalizado.</p>

                <div style="background:#f1f1f1; padding:15px; border-radius:6px; margin:20px 0;">
                    <p><b>IMC:</b> {imc} ({classificacao})</p>
                    <p><b>Recomendação:</b> {recomendacao}</p>
                </div>

                <p>Nosso objetivo é ajudar você a alcançar mais saúde e bem-estar.</p>
                <p style="margin-top:20px;">Atenciosamente,<br><b>Equipe Novatra</b></p>

                <!-- Rodapé -->
                <hr style="margin:30px 0;">
                <p style="font-size:12px; color:#555; text-align:center;">
                    Este é um e-mail automático, por favor não responda.<br>
                    🔗 <a href="https://projeto-imc.onrender.com" 
                          style="color:#1A5276; text-decoration:none;">Acesse nosso site</a>
                </p>
            </div>
        </body>
    </html>
    """
