
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/ErikJhonatta/Compiladores">
    <img src="https://static.thenounproject.com/png/1706925-200.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Compiladores</h3>

  <p align="center">
    Repositório para a disciplina de Compiladores do PLE 2020.3
    <br />



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Sobre o Projeto](#sobre-o-projeto)
  * [Feito Com](#feito-com)
* [Começando](#começando)
  * [Pré-requisitos](#pré-requisitos)
  * [Gramática](#gramática)
  * [Instalação](#instalação)
* [Uso](#uso)
* [Licença](#licença)
* [Contato](#contato)
* [Contribuidores](#contribuidores)



<!-- ABOUT THE PROJECT -->
## Sobre o Projeto

O projeto foi um avaliação da disciplina de Compiladores do período PLE 2020.3 da UFAPE, onde criaríamos uma linguagem livre de contexto LL(1),
que não possua recursão a esquerda, que seja fatorada a esquerda, tenha um símbolo de look ahead e tenha os seguintes aspectos:


1. Declaração de variáveis de tipo inteiro e booleano
2. Declaração de procedimentos e funções (sem e com parâmetros)
3. Comandos de atribuição
4. Chamada de procedimentos e funções
5. Comando de desvio condicional (if e else)
6. Comando de laço (while)
7. Comando de retorno de valor
8. Comandos de desvio incondicional (break e continue)
9. Comando de impressão de constante e variável na tela
10. Expressões aritméticas (+, -, * e /)
11. Expressões booleanas (==, !=, >, >=, < e <=)

### Feito Com
* [Python](https://www.python.org/)

<!-- GETTING STARTED -->
## Começando

Como usar o compilador

### Pré-requisitos
* Python3

```sh
sudo apt-get update
sudo apt-get install python3.8
```
ou

[Python Downloads](https://www.python.org/downloads/)
### Gramática
`Gramática.bnf`

Além das características mostradas em [Sobre o Projeto](#sobre-o-projeto), a linguagem possui algumas outras:

1. Nome de Variável deve começar com 'v'
`int vCount;`
2. Nome de Função deve começar com 'f'
`func fSoma(int vA, int vB){...}`
3. Nome de Procedimento deve começar com 'p'
`proc pSub(int vA, int vB)`
4. Declaração de Funções e Procedimentos possuem palavra reservada
* Procedimentos ('proc')

`proc pFoo(...){...}`
* Funções ('func')

`func fBar(...){...}`


### Instalação

1. Clone o repositório
```sh
git clone https://github.com/ErikJhonatta/Compiladores.git
```

<!-- USAGE EXAMPLES -->
## Uso
Crie um Arquivo de código fonte, seguindo a gramática da linguagem
* [Gramática](#gramática)
Execute o `Main.py` de um terminal, logo em seguida de um arquivo de código fonte
```sh
python3 Main.py test.eb
```


<!-- LICENSE -->
## Licença

Distribuído sob a Licença MIT. Veja `LICENSE` para mais informações.



<!-- CONTACT -->
## Contato

Erik Jhonatta - [@erikjhonatta](https://instagram.com/ErikJhonatta) - erikjhonatta@gmail.com

Bruno Diniz   - [@brunodinizbd](https://www.instagram.com/brunodinizbd/) - brunosoares.ibi@gmail.com

Link do Projeto: [https://github.com/ErikJhonatta/Compiladores](https://github.com/ErikJhonatta/Compiladores)



## Contribuidores

<table>
  <tr>
    <td align="center"><a href="https://github.com/ErikJhonatta"><img src="https://github.com/ErikJhonatta.png" width="100px;" alt=""/><br /><sub><b>Erik Jhonatta</b></sub></a><br /><a href="https://github.com/ErikJhonatta/Compiladores/commits?author=ErikJhonatta" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/BASDiniz"><img src="https://github.com/BASDiniz.png" width="100px;" alt=""/><br /><sub><b>Bruno Diniz</b></sub></a><br /><a href="https://github.com/ErikJhonatta/Compiladores/commits?author=BASDiniz" title="Code">💻</a></td>
  </tr>
</table>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ErikJhonatta/Compiladores.svg?style=flat-square
[contributors-url]: https://github.com/ErikJhonatta/Compiladores/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ErikJhonatta/Compiladores.svg?style=flat-square
[forks-url]: https://github.com/ErikJhonatta/Compiladores/network/members
[stars-shield]: https://img.shields.io/github/stars/ErikJhonatta/Compiladores.svg?style=flat-square
[stars-url]: https://github.com/ErikJhonatta/Compiladores/stargazers
[issues-shield]: https://img.shields.io/github/issues/ErikJhonatta/Compiladores.svg?style=flat-square
[issues-url]: https://github.com/ErikJhonatta/Compiladores/issues
[license-shield]: https://img.shields.io/github/license/ErikJhonatta/Compiladores.svg?style=flat-square
[license-url]: https://github.com/ErikJhonatta/Compiladores/blob/master/LICENSE
