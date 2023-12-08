from app.config import host

def reset_message(token):
    return f"""
    <html>
        <body>
            <div style="background-color: #060606; text-align: center; display: flex; flex-direction: column; align-items: center; height:auto; width: auto;">
                <div style="text-align: center;"><h1 style="font-weight: bold; text-decoration: underline; color: #FFF; text-align: center;">Réinitialisation du mot de passe</h1></div>
                <div style="margin-top: 100px; margin-bottom: 50px; padding: 50px; width: fit-content; height: fit-content; background-color: #424242; border-radius: 25px;"><p style="color: #FFF;"> Veuillez <a style="color: #059A6D;" href="{host}/password/reset_password/{token}">cliquer ici</a> pour réinitialiser votre mot de passe.</p></div>
            </div>
        </body>
    </html>
    """