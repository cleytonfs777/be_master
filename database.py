import sqlite3

class Agendador:
    def __init__(self, arquivo):
        self.conn = sqlite3.connect(arquivo)
        self.cursor = self.conn.cursor()
    
    def carrega_lista(self):
        self.cursor.execute('SELECT * FROM agendador')
        linhas = []
        for linha in self.cursor.fetchall():
            linhas.append(linha[1])
        return linhas

    def salva_lista(self, lista_carrega):
        consulta1 = 'DELETE FROM agendador'
        self.cursor.execute(consulta1,)
        consulta2 = 'INSERT OR IGNORE INTO agendador (data_hora) VALUES (?)'
        for item in lista_carrega:
            self.cursor.execute(consulta2, (f"{item}",))
            self.conn.commit()

    def apaga_lista(self):
        consulta1 = 'DELETE FROM agendador'
        self.cursor.execute(consulta1,)
        self.conn.commit()

    def fechar(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":

    lista = ["09/08/2024 14:00", "24/07/2024 11:20",
             "xx/11/2024 07:09", "01/09/2024 09:48", "27/05/2024 14:30", "27/05/2024 14:30", "27/05/2024 14:30", "27/05/2024 14:30", "xx/05/2024 14:30"]

    agenda = Agendador('bedatabase.db')
    agenda.salva_lista(lista)
    # agenda.apaga_lista()
    print(agenda.carrega_lista())
    agenda.fechar()
