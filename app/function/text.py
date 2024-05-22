import re
from markupsafe import escape

def from_custom_texte(texte):
    # Utilisation d'une expression régulière pour trouver les balises spécifiées
    pattern = r'{#([0-9A-Fa-f]{6})%(\d+):([^}]*)}'
    
    # Fonction de remplacement pour re.sub()
    def remplacer(match):
        couleur = match.group(1)
        taille = match.group(2)
        contenu = match.group(3)
        if int(taille) > 7:
            taille = "7"
        return f'<font color="#{couleur}" size={taille}>{contenu}</font>'
    
    # Remplacer les balises spécifiées par les balises HTML appropriées
    
    texte_html = re.sub(pattern, remplacer, escape(texte))

    
    return texte_html
 
def to_custom_texte(texte_html):
    # Expression régulière pour trouver les balises <font>
    pattern = r'<font color="([^"]*)" size=(\d+)>(.*?)</font>'

    # Fonction de remplacement pour re.sub()
    def remplacer(match):
        couleur = match.group(1)
        taille = match.group(2)
        contenu = match.group(3)
        return "{"+f'{couleur}%{taille}:{contenu}'+"}"
    
    # Remplacer les balises <font> par la forme spécifiée
    texte_converti = re.sub(pattern, remplacer, texte_html)
    
    return texte_converti