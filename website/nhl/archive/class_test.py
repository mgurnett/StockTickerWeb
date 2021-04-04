class Single():
    def __init__(self, left, right):
        self.left=left
        self.right=right

    def __str__ (self):
        return (f'left= {self.left} and right= {self.right}')

class CollectionOfSingles():
    def __init__(self, SingleObjects):
        self.singles = list(SingleObjects) #the cast here is to indicate that some checks would be nice
        # Here is where you could put the save function like pickle.

a = Single("a", "b")
b = Single("c", "d")
c = Single("e", "f")

objectarray = CollectionOfSingles([a, b, c])
print (objectarray.singles[0])
'''
[<__main__.Single object at 0x00000000034F7D68>, 
<__main__.Single object at 0x00000000035592E8>, 
<__main__.Single object at 0x0000000003786588>]
and you could also append additional ones directly:
'''
objectarray.singles.append(Single("g", "d"))
objectarray.singles
'''
[<__main__.Single object at 0x00000000034F7D68>, 
<__main__.Single object at 0x00000000035592E8>, 
<__main__.Single object at 0x0000000003786588>, 
<__main__.Single object at 0x0000000003786828>]
implementing __repr__ or __str__ helps make the print nicer.
'''
for i in objectarray.singles:
    print (i)