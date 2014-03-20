def a():
    print 'a'
    b()
def b():
    print 'b'
    a()

if __name__=="__main__":

    a()
