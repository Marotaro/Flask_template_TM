import re
from markupsafe import escape
from html_sanitizer import Sanitizer

def from_custom_texte(texte):
    # Utilisation d'une expression régulière pour trouver les balises spécifiées
    pattern = r'{#([0-9A-Fa-f]{6})%((?:\d+\.\d+)|(?:\d+)):(.*?)}'
    
    # Fonction de remplacement pour re.sub()
    def remplacer(match):
        couleur = match.group(1)
        taille = match.group(2)
        contenu = match.group(3)
        if float(taille) > 3:
            taille = "3"
        if float(taille) < 0.5:
            taille = "0.5" 
        return f'<span style="color: #{couleur}; font-size: calc({taille}*max(0.85vw,10px));">{contenu}</span>'
    
    sanitizer = Sanitizer({
        'tags': {'madeup', 'a'},
        'attributes': {
            'madeup': set(),
            'a': { 'href', 'title'}
        },
        'empty': set(),
        'separate': set(),
        'whitespace': set(),
        'keep_typographic_whitespace': True,
        'autolink' : True       
    })

    # Remplacer les balises spécifiées par les balises HTML appropriées

    texte_html = re.sub(pattern, remplacer, sanitizer.sanitize(texte))

    
    return texte_html
 
def to_custom_texte(texte_html):
    # Expression régulière pour trouver les balises <font>
    pattern = r'<span style="color: #([^"]*); font-size: calc\(([^*]+)\*max\(0.85vw,10px\)\);">(.*?)</span>'

    # Fonction de remplacement pour re.sub()
    def remplacer(match):
        couleur = match.group(1)
        taille = match.group(2)
        contenu = match.group(3)
        return "{"+f'#{couleur}%{taille}:{contenu}'+"}"
    
    sanitizer = Sanitizer({
        'tags': {'madeup', 'a'},
        'attributes': {
            'madeup': set(),
            'a': { 'href', 'title'}
        },
        'empty': set(),
        'separate': set(),
        'whitespace': set(),
        'keep_typographic_whitespace': True,
        'autolink' : True       
    })
    
    # Remplacer les balises <font> par la forme spécifiée
    texte_converti = sanitizer.sanitize(re.sub(pattern, remplacer, texte_html))
    
    return texte_converti