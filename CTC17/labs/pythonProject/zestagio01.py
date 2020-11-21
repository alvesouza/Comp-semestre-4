def ordenar_lista(lista):
    # escreva seu codigo aqui
    return sorted(lista, key=lambda x:(x[0]))

if __name__ == '__main__':
    numero_de_entradas = int(input())
    lista = []
    for i in range(numero_de_entradas):
        primeiro_valor, segundo_valor = input().split()
        primeiro_valor, segundo_valor = int(primeiro_valor), int(segundo_valor)
        lista.append((primeiro_valor, segundo_valor))

    lista = ordenar_lista(lista)

    for item in lista:
        print(item[0], item[1])