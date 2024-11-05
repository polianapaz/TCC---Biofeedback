import matplotlib.pyplot as plt

eixo_x = []
for i in range(146):
    eixo_x.append(i/146)
eixo_y = []
graf=[]
for i in range(48):
    ba=0.4*i/48
    graf.append(round( ba, 4))
for i in range(50):
    ba=0.4
    graf.append(round( ba, 4))
for i in range(48):
    ba=0.4*(1-i/48)
    graf.append(round( ba, 4))        
arq_nome = ("graficos/Trabalho Isométrico a 40%aa.txt")
arquivo_result = open(arq_nome , "+a")
for pt in range(len(graf)):
    arquivo_result.write(str(graf[pt])+" ")
arquivo_result.close()
eixo_y = graf
fig, ax = plt.subplots()
ax.plot(eixo_x, eixo_y)
plt.show()
