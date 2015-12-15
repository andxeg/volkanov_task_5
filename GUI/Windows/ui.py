from PyQt4 import uic
import os

def clear(name, num):
    f = open(name, "r")
    s = f.readlines()
    s = s[num:]
    f.close()
    f = open(name, "w")
    for s0 in s:
        f.write(s0)
    f.close()

if __name__ == "__main__":
    for s in os.listdir(os.curdir):
        if s.endswith(".ui"):
            fin = open(s, "r")
            fout = open("ui_" + s.replace(".ui", ".py"), "w")
            print("Building " + s + "...")
            #uic.compileUi(fin, fout, from_imports=True)
            uic.compileUi(fin, fout)
            fin.close()
            fout.close()
            clear("ui_" + s.replace(".ui", ".py"), 8)

    os.system("pyrcc4 -py3 resources.qrc -o resources_rc.py")
    clear("resources_rc.py", 8)
        
