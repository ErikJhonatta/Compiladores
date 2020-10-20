from Lexer.Scanner import Scanner
from Parser.Parser import Parser
import sys
if __name__ == "__main__":
    path = sys.argv[1]
    try:
        fonte = open(path, 'r')
        programa = ''.join(fonte.readlines())
        fonte.close()
    except Exception:
        print("Código Fonte não encontrado")
        sys.exit(1)

    lexer = Scanner(programa)
    tabtokens = lexer.scan()
    # for i in tabtokens:
    # 	print(i)
    parser = Parser(tabtokens)
    try:
        parser.start()
    except Exception as e:
        print(e)

    for i in parser.tabSimbolos:
        print(i)

    # print('-------------------------------')

    # for i in parser.tabTresEnderecos:
    #     print(i)