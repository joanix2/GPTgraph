from interface.Win import MainWin
from noyaux.kernel import Kernel

def main():
    kern = Kernel()
    root = MainWin(kern)
    root.mainloop()

if __name__ == '__main__':
    main()