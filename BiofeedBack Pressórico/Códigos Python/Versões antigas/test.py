def altura_col (tipo):
    alturas=[]
    with open ("recorde/"+str(tipo), "r") as arquivo:
        for linha in arquivo:
            valores = linha.split()
            alturas.append(valores)
    arquivo.close()
    return(alturas)
teste=[]
tipe="Recorde"
teste=altura_col(tipe)
print(teste[1][1])

