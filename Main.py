from Lexer.Scanner import Scanner
import sys
if __name__ == "__main__":
    path = sys.argv[1]
    try:
        fonte = open(path,'r')
        programa = ''
        for i in fonte.readlines():
            programa += i
        fonte.close()
    except:
        print("Código Fonte não encontrado")
        exit(1)

    lexer = Scanner(programa)
    tabTokens = lexer.scan()
    for i in tabTokens:
        print(i)