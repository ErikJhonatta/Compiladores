from Parser.Escopo import Escopo
import re
class Parser:
    def __init__(self, tabTokens):
        self.tabTokens = tabTokens
        self.indexToken = 0
        self.erro = False
        self.listaEscopos = []
        self.indexEscopoAtual = -1
        self.tabSimbolos = []
        self.indexDecVarAtual = 0 #Pra saber na semantica qual declaracao de variavel no codigo tá sendo checada
    def tokenAtual(self):
        return self.tabTokens[self.indexToken]

    def start(self):
        escopoPai = self.indexEscopoAtual
        self.indexEscopoAtual += 1
        escopoInicial = Escopo(self.indexEscopoAtual,escopoPai)
        self.listaEscopos.append(escopoInicial)
        self.statement_list()
        return

    def statement_list(self):
        if(self.tokenAtual().tipo == "FIM"):
            self.listaEscopos[0].fechar()
            return
        else:
            self.statement()
            self.statement_list()
            return
    
    def statement(self):
        #<var-declaracao>
        if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'TBOOLEAN'):#tipo
            temp = []
            temp.append('VAR')
            temp.append(self.tokenAtual().tipo)
            self.indexToken +=1
            if(self.tokenAtual().tipo == 'ID' and self.tokenAtual().lexema[0] == 'v'):#identificador var
                temp.append(self.tokenAtual().lexema)
                self.indexToken +=1
                if(self.tokenAtual().tipo == 'ATTR'):#atribuicao
                    self.indexToken +=1
                    #Expression
                    temp.append(self.expression())
                    if(self.tokenAtual().tipo == 'SEMICOLON'):
                        self.indexToken +=1
                        temp.append(self.indexEscopoAtual)
                        self.tabSimbolos.append(temp)
                        print(temp)
                        if(self.checkSemantica('VARDEC',self.indexDecVarAtual)):
                            return
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico Ponto e virgula Var declaracao na linha '+str(self.tokenAtual().linha))
                else:
                    self.erro = True
                    raise Exception('Erro sintatico Atribuicao Var declaracao na linha '+str(self.tokenAtual().linha))
            else:
                self.erro = True
                raise Exception('Erro sintatico Identificador Var declaracao na linha '+str(self.tokenAtual().linha))
            
        #<funcao-declaracao>
        elif(self.tokenAtual().tipo == 'FUNC'):#tipo função
            self.indexToken += 1
            if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'TBOOLEAN'):#tipo
                self.indexToken += 1
                if(self.tokenAtual().tipo == 'ID' and self.tokenAtual().lexema[0] == 'f'):#identificador
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
                                        if(self.tokenAtual().tipo == 'RBRACK'):
                                            self.erro = True
                                            raise Exception('Erro sintatico virgula Func declaracao na linha '+str(self.tokenAtual().linha))
                                        else:
                                            pass
                                    elif(self.tokenAtual().tipo == 'RBRACK'):
                                        self.indexToken += 1
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
                        
                        #saiu do laço, isso significa que encontrou o RBRACK
                        if(self.tokenAtual().tipo != 'LCBRACK'):
                            self.indexToken += 1
                        
                        if(self.tokenAtual().tipo == 'LCBRACK'):#chave esquerda
                            self.indexToken += 1
                            encontrouReturn = False
                            while(self.tokenAtual().tipo != 'RCBRACK'): #verificar caso em que não encontra o RCBRACK
                                if(self.tokenAtual().tipo == 'RETURN'):
                                    self.indexToken += 1
                                    encontrouReturn = True
                                    if(self.tokenAtual().tipo == 'ID'):#identificador
                                        self.indexToken += 1 
                                        if(self.tokenAtual().tipo == 'SEMICOLON' and self.lookAhead().tipo == 'RCBRACK'):#ponto e virgula seguido de uma chave direita
                                            self.indexToken += 1
                                            break
                                        else:
                                            self.erro = True
                                            raise Exception('Erro sintatico Retorno Func declaracao na linha '+str(self.tokenAtual().linha))
                                    else:
                                        self.erro = True
                                        raise Exception('Erro sintatico Retorno Func declaracao na linha '+str(self.tokenAtual().linha))
                                else:
                                    self.statement()#chamo para verificar os stmts contidos dentro do escopo da função
                            
                            if(encontrouReturn == False):
                                self.erro = True
                                raise Exception('Erro sintatico no retorno da função na linha '+str(self.tokenAtual().linha - 1))
                            
                            self.indexToken +=1

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
        
        #<procedimento-declaracao>
        elif(self.tokenAtual().tipo == 'PROC'):
            self.indexToken += 1
            if(self.tokenAtual().tipo == 'ID' and self.tokenAtual().lexema[0] == 'p'):
                self.indexToken += 1
                if(self.tokenAtual().tipo == 'LBRACK'):#parentese esquerdo
                    self.indexToken += 1
                    while(self.tokenAtual().tipo != 'RBRACK'): #obs: verificar caso em que não encontre o RBRACK
                        if(self.tokenAtual().tipo == 'INT' or self.tokenAtual().tipo == 'TBOOLEAN'):#tipo
                            self.indexToken += 1
                            if(self.tokenAtual().tipo == 'ID'):#identificador
                                self.indexToken += 1
                                if(self.tokenAtual().tipo == 'COMMA'):#virgula para um proximo parametro
                                    self.indexToken += 1
                                    if(self.tokenAtual().tipo == 'RBRACK'):
                                        self.erro = True
                                        raise Exception('Erro sintatico virgula Proc declaracao na linha '+str(self.tokenAtual().linha))
                                    else:
                                        pass
                                elif(self.tokenAtual().tipo == 'RBRACK'):
                                    self.indexToken += 1
                                    break
                                else:
                                    self.erro = True
                                    raise Exception('Erro sintatico em Proc declaracao na linha '+str(self.tokenAtual().linha))    
                            else:
                                self.erro = True
                                raise Exception('Erro sintatico identificador Var declaracao na linha '+str(self.tokenAtual().linha))
                        else:
                            self.erro = True
                            raise Exception('Erro sintatico Tipo Var declaracao na linha '+str(self.tokenAtual().linha))
                        
                    #saiu do laço, isso significa que encontrou o RBRACK
                    if(self.tokenAtual().tipo != 'LCBRACK'):
                        self.indexToken += 1
                    
                    if(self.tokenAtual().tipo == 'LCBRACK'):#chave esquerda
                        self.indexToken += 1
                        while(self.tokenAtual().tipo != 'RCBRACK'): #verificar caso em que não encontra o RCBRACK
                            if(self.tokenAtual().tipo == 'SEMICOLON' and self.lookAhead().tipo == 'RCBRACK'):#ponto e virgula seguido de uma chave direita
                                self.indexToken += 1
                                break
                            else:
                                self.statement()#chamo para verificar os stmts contidos dentro do escopo da função
                        self.indexToken += 1
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico Chave esquerda do Procedimento declaracao na linha ' + str(self.tokenAtual().linha))
                else:
                    self.erro = True
                    raise Exception('Erro sintatico Parentese esquerdo do Procedimento declaracao na linha ' + str(self.tokenAtual().linha))
            else:
                    self.erro = True
                    raise Exception('Erro sintatico Identificador do Proc declaracao na linha ' + str(self.tokenAtual().linha))
        #Puts
        elif (self.tokenAtual().tipo == 'PUTS'):
            self.indexToken +=1
            if((self.tokenAtual().tipo == 'ID' and self.tokenAtual().lexema[0] == 'v') or self.tokenAtual().tipo == 'NUMBER'):
                self.indexToken+=1
                if(self.tokenAtual().tipo == 'SEMICOLON'):# se for um numero ou var o proximo token vai ser esse semicolon
                    self.indexToken += 1
                    return
                else:
                    self.erro = True
                    raise Exception('Erro sintatico ponto e virgula no puts na linha ' + str(self.tokenAtual().linha))
            else:
                self.erro = True
                raise Exception('Erro sintatico depois do puts na linha ' + str(self.tokenAtual().linha))
        #Chamada de funcao e procedimento
        elif(self.tokenAtual().tipo == 'ID'):
            if(self.tokenAtual().lexema[0] == 'f' or self.tokenAtual().lexema[0] == 'p'):
                self.indexToken +=1
                if(self.tokenAtual().tipo == 'LBRACK'):
                    self.indexToken+=1
                    while(self.tokenAtual().tipo != 'RBRACK'):# verifica argumentos da funcao para ser chamada, nao checa tipos (semantica)
                        if(self.tokenAtual().tipo == 'NUMBER' or self.tokenAtual().tipo == 'BOOLEAN' or self.tokenAtual().lexema[0] == 'v'):#verifica se foi passado numero, boolean, ou variavel
                            self.indexToken += 1
                            if(self.tokenAtual().tipo == 'COMMA'):
                                self.indexToken +=1
                                if(self.tokenAtual().tipo == 'RBRACK'):
                                    self.erro = True
                                    raise Exception('Erro sintatico falta de argumentos na linha ' + str(self.tokenAtual().linha))
                            elif(self.tokenAtual().tipo == 'RBRACK'):
                                self.indexToken +=1
                                break
                            else:
                                self.erro = True
                                raise Exception('Erro sintatico Virgula na linha ' + str(self.tokenAtual().linha))
                        else:
                            self.erro = True
                            raise Exception('Erro sintatico argumento invalido na linha ' + str(self.tokenAtual().linha))
                    #fora do laço encontrou o RBRACK
                    if(self.tokenAtual().tipo == 'SEMICOLON'):# ponto e virgula no final da declaração do puts
                        self.indexToken +=1
                        return
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico Ponto e Virgula na linha ' + str(self.tokenAtual().linha))
                else:
                    self.erro = True
                    raise Exception('Erro sintatico parentese esquerdo chama de funcao '+str(self.tokenAtual().linha))
            else:
                self.erro = True
                raise Exception('Erro sintatico identificador chamada de funcao ou procedimento '+str(self.tokenAtual().linha))
        #IF
        elif(self.tokenAtual().tipo == 'IF'):
            self.indexToken+=1
            if(self.tokenAtual().tipo == 'LBRACK'):
                self.indexToken +=1
                self.condicao()# precisa atualizar o index dentro
                if(self.tokenAtual().tipo == 'RBRACK'):
                    self.indexToken +=1
                    if(self.tokenAtual().tipo == 'LCBRACK'):
                        self.indexToken +=1
                        while(self.tokenAtual().tipo != 'RCBRACK'):
                            self.statement()
                        #fora do laço, encontrou o RCBRACK
                        self.indexToken +=1
                        if(self.tokenAtual().tipo == 'ELSE'):
                            self.indexToken +=1
                            if(self.tokenAtual().tipo == 'LCBRACK'):
                                self.indexToken +=1
                                while(self.tokenAtual().tipo != 'RCBRACK'):
                                    self.statement()
                                self.indexToken +=1
                            else:
                                self.erro = True
                                raise Exception('Erro sintatico chaves esquerda else na linha '+str(self.tokenAtual().linha)+' '+str(self.tokenAtual().lexema))    
            
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico chaves esquerda IF na linha '+str(self.tokenAtual().linha)+' '+str(self.tokenAtual().lexema))    
            
                else:
                    self.erro = True
                    raise Exception('Erro sintatico parentese direito IF na linha '+str(self.tokenAtual().linha)+' '+str(self.tokenAtual().lexema))    
             
            else:
                self.erro = True
                raise Exception('Erro sintatico parentese esquerdo IF na linha '+str(self.tokenAtual().linha)+' '+str(self.tokenAtual().lexema))    

        elif(self.tokenAtual().tipo == 'WHILE'):
            self.indexToken += 1
            if(self.tokenAtual().tipo == 'LBRACK'):
                self.indexToken += 1
                self.condicao()
                #print(self.tokenAtual().lexema)
                if(self.tokenAtual().tipo == 'RBRACK'):
                    self.indexToken += 1
                    if(self.tokenAtual().tipo == 'LCBRACK'):
                        self.indexToken += 1
                        while(self.tokenAtual().tipo != 'RCBRACK'):
                            if(self.tokenAtual().tipo == 'BREAK' or self.tokenAtual().tipo == 'CONTINUE'):
                                self.indexToken += 1
                                if(self.tokenAtual().tipo == 'SEMICOLON'):
                                    self.indexToken += 1
                                else:
                                    self.erro = True
                                    raise Exception('Erro sintatico ponto e virgula na linha '+str(self.tokenAtual().linha)+' '+str(self.tokenAtual().lexema)) 
                            else:
                                self.statement()
                        self.indexToken += 1
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico chaves esquerda else na linha '+str(self.tokenAtual().linha)+' '+str(self.tokenAtual().lexema))         
                else:
                    self.erro = True
                    raise Exception('Erro sintatico parentese direito WHILE na linha '+str(self.tokenAtual().linha)+' '+str(self.tokenAtual().lexema))
            else:
                self.erro = True
                raise Exception('Erro sintatico parentese esquerdo WHILE na linha '+str(self.tokenAtual().linha)+' '+str(self.tokenAtual().lexema))     
        else:
            if(self.tokenAtual().tipo == 'FIM'):
                self.erro = True
                raise Exception('Missing Token na linha '+str(self.tokenAtual().linha)+' '+str(self.tokenAtual().lexema))    
            self.erro = True
            raise Exception('Erro sintatico Token fora do statement na linha '+str(self.tokenAtual().linha)+' '+str(self.tokenAtual().lexema))
    
    def expression(self):
        if(self.tokenAtual().tipo == 'NUMBER'):#<numero> que pode occorrer só, na aritmetica ou na logica
            if (not (self.lookAhead().tipo == 'EQUAL' or self.lookAhead().tipo == 'DIFF' or self.lookAhead().tipo == 'LESS' or self.lookAhead().tipo == 'LESSEQUAL' or self.lookAhead().tipo == 'GREAT' or self.lookAhead().tipo == 'GREATEQUAL')):# Se nao tiver simbolo de expressao logica
                #checa simbolo de op aritmetica
                if(not (self.lookAhead().tipo == 'SUM' or self.lookAhead().tipo == 'SUB' or self.lookAhead().tipo == 'DIV' or self.lookAhead().tipo == 'MUL')):#Se nao tiver simbolo de expressao aritmetica
                    #Entra aqui se for apenas numero
                    val = self.tokenAtual().lexema
                    self.indexToken +=1
                    return val
                else:#Se tiver simbolo aritmetico
                    aritExpr = str(self.tokenAtual().lexema)
                    self.indexToken+=1 # Em cima do simbolo aritmetico
                    aritExpr+=str(self.tokenAtual().lexema)
                    if(self.lookAhead().tipo == 'NUMBER' or (self.lookAhead().tipo == 'ID' and (self.lookAhead().lexema[0] == 'v' or self.lookAhead().lexema[0] == 'f'))):
                        aritExpr+=str(self.lookAhead().lexema) ### funcionando para numero e numer apenas
                        self.indexToken +=2 #Token depois do numero
                        #Mais de um termo na expressao, entra nesse if
                        if(self.tokenAtual().tipo == 'SUM' or self.tokenAtual().tipo == 'SUB' or self.tokenAtual().tipo == 'DIV' or self.tokenAtual().tipo == 'MUL'):
                            aritExpr += self.tokenAtual().lexema
                            self.indexToken += 1
                            aritExpr += self.expression()
                        return aritExpr
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico numero op ?, (arithmetic expression) na linha '+str(self.tokenAtual().linha))
            else: #Se tiver simbolo de expressao logica, logica so permite 2 termos
                logicExpr = str(self.tokenAtual().lexema)
                self.indexToken +=1 # Em cima do simbolo logico (op-condicional)
                logicExpr+=str(self.tokenAtual().lexema)

                if(self.lookAhead().tipo == 'NUMBER'):
                    logicExpr += str(self.lookAhead().lexema)
                    self.indexToken+=2
                    return logicExpr
                elif(self.lookAhead().tipo == 'ID'):
                    if(self.lookAhead().lexema[0] == 'v'):
                        self.indexToken +=2
                        return
                    elif(self.lookAhead().lexema[0] == 'f'):
                        self.indexToken +=2 # vai pro token depois do ID da funcao, no caso o parentese
                        if(self.tokenAtual().tipo == 'LBRACK'):
                            self.indexToken+=1
                            while(self.tokenAtual().tipo != 'RBRACK'):
                                if(self.tokenAtual().tipo == 'NUMBER' or self.tokenAtual().tipo == 'BOOLEAN' or self.tokenAtual().lexema[0] == 'v'):#verifica se foi passado numero, boolean, ou variavel
                                    self.indexToken+=1
                                    if(self.tokenAtual().tipo == 'COMMA'):
                                        self.indexToken +=1
                                        if(self.tokenAtual().tipo == 'RBRACK'):
                                            self.erro = True
                                            raise Exception('Erro sintatico falta de argumentos na linha ' + str(self.tokenAtual().linha))
                                    elif(self.tokenAtual().tipo == 'RBRACK'):
                                        self.indexToken +=1
                                        break
                                    else:
                                        self.erro = True
                                        raise Exception('Erro sintatico Virgula na linha ' + str(self.tokenAtual().linha))
                                else:
                                    self.erro = True
                                    raise Exception('Erro sintatico argumento invalido na linha ' + str(self.tokenAtual().linha))
                        else:
                            self.erro = True
                            raise Exception('Erro sintatico chamada de func parentese esquerdo na linha '+str(self.tokenAtual().linha))
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico operacao sem funcao ou variavel '+str(self.tokenAtual().linha))
                else:
                    self.erro = True
                    raise Exception('Erro sintatico numero op ?, (logical expression) na linha '+str(self.tokenAtual().linha))
        
        elif(self.tokenAtual().tipo == 'BOOLEAN'):# Se a expressão for só um boolean
            val = self.tokenAtual().lexema
            self.indexToken +=1
            return val

        elif(self.tokenAtual().tipo == 'ID'):# Identificador de Função e Variável
            if(self.tokenAtual().lexema[0] == 'v' or self.tokenAtual().lexema[0] == 'f'):# checa se o identificador começa com f ou v
                if(self.tokenAtual().lexema[0] == 'f'):# se for uma funcao
                    self.indexToken+=1
                    if(self.tokenAtual().tipo == 'LBRACK'):
                        self.indexToken +=1
                        while(self.tokenAtual().tipo != 'RBRACK'):# verifica argumentos da funcao para ser chamada, nao checa tipos (semantica)
                            if(self.tokenAtual().tipo == 'NUMBER' or self.tokenAtual().tipo == 'BOOLEAN' or self.tokenAtual().lexema[0] == 'v'):#verifica se foi passado numero, boolean, ou variavel
                                self.indexToken += 1
                                if(self.tokenAtual().tipo == 'COMMA'):
                                    self.indexToken +=1
                                    if(self.tokenAtual().tipo == 'RBRACK'):#nao ta incrementando  index igual as outras funcoes, mas ta funcionando
                                        self.erro = True
                                        raise Exception('Erro sintatico falta de argumentos na linha ' + str(self.tokenAtual().linha))
                                elif(self.tokenAtual().tipo == 'RBRACK'):
                                    break
                                else:
                                    self.erro = True
                                    raise Exception('Erro sintatico Virgula na linha ' + str(self.tokenAtual().linha))
                            else:
                                self.erro = True
                                raise Exception('Erro sintatico argumento invalido na linha ' + str(self.tokenAtual().linha))
                        #fora do laço encontrou o RBRACK
                        self.indexToken+=1
                    else:
                        self.erro = True
                        raise Exception('Erro sintatico Parentese esquerdo da Funcao declaracao na linha ' + str(self.tokenAtual().linha))
                else:#é uma variavel
                    self.indexToken +=1
                    return
            else:
                self.erro = True
                raise Exception('Erro sintatico, id nao comeca com f ou v '+str(self.tokenAtual().linha))
        else:
            self.erro = True
            raise Exception('Erro sintatico expression '+str(self.tokenAtual().linha))

    def condicao(self):
        self.expression()
        self.condicao_aux()
        return
    def condicao_aux(self):
        if(self.tokenAtual().tipo == 'EQUAL' or self.tokenAtual().tipo == 'DIFF' or self.tokenAtual().tipo == 'LESS' or self.tokenAtual().tipo == 'LESSEQUAL' or self.tokenAtual().tipo == 'GREAT' or self.tokenAtual().tipo == 'GREATEQUAL'):
            self.indexToken +=1
            self.condicao()
            return
        else:
            return
    def lookAhead(self):
        return self.tabTokens[self.indexToken + 1]
    def checkSemantica(self,tipo,index):#checa semantica, se tiver tudo OK return True
        if(tipo == 'VARDEC'): # checa semantica de declaração de Variável
            simbAtual = self.tabSimbolos[index]
            if(simbAtual[1] == 'INT'):
                if(simbAtual[3].isnumeric() or bool(re.match("[0-9A-Za-a]*( ){0,}([+-/*]( ){0,}[0-9A-Za-a]*( ){0,})*",simbAtual[3]))):
                    self.indexDecVarAtual +=1
                    return True
                else:
                    #linha do ponto e virgula que é a mesma
                    raise Exception("Erro Semântico, variavel do tipo inteiro nao recebe inteiro na linha: "+str(self.tokenAtual().linha))
            if(simbAtual[1] == 'TBOOLEAN'):
                if(simbAtual[3] == 'true' or simbAtual[3] == 'false'):
                    self.indexDecVarAtual +=1
                    return True
                else:
                    #linha do ponto e virgula que é a mesma
                    raise Exception("Erro Semântico, variavel do tipo boolean nao recebe boolean na linha: "+str(self.tokenAtual().linha))
        
        #elif(outros tipos)