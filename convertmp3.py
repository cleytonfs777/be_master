import os

def convert_mp3():

    caminho_m = "/home/cleyton/Área de Trabalho/TESTES/audios"
    master_path = os.walk(caminho_m)

    for f_caminho in master_path:
        if len(f_caminho[-1]) != 0:
            for arq in f_caminho[-1]:
                cam_ends = os.path.join(f_caminho[0], arq)
                print(cam_ends)
                os.system(f"ftransc -f mp3 {cam_ends}")
                


        
        
        # rec_caminho = os.listdir(os.path.join(caminho_m, f_caminho))

        # for s_caminho in rec_caminho:
        #     try:
        #         arqqs = os.listdir(os.path.join(caminho_m, f_caminho, s_caminho))
        #         for aarr in arqqs:
        #             finn = os.path.join(s_caminho, aarr)
        #             print(finn)
        #             os.remove(os.path.join(caminho_m, f_caminho, s_caminho, aarr))
        #     except Exception as e:
        #         print(e)

if __name__ == "__main__":
    convert_mp3()













# lista = ["listados/teste.3gp", "listados/teste2.3gp"]

# for inter in lista:
#     os.system(f"ftransc -f mp3 {inter}")
#     os.system(f"ftransc -f mp3 {inter}")
