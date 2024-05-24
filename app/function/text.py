import re
from markupsafe import escape
from html_sanitizer import Sanitizer

def from_custom_texte(texte):

    # remplacement couleur
    def r_color(texte):
        pattern = r'{#([0-9A-Fa-f]{6}):(.*?)}'
        def remplacer(match):
            couleur = match.group(1)
            contenu = match.group(2)
            return f'<span style="color: #{couleur};">{contenu}</span>'
        
        return re.sub(pattern, remplacer, texte)
    
    # remplacement taille
    def r_size(texte):
        pattern = r'{%((?:\d+\.\d+)|(?:\d+)):(.*?)}'
        def remplacer(match):
            size = match.group(1)
            if float(size) > 3:
                size = "3"
            if float(size) < 0.5:
                size = "0.5"
            contenu = match.group(2)
            return f'<span style="font-size: calc({size}*max(0.85vw,10px));">{contenu}</span>'
        
        return re.sub(pattern, remplacer, texte)
    
    # remplacement lien
    def r_link(texte):
        pattern = r'{\?"(.*?)":(.*?)}'
        def remplacer(match):
            link = match.group(1)
            contenu = match.group(2)
            return f"<a href=\"{link}\">{contenu}</a>"
        
        return re.sub(pattern, remplacer, texte)

    sanitizer = Sanitizer({
        'tags': {'madeup'},
        'attributes': {
            'madeup': set(),
        },
        'empty': set(),
        'separate': set(),
        'whitespace': set(),
        'keep_typographic_whitespace': True,
        'autolink' : False,    
    })


    cleaned_text = texte
    traitements = [r_color, r_size, r_link]
    for traitement in traitements:
        cleaned_text = traitement(cleaned_text)
    
    auto_link = Sanitizer({
        'tags': {'span','a'},
        'attributes': {
            'span': {'style'},
            'a': {'href','title'},
        },
        'empty': set(),
        'separate': set(),
        'whitespace': set(),
        'keep_typographic_whitespace': True,
        'autolink' : True,
        'is_mergeable': lambda e1, e2 :False, 
    })
    print(cleaned_text)
    print(auto_link.sanitize(cleaned_text))
    return auto_link.sanitize(cleaned_text)

 
def to_custom_texte(texte):

    # remplacement couleur
    def r_color(texte):
        pattern = r'<span style="color: #([0-9A-Fa-f]{6});">(.*?)</span>'
        def remplacer(match):
            couleur = match.group(1)
            contenu = match.group(2)
            return '{'+f'#{couleur}:{contenu}'+'}'
        
        return re.sub(pattern, remplacer, texte)
    
    # remplacement taille
    def r_size(texte):
        pattern =r'<span style="font-size: calc\(([^*]+)\*max\(0.85vw,10px\)\);">(.*?)</span>'
        def remplacer(match):
            size = match.group(1)
            contenu = match.group(2)
            return '{'+f'%{size}:{contenu}' +'}'
        
        return re.sub(pattern, remplacer, texte)
    
    # remplacement lien
    def r_link(texte):
        pattern =r'<a href="(.*?)">(.*?)</a>'
        def remplacer(match):
            link = match.group(1)
            contenu = match.group(2)
            return '{'+f'?\"{link}\":{contenu}'+'}'
        
        return re.sub(pattern, remplacer, texte)

    sanitizer = Sanitizer({
        'tags': {'madeup'},
        'attributes': {
            'madeup': set()
        },
        'empty': set(),
        'separate': set(),
        'whitespace': set(),
        'keep_typographic_whitespace': True,
        'autolink' : True       
    })

    stored_text = texte
    traitements = [r_color, r_size, r_link]
    for traitement in traitements:
        stored_text = traitement(stored_text)

    return sanitizer.sanitize(stored_text)