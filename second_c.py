from PyQt5 import uic,QtWidgets
from PyQt5.QtCore import *
from datetime import datetime, timedelta
from time import sleep, time
from database import Agendador
import re
import shutil
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import sys
import os
import setup
# from convertmp3 import *
from selenium.webdriver import Keys, ActionChains
from dotenv import load_dotenv

load_dotenv()


# from selenium.webdriver.firefox.options import Options as FirefoxOptions


class MySecondApp(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi("IIprojeto.ui", self)
        self.inputData2.setMaxLength(10)
        self.inputData2.setInputMask('99/99/9999')
        self.inputInit2.setMaxLength(5)
        self.inputInit2.setInputMask('99:99')
        self.inputF2.setMaxLength(5)
        self.inputF2.setInputMask('99:99')
        self.bntHoje2.clicked.connect(self.dia_hoje)
        self.btnAma2.clicked.connect(self.dia_amanha)
        self.btn3m2.clicked.connect(self.tempo_3m)
        self.btn5m2.clicked.connect(self.tempo_5m)
        self.btn10m2.clicked.connect(self.tempo_10m)
        self.btn15402.clicked.connect(self.tempo_15_40)
        self.btn23002.clicked.connect(self.tempo_23_00)
        self.btn90302.clicked.connect(self.tempo_09_30)
        self.btnClean.clicked.connect(self.limpar)
        self.btnInsertList.clicked.connect(self.addList)
        self.btnListPush.clicked.connect(self.pushList)
        self.btnListSave.clicked.connect(self.saveList)
        self.btnClearBank.clicked.connect(self.clear_bank)
        self.btnIDelList.clicked.connect(self.delete_selected)
        self.btnSeleciona.clicked.connect(self.select_caminho)
        self.btnInitR.clicked.connect(self.registro_be)
        self.btnOrdenar.clicked.connect(self.ord_files)
        self.btnDownload.clicked.connect(self.download_files)
        self.btnToDrive.clicked.connect(self.sync_drive)
        self.btnconvert.clicked.connect(self.convert_now)
        self.btn_convmp3.clicked.connect(self.mp3_comp)
        self.btnClearBe.clicked.connect(self.apaga_baixados)
        self.btnRemove.clicked.connect(self.remove_token)
        self.pushList()
        self.set_message("")
        self.inputCaminho.setText(os.getenv('WAY_INPUT'))
     
    def set_message(self, msg):
        self.labelSaida.setText(msg)

    def dia_hoje(self):
        diah = datetime.now()
        diah_s = diah.strftime("%d/%m/%Y")
        self.inputData2.setText(diah_s)

    def dia_amanha(self):
        diam = datetime.now() + timedelta(days=1)
        diam_s = diam.strftime("%d/%m/%Y")
        self.inputData2.setText(diam_s)

    def tempo_3m(self):
        temp3 = datetime.now() + timedelta(minutes=3)
        temp3_s = temp3.strftime("%H:%M")
        self.inputInit2.setText(temp3_s)

    def tempo_5m(self):
        temp5 = datetime.now() + timedelta(minutes=5)
        temp5_s = temp5.strftime("%H:%M")
        self.inputInit2.setText(temp5_s)

    def tempo_10m(self):
        temp10 = datetime.now() + timedelta(minutes=10)
        temp10_s = temp10.strftime("%H:%M")
        self.inputInit2.setText(temp10_s)

    def tempo_15_40(self):
        timmes = "15:40"
        self.inputF2.setText(timmes)

    def tempo_23_00(self):
        timmes1 = "23:00"
        self.inputF2.setText(timmes1)

    def tempo_09_30(self):
        timmes2 = "09:30"
        self.inputF2.setText(timmes2)

    def limpar(self):
        self.inputData2.setText("")
        self.inputInit2.setText("")
        self.inputF2.setText("")
        self.listWidget.clear()
        self.set_message("Limpeza realizada com sucesso!!")

    def addList(self):
 
        self.dat_i = self.inputData2.text()
        self.hor_i = self.inputInit2.text()
        self.hor_t = self.inputF2.text()

        print("Inicializando adição...")
        self.data_hora_i = self.dat_i + " " + self.hor_i
        self.data_hora_t = 0

        if datetime.strptime(self.hor_i, '%H:%M') < datetime.strptime(self.hor_t, '%H:%M'):
            self.data_hora_t = self.dat_i + " " + self.hor_t
        else:
            arr = self.dat_i.split('/')
            new = str(int(arr[0]) + 1)
            self.dat_f = self.dat_i.replace(arr[0], new)
            self.data_hora_t = self.dat_f + " " + self.hor_t

        
        self.data_hora_i = datetime.strptime(self.data_hora_i, '%d/%m/%Y %H:%M')
        self.data_hora_t = datetime.strptime(self.data_hora_t, '%d/%m/%Y %H:%M')


        lista = []
        data_hora_n = self.data_hora_i
        try:
            while data_hora_n < self.data_hora_t:
                lista.append(datetime.strftime(data_hora_n, '%d/%m/%Y %H:%M'))
                data_hora_n = data_hora_n + timedelta(minutes=21)
            self.set_message("Lista Gerada com sucesso")
        except:
            self.set_message("Falha ao Gerar lista")
        for icone in lista:
            self.listWidget.addItem(icone)

    def pushList(self):
        self.listWidget.clear()
        self.agenda = Agendador('bedatabase.db')
        lista = self.agenda.carrega_lista()
        for icone in lista:
            self.listWidget.addItem(icone)
        self.agenda.fechar()
        self.set_message("Lista carregada com sucesso!!")

    def saveList(self):
        myarr = []
        self.agenda = Agendador('bedatabase.db')
        for i in range(0, self.listWidget.count()):
            try:
               myarr.append(self.listWidget.item(i).text())
            except:
                self.listWidget.addItem("Falha ao salvar lista")
        self.set_message("Sua lista foi salva no Banco de Dados")

        self.agenda.salva_lista(myarr)
        self.agenda.fechar()

    def clear_bank(self):
        self.agenda = Agendador('bedatabase.db')
        self.agenda.apaga_lista()
        self.set_message("Banco de dados apagado com sucesso!!")

    def delete_selected(self):
        self.listWidget.takeItem(self.listWidget.currentRow())
        self.set_message("Item apagado com sucesso!!")

    def select_caminho(self):
        arquivo = QtWidgets.QFileDialog.getExistingDirectory(
            None, "Onde Salvar os Audios", os.getenv('WAY_INPUT'))
        self.inputCaminho.setText(arquivo)

    def formataTimestamp(self, timest):

        lista1 = timest[0:-3]
        lista2 = timest[-3:]
        list_c = f"{lista1}.{lista2}"
        numb_main = float(list_c)
        print(numb_main)
        numb_main = numb_main - 60*20
        result = datetime.fromtimestamp(numb_main).strftime(
            '%d/%m %H:%M')
        retult2 = result.replace(":", ".").replace(" ", "_").replace("/", ".")

        return retult2

    def registro_be(self):
        self.limpa_tela()
        myarr = []
        for i in range(0, self.listWidget.count()):
            try:
               myarr.append(self.listWidget.item(i).text())
            except:
                self.listWidget.addItem("Falha ao salvar lista")
        self.set_message("Sua lista foi gerada")
        print(myarr)
        self.worker = WorkerThread(myarr)
        self.worker.start()
        self.worker.finished.connect(self.evt_worker_finished)
        self.worker.update_progress.connect(self.evt_update_progress)
        self.worker.update_rotulo.connect(self.evt_update_label)

    def ord_files(self):

        caminho = self.inputCaminho.text()

        def formataTimestamp(timest):

            lista1 = timest[0:-3]
            lista2 = timest[-3:]
            list_c = f"{lista1}.{lista2}"
            numb_main = float(list_c)
            # print(numb_main)
            numb_main = numb_main - 60*20
            result = datetime.fromtimestamp(numb_main).strftime(
                '%d/%m %H:%M')
            retult2 = result.replace(":", ".").replace(
                " ", "_").replace("/", ".")

            return retult2

        def more_tests(arr, caminho):

            for names in arr:
                try:

                    os.mkdir(os.path.join(caminho, names))
                except:
                    print("Arquivo já existe")

        def cria_pathmain(caminho):
            meses = {
                "01": "01.JANEIRO",
                "02": "02.FEVEREIRO",
                "03": "03.MARÇO",
                "04": "04.ABRIL",
                "05": "05.MAIO",
                "06": "06.JUNHO",
                "07": "07.JULHO",
                "08": "08.AGOSTO",
                "09": "09.SETEMBRO",
                "10": "10.OUTUBRO",
                "11": "11.NOVEMBRO",
                "12": "12.DEZEMBRO"
            }

            for item in os.listdir(caminho):
                try:
                    mes = re.findall(r'\.\d\d', item)[0].replace(".", "")
                    pas_atual = meses[mes]
                    old_cam = os.path.join(caminho, item)
                    new_caminh = os.path.join(caminho, pas_atual)
                    if pas_atual in os.listdir(caminho):
                        print("Pasta já existe, mover para ela")
                        shutil.move(old_cam, new_caminh)
                    else:
                        print("Deve criar a pasta")
                        os.mkdir(new_caminh)
                        shutil.move(old_cam, new_caminh)
                except:
                    pass

        def converteBaixado(caminho):

            itens = os.listdir(caminho)
            arrii = []
            cont = 1
            try:
                for item in itens:
                    item_n = re.findall(r"upload_\d+\.3gp",
                                        item)[0].replace("upload_", "").replace(".3gp", "")

                    item_n = formataTimestamp(item_n)
                    os.rename(os.path.join(caminho, item), os.path.join(
                        caminho, f"{item_n}.3gp"))
                    cont += 1
            except:
                pass

            # CRIA AS PASTAS PARA RECEBER OS ARQUIVOS 3GP CRIADOS
            try:
                for iitt in os.listdir(caminho):
                    arrii.append(re.findall(r"\d+\.\d+_", iitt)
                                 [0].replace("_", ""))
                more_tests(list(set(arrii)), caminho)
            except:
                pass

            # MOVE TODOS OS ARQUIVOS BAIXADOS PARA SUAS RESPECTIVAS PASTAS
            try:
                print("passei aqui")
                for item in os.listdir(caminho):
                    new_cam = os.path.join(caminho, item)
                    if(os.path.isfile(new_cam)):
                        origem = new_cam
                        destino = os.path.join(caminho, re.findall(
                            r"\d+\.\d+_", item)[0].replace("_", ""))

                        shutil.move(origem, destino)
            except:
                print("Falha ao mover o arquivo...")

            # CRIA A PASTA COM OS MESES BASEADO NAS PASTAS
            cria_pathmain(caminho)
        converteBaixado(caminho)

    def download_files(self):

        self.limpa_tela()

        self.dowloader = DowloaderThread(self.inputCaminho.text())
        self.dowloader.start()
        self.dowloader.finished.connect(self.dowload_finished)
        self.dowloader.update_progress_d.connect(self.evt_update_progress)
        self.dowloader.update_rotulo_d.connect(self.evt_update_label)

    def evt_worker_finished(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(
            "Todos os registros foram implementadas com sucesso!!")
        msgBox.setWindowTitle("Registros AUD")
        msgBox.setStyleSheet(
            "color: white; font-weight: bold; text-align: center; font-size:14px; background-color: #21222c")
        msgBox.exec()

    def dowload_finished(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(
            "Downloads realizados com sucesso!!")
        msgBox.setWindowTitle("Downloads Completos")
        msgBox.setStyleSheet(
            "color: white; font-weight: bold; text-align: center; font-size:14px; background-color: #21222c")
        msgBox.exec()

    def sync_finished(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(
            "Todos os arquivos da pasta foram sincronizados com sucesso!!")
        msgBox.setWindowTitle("Sincronização Concluida")
        msgBox.setStyleSheet(
            "color: white; font-weight: bold; text-align: center; font-size:14px; background-color: #21222c")
        msgBox.exec()

    def clear_finished(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(
            "Todos os arquivos baixados foram apagados com sucesso!!")
        msgBox.setWindowTitle("Limpeza Concluida")
        msgBox.setStyleSheet(
            "color: white; font-weight: bold; text-align: center; font-size:14px; background-color: #21222c")
        msgBox.exec()

    def evt_update_progress(self, val):
        self.progressBar.setValue(val)

    def evt_update_label(self, val):
        self.labelSaida.setText(val)

    def sync_drive(self):
        self.limpa_tela()
        self.sync_ = SyncThread(self.inputCaminho.text())
        self.sync_.start()
        self.sync_.finished.connect(self.sync_finished)
        self.sync_.update_progress_s.connect(self.evt_update_progress)
        self.sync_.update_rotulo_s.connect(self.evt_update_label)

    def clear_drive(self):
        self.limpa_tela()

    def convmp3_finished(self):

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(
            "Conversão realizada com sucesso!!")
        msgBox.setWindowTitle("Conversão para mp3")
        msgBox.setStyleSheet(
            "color: white; font-weight: bold; text-align: center; font-size:14px; background-color: #21222c")
        msgBox.exec()

    def mp3_comp(self):
        self.limpa_tela()
        caminho_m = os.getenv('WAY_INPUT')
        master_path = os.walk(caminho_m)
        axx = []
        cttt = [x[-1] for x in master_path if len(x[-1]) != 0]
        for ct in cttt:
            axx += ct
        print(len(axx))
        counterII = 0
        self.labelSaida.setText(f"Convertendo arquivos para mp3")
        self.convMp3(caminho_m, len(axx))
        self.convmp3_finished()

    def convMp3(self, caminho, total):

        caminho_m = caminho
        counterII = 0
        master_path = os.walk(caminho_m)
        for f_caminho in master_path:
            if len(f_caminho[-1]) != 0:
                for arq in f_caminho[-1]:
                    cam_ends = os.path.join(f_caminho[0], arq)
                    print(cam_ends)
                    os.system(f"ftransc -f mp3 {cam_ends}")
                    os.remove(cam_ends)
                    counterII += 1
                    self.progressBar.setValue((counterII*100)/total)

    def convert_now(self):
        #Obter todos os arquivos da tela
        myarr = []
        for i in range(0, self.listWidget.count()):
            try:
               myarr.append(self.listWidget.item(i).text())
            except:
                self.listWidget.addItem("Falha ao salvar lista")
        # self.set_message("Sua lista foi salva no Banco de Dados")
        # print(myarr)
        for it in range(0, len(myarr)):
            item_n = myarr[it].split(" ")
            diahw = datetime.now()
            diahw = diahw.strftime("%d/%m/%Y")
            myarr[it] = f"{diahw} {item_n[1]}"
        self.listWidget.clear()
        for icone in myarr:
            self.listWidget.addItem(icone)

    def limpa_tela(self):
        self.progressBar.setValue(0)
        self.labelSaida.setText("")

    def apaga_baixados(self):
        self.limpa_tela()
        self.clear_ = ClearThread()
        self.clear_.start()
        self.clear_.finished.connect(self.clear_finished)
        self.clear_.update_progress_c.connect(self.evt_update_progress)
        self.clear_.update_rotulo_c.connect(self.evt_update_label)

    def remove_token(self):
        cami = os.getenv('WAY_INPUT_SHORT')
        miarq = os.listdir(cami)

        for mia in miarq:
            if(mia == "token.json"):
                os.remove(os.path.join(cami, mia))

class SyncThread(QThread):

    update_progress_s = pyqtSignal(int)
    update_rotulo_s = pyqtSignal(str)

    def __init__(self, caminho):
        super(QThread, self).__init__()
        self.caminho = caminho

    def run(self):

        pasta_main = os.getenv('ID_MAIN_DIR')
        my_drive = setup.MyDrive()
        print(f" O caminho da pasta é: {os.listdir(self.caminho)}")
        itenslen = len(os.listdir(self.caminho))
        ccouter = 1

        self.update_rotulo_s.emit("Iniciando Sincronização. Aguarde...")
        for item_c in os.listdir(self.caminho):
            countad = 0
            lltk = True
            try:
                for item_d in my_drive.list_files(pasta_main):
                    if item_d[0].__contains__(item_c):
                        # SE A PASTA EXISTE IREI REALIZAR O UPLOAD DE TODOS OS ARQUIVOS DENTRO DELA PARA A PASTA DE MESMO NOME COM O ID
                        print(
                            f"A pasta {item_c} existe no drive na pasta {item_d}")
                        for itens in os.listdir(os.path.join(self.caminho, item_c)):
                            tester = [x for x in (my_drive.list_files(
                                item_d[1])) if x[0] == itens]
                            if len(tester) == 1:
                                print(
                                    f"subasta {tester[0][0]} exite no local seu id {tester[0][1]}")
                                for cadas in (os.listdir(os.path.join(
                                        self.caminho, item_c, tester[0][0]))):
                                    print("UPLOAD FILE")
                                    neway = os.path.join(
                                        self.caminho, item_c, tester[0][0])
                                    #
                                    my_drive.upload_file(
                                        cadas, neway, tester[0][1])

                            else:
                                print(
                                    f"{itens} subpasta não existe deve ser criada")
                                # CRIAR PASTA
                                print(
                                    f"Usar o ID {item_d[1]} com nome {itens}")
                                id_folder_n = my_drive.create_folder(
                                    itens, item_d[1])
                                print(
                                    f"O id da pasta {itens} é o id {id_folder_n}")
                                #FAZER O UPLOAD DOS ARQUIVOS PARA A PASTA
                                print("UPLOAD FILE")
                                for lissii in os.listdir(os.path.join(self.caminho, item_c, itens)):
                                    my_drive.upload_file(
                                        lissii, os.path.join(self.caminho, item_c, itens), id_folder_n)

                        lltk = False
                        break
            except:
                pass

            if lltk:
                # CRIAREI A PASTA NO DRIVE E POSTERIORMENTE FAREI O DOWNLOAD DE TODOS OS ARQUIVOS DA PASTA PELO ID
                print(
                    f"A pasta {item_c} não existe no drive usando o id {pasta_main}")
                id_folder_nn = my_drive.create_folder(item_c, pasta_main)
                print(f"Pasta {item_c} crianda com o id {id_folder_nn}")
                for itens in os.listdir(os.path.join(self.caminho, item_c)):
                    if my_drive.list_files(id_folder_nn) != []:
                        tester = [x for x in (my_drive.list_files(
                            id_folder_nn)) if x[0] == itens]
                        tama = len(tester)
                    else:
                        tama = 0
                    if tama == 1:
                        print(
                            f"subasta {tester[0][0]} exite no local seu id {tester[0][1]}")
                        for cadas in (os.listdir(os.path.join(
                                self.caminho, item_c, tester[0][0]))):
                            print("UPLOAD FILE")
                            neway = os.path.join(
                                self.caminho, item_c, tester[0][0])
                            #
                            my_drive.upload_file(
                                cadas, neway, tester[0][1])

                    else:
                        print(f"{itens} subpasta não existe deve ser criada")
                        # CRIAR PASTA
                        print(f"Usar o ID {id_folder_nn} com nome {itens}")
                        id_folder_n = my_drive.create_folder(
                            itens, id_folder_nn)
                        print(
                            f"O id da pasta {itens} é o id {id_folder_n}")
                        #FAZER O UPLOAD DOS ARQUIVOS PARA A PASTA
                        print("UPLOAD FILE")
                        for lissii in os.listdir(os.path.join(self.caminho, item_c, itens)):
                            my_drive.upload_file(
                                lissii, os.path.join(self.caminho, item_c, itens), id_folder_n)

            self.update_rotulo_s.emit(
                f"{ccouter} pastas de {itenslen} sincronizadas...")
            self.update_progress_s.emit((ccouter*100)/itenslen)
            ccouter += 1

class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    update_rotulo = pyqtSignal(str)

    def __init__(self, lista):
        super(QThread, self).__init__()
        self.lista = lista
  
    def run(self):
        self.lista
        # Inserir datas selecionadas com sucesso
        # Roda no modo oculto
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        browser = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        browser.implicitly_wait(5)

        # Para abrir o site do Bruno

        browser.get(os.getenv('BE_URL'))

        # Minhas Credenciais
        fb_name = os.getenv('BE_USER')
        fb_pass = os.getenv('BE_PASSWORD')
        # Fill credentials

        # Iniciando a realização do login
        try:
            self.update_rotulo.emit("Iniciando Login...")
            browser.find_element(By.NAME, "username").send_keys(fb_name)
            browser.find_element(By.NAME, "password").send_keys(fb_pass)
            browser.find_element(
                By.XPATH, '//*[@id="login-page"]/div/form/div[5]/div/button').click()
            browser.find_element(
                By.XPATH, '//*[@id="top-settings-btn"]/i').click()
            self.update_rotulo.emit("Login realizado com sucesso")
        except:
            self.update_rotulo.emit("Falha ao realizar login")

        browser.find_element(
            By.XPATH, '//*[@id="profile-dropdown"]/li[5]/a').click()
        browser.find_element(
            By.CSS_SELECTOR, '#tab > li:nth-child(2) > a:nth-child(1)').click()
        browser.find_element(
            By.CSS_SELECTOR, '#load_div > div:nth-child(11) > a').click()
        ntm = self.lista
        regs = len(self.lista)
        cont1 = '1200'

        self.update_rotulo.emit("Iniciando Escutas...")
        count = 0

        try:
            for num1 in ntm:
                # inserir o tipo de captura
                browser.find_element(
                    By.XPATH, '//*[@id="type"]/option[2]').click()
                # inserir data e hora
                browser.find_element(
                    By.XPATH, '//*[@id="startTime"]').send_keys(num1)
                # inserir duração
                browser.find_element(
                    By.XPATH, '//*[@id="duration"]').send_keys(cont1)
                # Clica para inserir od dados
                browser.find_element(
                    By.XPATH, '//*[@id="searchbutton"]').click()
                count += 1
                self.update_rotulo.emit(f"{count}/{regs} escutas gravadas...")
                x = (count*100)/regs
                self.update_progress.emit(x)

        except:
            self.update_rotulo.emit("Falha durante registro de audios")
            sleep(1)
            self.update_rotulo.emit(f"Ultimo gravado {num1}")

        if count == regs:
            sleep(1)
            self.update_rotulo.emit(f"{regs} áudios gravados com sucesso")
        else:
            sleep(1)
            self.update_rotulo.emit(
                f"Falha ocorriga!! Foram gravados apenas {count} registros")

class DowloaderThread(QThread):
    update_progress_d = pyqtSignal(int)
    update_rotulo_d = pyqtSignal(str)

    def __init__(self, caminho):
        super(QThread, self).__init__()
        self.caminho = caminho

    def run(self):
        self.update_rotulo_d.emit("Robô inicializado. Aguarde...")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        browser = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        browser.implicitly_wait(5)


        browser.get(os.getenv('BE_URL'))

        # Minhas Credenciais
        fb_name = os.getenv('BE_USER')
        fb_pass = os.getenv('BE_PASSWORD')

        browser.find_element(By.NAME, "username").send_keys(fb_name)

        browser.find_element(By.NAME, "password").send_keys(fb_pass)
        browser.find_element(
            By.XPATH, '//*[@id="login-page"]/div/form/div[5]/div/button').click()
        browser.find_element(By.XPATH, '//*[@id="top-settings-btn"]/i').click()
        browser.find_element(
            By.XPATH, '//*[@id="profile-dropdown"]/li[5]/a').click()
        browser.find_element(
            By.CSS_SELECTOR, '#tab > li:nth-child(2) > a:nth-child(1)').click()
        browser.find_element(
            By.CSS_SELECTOR, '#load_div > div:nth-child(11) > a').click()
        browser.find_element(
            By.XPATH, '//*[@id="limitoption"]/option[5]').click()

        # Conferir quantos arquivos posso fazer dowloader
        total_links = []
        for itt in range(1, 11):
            try:
                element = browser.find_element(
                    By.XPATH, f'//*[@id = "pagingid"]/li[{itt}]/a')
                browser.execute_script("arguments[0].click();", element)
                sleep(2)
                lingk = browser.find_elements(By.PARTIAL_LINK_TEXT, 'Ouvir')
                for item in lingk:
                    linsk = item.get_attribute("href")
                    if not("jpg" in linsk):
                        total_links.append(linsk)
                self.update_rotulo_d.emit("Iniciando o processo de Dowloads")
            except Exception as e:
                print(e)
                break
        countss = 0
        t_link_1 = len(total_links)
        for links in total_links:
            browser.get(links)
            countss += 1
            self.update_rotulo_d.emit(
                f"{countss}/{t_link_1} arquivos baixados")
            self.update_progress_d.emit((countss*100)/t_link_1)

            sleep(1)

        caminho = os.getenv('WAY_INPUT_SHORT')
        novo = self.caminho
        sleep(10)
        try:
            for item in os.listdir(caminho):
                new_cam = os.path.join(caminho, item)
                if(item.__contains__(".3gp")):
                    origem = new_cam
                    destino = os.path.join(novo, item)
                    shutil.move(origem, destino)
            self.update_rotulo_d.emit("Arquivos modidos para a pasta audios")

        except:
            self.update_rotulo_d.emit("Falha ao mover o arquivo...")
            print("Falha ao mover o arquivo...")

        sleep(2)

class ClearThread(QThread):

    update_progress_c = pyqtSignal(int)
    update_rotulo_c = pyqtSignal(str)

    def __init__(self):
        super(QThread, self).__init__()

    def run(self):
        self.update_rotulo_c.emit("Apagando baixados. Aguarde...")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        browser = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        browser.implicitly_wait(5)

        browser.get(os.getenv('BE_URL'))
        alert = Alert(browser)

        # Minhas Credenciais
        fb_name = os.getenv('BE_USER')
        fb_pass = os.getenv('BE_PASSWORD')

        browser.find_element(By.NAME, "username").send_keys(fb_name)

        browser.find_element(By.NAME, "password").send_keys(fb_pass)
        browser.find_element(
            By.XPATH, '//*[@id="login-page"]/div/form/div[5]/div/button').click()
        browser.find_element(By.XPATH, '//*[@id="top-settings-btn"]/i').click()
        browser.find_element(
            By.XPATH, '//*[@id="profile-dropdown"]/li[5]/a').click()
        browser.find_element(
            By.CSS_SELECTOR, '#tab > li:nth-child(2) > a:nth-child(1)').click()
        browser.find_element(
            By.CSS_SELECTOR, '#load_div > div:nth-child(11) > a').click()
        browser.find_element(
            By.XPATH, '//*[@id="limitoption"]/option[5]').click()
        
        ct_apaga = []

        # Conferir quantos arquivos posso fazer dowloader
        for itt in range(1, 11):
            try:
                element = browser.find_element(
                    By.XPATH, f'//*[@id = "pagingid"]/li[{itt}]/a')
                browser.execute_script("arguments[0].click();", element)
                for ctt in range(2, 52):
                    try:
                        element = browser.find_element(
                            By.XPATH, f'/html/body/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/table[2]/tbody/tr[{ctt}]/td[8]/a')
                        print(element.get_attribute('href'))
                        sleep(1)
                        ct_apaga.append(ctt-2)
                        # print(element)
                    except Exception as e:
                        print(e)
                        break
                self.update_rotulo_c.emit("Iniciando limpeza por itens...")
                countsx = 0
                for idc in ct_apaga:
                    t_link_1x = len(ct_apaga)
                    countsx += 1
                    try:
                        localidade = browser.find_element(
                            By.CSS_SELECTOR, f'#sendDelete{idc}')
                        browser.execute_script("arguments[0].click();", localidade)
                        sleep(0.2)
                        self.update_rotulo_c.emit(f"{countsx}/{t_link_1x} arquivos apagados")
                        self.update_progress_c.emit((countsx*100)/t_link_1x)
                    except Exception as e:
                        print(e)
                        break
                sleep(1)
                deletar = browser.find_element(
                    By.CSS_SELECTOR, '#ajaxdiv > div:nth-child(4) > div.floatLeft > button')
                browser.execute_script(
                    "arguments[0].click();", deletar)
                sleep(1)
                alert.accept()
                sleep(1)
            except Exception as e:
                print(e)
                break

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MySecondApp()
    mainWindow.show()
    app.exec_()