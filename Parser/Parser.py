class Parser:
    def __init__(self, tabTokens):
        self.tabTokens = tabTokens
        self.indexToken = 0
        self.erro = False
    
    def tokenAtual(self):
        return self.tabTokens[self.indexToken]

    def start(self):
        self.statement_list()
        return

    def statement_list(self):
        if(self.tokenAtual().tipo == "FIM"):
            return
        else:
            self.statement()
            self.statement_list()
            return
    
    def statement(self):
        #<var-declaracao>
        if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'TBOOLEAN'):#tipo
            self.indexToken +=1
            if(self.tokenAtual().tipo == 'ID'):#identificador
                self.indexToken +=1
                if(self.tokenAtual().tipo == 'ATTR'):#atribuicao
                    self.indexToken +=1
                    #Expression
                    self.expression()
                    if(self.tokenAtual().tipo == 'SEMICOLON'):
                        self.indexToken +=1
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico Ponto e virgula Var declaracao')
                else:
                    self.erro = True
                    raise Exception('Erro sintatico Atribuicao Var declaracao')
            else:
                self.erro = True
                raise Exception('Erro sintatico Identificador Var declaracao')
        #TODO: resto das variaveis do statement, fora <var-declaracao>
        else:
            self.indexToken +=1
            return 
    def expression(self):# Precisa atualizar o index do token, se n dá erro na função que chamou essa aqui
        print("Dentro de expression")
        if(self.tokenAtual().tipo == 'NUMBER' and not (self.lookAhead().tipo == 'EQUAL' or self.lookAhead().tipo == 'DIFF' or self.lookAhead().tipo == 'LESS' or self.lookAhead().tipo == 'LESSEQUAL' or self.lookAhead().tipo == 'GREAT' or self.lookAhead().tipo == 'GREATEQUAL')):# Se a expressao for só um numero
            self.indexToken +=1
            return
        
        if(self.tokenAtual().tipo == 'BOOLEAN'):# Se a expressão for só um boolean
            self.indexToken +=1
            return

        if(self.tokenAtual().tipo == 'ID'):# Identificador de Função e Variável
            self.indexToken +=1
            return

        #TODO: Logical Expression e Arithmetic Expression dentro da var expression

    def lookAhead(self):
        return self.tabTokens[self.indexToken + 1]