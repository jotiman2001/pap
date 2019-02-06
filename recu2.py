

# it = iter(a)
#
# def f(iterator):
#     try:
#         elem = iterator.__next__()
#         for i in list(range(elem[1])):
#             print(elem[0],i)
#             f(iterator)
#     except StopIteration: # alle elemente aus a durch
#         print()
#         return
#
# f(it)


#------------------------------------------------



a=[("a",2),("b",3)]
c=[]
def f(a,i,lista):
    global c
    elem = a[i]
    list_number_of_clicks = range(1,elem[1]+1)
    ID = elem[0]

    for clicks in list_number_of_clicks:

        tupla=(ID,clicks)
        lista1 = lista.copy()
        lista1.append(tupla)

        if (i+1 < len(a)):
            f(a,i+1,lista1)
        else:
            # print(lista1)
            c.append(lista1)



result = f(a,0,[])
print(result)
for x in c:
    print(x)


#-------------------------------------

#
# a = [(3, 2), (14, 4), (23, 2)]
#
# b = []
# c = []
# le = len(a)
#
#
# def f(laenge):
#     global b
#     global c
#     x = laenge - 1
#
#     if (x < 0):
#         print(b)
#         c.append(b)
#         b = []
#         return
#
#     else:
#         elem = a[x]
#         for i in list(range(elem[1])):
#             # print((elem[0], i))
#             b.append((elem[0], i))
#             f(laenge - 1)
#
#
#
# f(le)
# print(c)
