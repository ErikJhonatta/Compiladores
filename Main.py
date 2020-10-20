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
    parser = Parser(tabtokens,True)
    #False = Boolean pode receber int - diferente de 0 é true| e vice e versa
    #True  = Boolean só recebe boolean | e vice e versa
    try:
        parser.start()
    except Exception as e:
        print(e)

    for i in parser.tabSimbolos:
        print(i)

    # print('-------------------------------')

    # for i in parser.tabTresEnderecos:
    #     print(i)
    parser.gerarArqCod()