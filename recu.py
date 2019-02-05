

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



a=[(3,2),(14,2),(33,2)]

le = len(a)

def f(laenge):
    x=laenge-1
    elem = a[x]
    if (x < 0):
        # print(b)
        # c.append(b)
        # b=[]
        return (elem[0])

    else:

        liste_der_klicks = list(range(elem[1]))
        for i in liste_der_klicks:

            print((elem[0], i+1))

        return f(laenge-1)


f(le)



#-------------------------------------


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
