from datetime import date

def datenow():
    today= date.today()
    return today.strftime("%d/%m/%Y")