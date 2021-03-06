# CFC-2
Projeto 2 da matéria Camada Física da Computação

--------
## Introdução
--------
## Entrega 1

A geração de tons DTMF é feita a partir da some de duas ondas senoidais de diferentes frequências, as quais devem seguir valores específicos de acordo com o padrão DTMF. Segue a tabela com os valores:

![Guia DTMF](https://ptolemy.eecs.berkeley.edu/eecs20/week2/keypad.gif)

Quando as duas ondas de frequências diferentes são somadas uma à outra uma onda resultante é gerada, correspondente a cada um dos tons DTMF. Uma vez que geramos a frequência desejada ela é salva para o uso do nosso programa.

Nosso programa foi feito com uma interface gráfica em pygame com o propósito de visualizar em tempo real a geração das ondas. Uma vez que o tom a ser tocado é selecionado a interface exibe a onda equivalente. Podemos observar as ondas respectivas às teclas 2 e 8:

![Onda do tom 2 selecionada](https://raw.githubusercontent.com/Yiaannn/CFC-2/master/readmeresources/tom2.png)
![Onda do tom 8 selecionada](https://raw.githubusercontent.com/Yiaannn/CFC-2/master/readmeresources/tom8.png)

A onda então pode ser tocada apertando o botão "Play".
Junto da possibilidade de gerar e tocar áudios, podemos também gravar áudio em tempo real. Observa-se a aba "Recording", na imagem abaixo:

![Gravação em tempo real](https://raw.githubusercontent.com/Yiaannn/CFC-2/master/readmeresources/gravando.png)



## Entrega 2


Para esta segunda entrega, o objetivo é incrementar a entrega passada implementando à recepção da onda, a transformada de Fourier aplicada no sinal recebido, assim podendo detectar qual sinal DTMF foi recebido.

Abaixo podemos observar a transformada de Fourier para a onde gerada, seguida pela transformada da onda recuperada:




Agora durante a gravação e reprodução o domínio em que o gráfico é plotado pode ser selecionado, podendo ser intensidade (y) por frequência (x) ou intensidade (y) por tempo (x). Assim que o sinal é recebido, já é aplicada a transformada, detectando assim os sinais senoidais que formam o sinal principal. Quando gravado podemos salvar a gravação, podendo ser reproduzida posteriormente na aba "Audio".

O restante do programa permanece com as funções iguais à entrega anterior.




## Entrega 3

### Introdução
A entrega 3 deste projeto consiste em incrementar ao projeto um protocolo de modulação de amplitude (AM) aos sinais sonoros. A modulação de amplitude consiste em alterar a amplitude de um sinal a fim de um receptor ser capaz de decodificar um sinal específico transmitido, com isso é possível compartilhar um mesmo meio para transmissão de diversos sinais com diversos tipos de informação.

### Modulação e demodulação
Em nosso programa, a modulação foi realizada multiplicando um sinal ponto a ponto pelo sinal da onda portadora, gerando assim o sinal modulado. A demodulação foi realizada utilizando a opreação contrária, dividindo-se o sinal modulado ponto a ponto pelo sinal portador, realizando as normalizações necessárias. As bandas utilizadas são selecionadas automaticamente através de um cálculo das frequências do sinal principal, de modo que na demodulação não seja criado nenhum conflito nas frequências. Adicionalmente o programa detecta automaticamente os sinais portadores na demodulação, não precisando escrevê-los manualmente.
