def filtrar_lista(lista):
    # escreva seu codigo aqui
    filtada = []
    for x in lista:
        # print(x)
        if x[1] == "true":
            # print(x[1])
            # print(x[0])
            filtada.append((x[0], x[1]))
    return filtada
numero_de_entradas = int(input())
lista = []
for i in range(numero_de_entradas):
    nome, cliente = input().split()
    lista.append((nome, cliente))

lista_filtrada = filtrar_lista(lista)

for item in lista_filtrada:
    print(item[0])