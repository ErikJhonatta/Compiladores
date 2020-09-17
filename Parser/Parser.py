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
                        return #VERIFICAR
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico Ponto e virgula Var declaracao na linha '+str(self.tokenAtual().linha))
                else:
                    self.erro = True
                    raise Exception('Erro sintatico Atribuicao Var declaracao na linha '+str(self.tokenAtual().linha))
            else:
                self.erro = True
                raise Exception('Erro sintatico Identificador Var declaracao na linha '+str(self.tokenAtual().linha))
        #TODO: resto das variaveis do statement, fora <var-declaracao>

        elif(self.tokenAtual().tipo == 'FUNC'):#tipo função
            self.indexToken += 1
            if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'TBOOLEAN'):#tipo
                self.indexToken += 1
                if(self.tokenAtual().tipo == 'ID'):#identificador
                    self.indexToken += 1
                    if(self.tokenAtual().tipo == 'LBRACK'):#parentese esquerdo
                        self.indexToken += 1
                        while(self.tokenAtual().tipo != 'RBRACK'): #verificar caso em que não encontre o RBRACK
                            if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'TBOOLEAN'):#tipo
                                self.indexToken += 1
                                if(self.tokenAtual().tipo == 'ID'):#identificador
                                    self.indexToken += 1
                                    if(self.tokenAtual().tipo == 'COMMA'):#virgula para um proximo parametro
                                        self.indexToken += 1
                                    elif(self.tokenAtual().tipo == 'RBRACK'):
                                        break
                                    else:
                                        self.erro = True
                                        raise Exception('Erro sintatico virgula Func declaracao na linha '+str(self.tokenAtual().linha))    
                                else:
                                    self.erro = True
                                    raise Exception('Erro sintatico identificador Var declaracao na linha '+str(self.tokenAtual().linha))
                            else:
                                self.erro = True
                                raise Exception('Erro sintatico Tipo Var declaracao na linha '+str(self.tokenAtual().linha))
                        
                        #saiu do laço, isso significa que encontrou o RBRACK, logo, avanço um token
                        self.indexToken += 1
                        if(self.tokenAtual().tipo == 'LCBRACK'):#chave esquerda
                            while(self.tokenAtual().tipo != 'RCBRACK'): #verificar caso em que não encontra o RCBRACK
                                self.indexToken += 1
                                return self.statement()#chamo recursivamente para verificar os stmts contidos dentro do escopo da função
                                #fazer parte do RETURN
                        else:
                            self.erro = True
                            raise Exception('Erro sintatico Chave esquerda da Funcao declaracao na linha ' + str(self.tokenAtual().linha))
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico Parentese esquerdo da Funcao declaracao na linha ' + str(self.tokenAtual().linha))
                else:
                    self.erro = True
                    raise Exception('Erro sintatico Identificador da Funcao declaracao na linha ' + str(self.tokenAtual().linha))
            else:
                self.erro = True
                raise Exception('Erro sintatico Tipo da Funcao declaracao na linha ' + str(self.tokenAtual().linha)) 
            
        else:
            self.erro = True
            raise Exception('Erro sintatico Token fora do statement na linha '+str(self.tokenAtual().linha))
    def expression(self):
        if(self.tokenAtual().tipo == 'NUMBER'):#<numero> que pode occorrer só, na aritmetica ou na logica
            if (not (self.lookAhead().tipo == 'EQUAL' or self.lookAhead().tipo == 'DIFF' or self.lookAhead().tipo == 'LESS' or self.lookAhead().tipo == 'LESSEQUAL' or self.lookAhead().tipo == 'GREAT' or self.lookAhead().tipo == 'GREATEQUAL')):# Se nao tiver simbolo de expressao logica
                #checa simbolo de op aritmetica
                if(not (self.lookAhead().tipo == 'SUM' or self.lookAhead().tipo == 'SUB' or self.lookAhead().tipo == 'DIV' or self.lookAhead().tipo == 'MUL')):#Se nao tiver simbolo de expressao aritmetica
                    #Entra aqui se for apenas numero
                    self.indexToken +=1
                    return
                else:#Se tiver simbolo aritmetico
                    self.indexToken+=1 # Em cima do simbolo aritmetico
                    if(self.lookAhead().tipo == 'NUMBER' or self.lookAhead().tipo == 'ID'):
                        self.indexToken +=2 #Token depois do numero
                        return
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico numero op ?, (arithmetic expression) na linha '+str(self.tokenAtual().linha))
            else: #Se tiver simbolo de expressao logica
                self.indexToken +=1 # Em cima do simbolo logico (op-condicional)
                if(self.lookAhead().tipo == 'NUMBER' or self.lookAhead().tipo == 'ID'):
                    self.indexToken +=2 # Passa para o token depois do numero
                    return
                else:
                    self.erro = True
                    raise Exception('Erro sintatico numero op ?, (logical expression) na linha '+str(self.tokenAtual().linha))
        
        if(self.tokenAtual().tipo == 'BOOLEAN'):# Se a expressão for só um boolean
            self.indexToken +=1
            return

        if(self.tokenAtual().tipo == 'ID'):# Identificador de Função e Variável
            self.indexToken +=1
            return

        
    def lookAhead(self):
        return self.tabTokens[self.indexToken + 1]