from Token import Token
class Scanner:
    def __init__(self, programa):
        self.tokens = []
        self.programa = programa
        self.inicio = 0
        self.atual = 0
        self.linha = 1
    
    def nextChar(self):
        self.atual +=1 #atualiza antes de retornar
        return self.programa[self.atual - 1] #Passa pro proximo char
        #atual é o char a frente do que tá sendo lido

    def scan(self): #
        self.scanTokens()
        self.tokens.append(Token("FIM",'',self.linha)) #Escrever fim de arquivo nos tokens
        self.scanReserved() # Verifica a tabela de tokens para atualizar o Tipo dos tokens das palavras reservadas
        return self.tokens
    def scanTokens(self):# procura os tokens
        while(self.atual < len(self.programa)): #enquanto n chegar no final
            self.inicio = self.atual
            char = self.nextChar()
            if char == ' ' or char == '\t' or char == '\r':
                pass
            elif char == '\n':
                self.linha += 1
            elif char == '(':# Parentese esquerdo
                self.tokens.append(Token("LBRACK",self.programa[self.inicio:self.atual],self.linha))
           
            elif char == ')':# Parentese direito
                self.tokens.append(Token("RBRACK",self.programa[self.inicio:self.atual],self.linha))
           
            elif char == '{': # Chaves (Curly Brackets) esquerdo
                self.tokens.append(Token("LCBRACK",self.programa[self.inicio:self.atual],self.linha))

            elif char == '}': # Direito
                self.tokens.append(Token("RCBRACK",self.programa[self.inicio:self.atual],self.linha))
           
            elif char == '+': # Soma
                self.tokens.append(Token("SUM",self.programa[self.inicio:self.atual],self.linha))
           
            elif char == '-': # Subtracao
                self.tokens.append(Token("SUB",self.programa[self.inicio:self.atual],self.linha))
           
            elif char == '*': # Multiplicacao
                self.tokens.append(Token("MUL",self.programa[self.inicio:self.atual],self.linha))
            
            elif char == '/': # Divisao
                self.tokens.append(Token("DIV",self.programa[self.inicio:self.atual],self.linha))
            
            elif char == '=': # Igual ou Atribuicao
                if self.lookAhead() == '=':
                    self.atual +=1
                    self.tokens.append(Token("EQUAL",self.programa[self.inicio:self.atual],self.linha))
                else:
                    self.tokens.append(Token("ATTR",self.programa[self.inicio:self.atual],self.linha))
            elif char == '<': # Diferente, menor ou igual, menor
                if self.lookAhead() == '>':
                    self.atual +=1
                    self.tokens.append(Token("DIFF",self.programa[self.inicio:self.atual],self.linha))
                elif self.lookAhead() == '=':
                    self.atual+=1
                    self.tokens.append(Token("LESSEQUAL",self.programa[self.inicio:self.atual],self.linha))
                else:
                    self.tokens.append(Token("LESS",self.programa[self.inicio:self.atual],self.linha))           
            elif char == '>':# Maior ou igual, Maior
                if self.lookAhead() == '=':
                    self.atual +=1
                    self.tokens.append(Token("GREATEQUAL",self.programa[self.inicio:self.atual],self.linha))
                else:
                    self.tokens.append(Token("GREAT",self.programa[self.inicio:self.atual],self.linha))
            elif char == ',':# Virgula
                self.tokens.append(Token("COMMA",self.programa[self.inicio:self.atual],self.linha))
            
            elif char == ';':# Ponto e virgula
                self.tokens.append(Token("SEMICOLON",self.programa[self.inicio:self.atual],self.linha))
            
            elif char >= '0' and char <= '9': # Numeros
                while(self.lookAhead() >= '0' and self.lookAhead() <='9'):
                    self.nextChar()
                self.tokens.append(Token("NUMBER",self.programa[self.inicio:self.atual],self.linha))
            elif char.isalpha(): #Letras/Identificadores/Reservadas
                while(self.lookAhead().isalnum()):
                    self.nextChar()
                self.tokens.append(Token("ID",self.programa[self.inicio:self.atual],self.linha))
            else:
                print('Caractere Inválido na linha:',self.linha)
                exit(2)
    
    def scanReserved(self):
        for i in self.tokens:
            if(i.tipo == 'ID'):
                if(i.lexema == 'func'):
                
                elif(i.lexema == 'proc'):
                    i.tipo = "PROC"
                
                elif(i.lexema == 'int'):
                    i.tipo = 'INT'
                
                elif(i.lexema == 'boolean'):
                    i.tipo = 'TBOOLEAN' #Tipo Booleano
                
                elif(i.lexema == 'true'):
                    i.tipo = 'BOOLEAN' #Booleano
                
                elif(i.lexema == 'false'):
                    i.tipo = 'BOOLEAN'
                
                elif(i.lexema == 'return'):
                    i.tipo = 'RETURN'
                
                elif(i.lexema == 'if'):
                    i.tipo = 'IF'
                
                elif(i.lexema == 'while'):
                    i.tipo = 'WHILE'
                
                elif(i.lexema == 'puts'):
                    i.tipo = 'PUTS'
                
                elif(i.lexema == 'break'):
                    i.tipo = 'BREAK'
                
                elif(i.lexema == 'continue'):
                    i.tipo = 'CONTINUE'
                
                elif(i.lexema == 'else'):
                    i.tipo = 'ELSE'

    def lookAhead(self):
        if(self.atual < len(self.programa)):# verifica se nao esta no final do programa
            return self.programa[self.atual] # Pega o lookahead
        else:
            return '\0'