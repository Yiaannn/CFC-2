# CFC-2
Projeto 2 da matéria Camada Física da Computação

--------
## Introdução
--------
## Entrega 1

Preparamos a geração de tons DTMF gerando duas ondas senoidais de diferentes frequências. As frequências devem seguir valores específicos para seguir o padrão DTMF, de acordo com a seguinte tabela

![Guia DTMF](https://ptolemy.eecs.berkeley.edu/eecs20/week2/keypad.gif)

As duas ondas de frequências diferentes são somadas uma â outra, de forma que a onda resultante equivale ao tom DTMF desejado. Uma vez que geramos a frequência desejada ela é salva para o uso do nosso programa

Nosso programa foi feito com uma interface gráfica em pygame com o propósito de visualizar em tempo real o processamento das ondas. Uma vez que o tom a ser tocado é selecionado a interface exibe a onda equivalente:

![Onda do tom 2 selecionada](https://raw.githubusercontent.com/Yiaannn/CFC-2/master/readmeresources/tom2.png)
![Onda do tom 8 selecionada](https://raw.githubusercontent.com/Yiaannn/CFC-2/master/readmeresources/tom8.png)

A onda então pode ser tocada apertando o botão "Play".
Junto da possibilidade de gerar e tocar áudios, podemos também gravar áudio em tempo real. A gravação é feita exibindo a frequência recebida em 30 fps até ser interrompida (ou o limite de 10 segundos ser atingido) 

![Gravação em tempo real](https://raw.githubusercontent.com/Yiaannn/CFC-2/master/readmeresources/gravando.png)

Quando gravado podemos salvar a gravação de volta para o programa,
