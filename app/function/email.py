from app.config import host

def reset_message(token):
    return f"""
        <html>
            <body>
                <div style="background-color: #060606;">
                    <div style=" margin-left: auto; margin-right: auto; width: 50vw;"><h1 style="font-weight: bold; text-decoration: none; color: #FFF; font: normal 800 2.5vw normal Arial,Helvetica,sans-serif; text-align: center;">Réinitialisation du mot de passe</h1></div>
                    <div style="margin-left: auto; margin-right: auto; margin-top: 10vh; margin-bottom: 2vh; padding: 50px; width: fit-content; height: fit-content; background-color: #424242; border-radius: 25px;"><p style="color: #FFF; font: normal 800 1vw normal Arial,Helvetica,sans-serif;"> Veuillez <a style="color: #059A6D;" href="{host}/password/reset_password/{token}">cliquer ici</a> pour réinitialiser votre mot de passe.</p></div>
                </div>
            </body>
        </html>
    """