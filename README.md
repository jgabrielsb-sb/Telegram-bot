# Telegram-bot
- Esta é uma aplicação desenvolvida com o objetivo de gerir as assinaturas de um serviço Online.

  # 1. Como rodar a aplicação
  Primeiramente, é necessário obter criar o seu BOT no telegram e obter um **TOKEN**. Para obtê-lo, siga o tutorial: https://canaltech.com.br/apps/como-criar-um-bot-no-telegram-botfather/
  De posse do **TOKEN**, insira-o no campo **TOKEN** do arquivo **config_bot.py**.
  Por fim, rode a aplicação **main.py**.

  # 2. Alguns detalhes de implementação
  A classe **'Member'**, que implementa um membro único do grupo, possui cinco atributos: nome, número de celular, data de entrada, data de saída e plataforma de pagamento.
  Já a classe **'Register'**, que implementa uma coleção de membros, possui apenas um atributo: um dicionário em que cada key é dada pelo nome do membro e o value é dado por um elemennto da classe Member.
  Ambas as classes estão especificadas no arquivo members.py

  A classe 'Register', por sua vez, possui os métodos com as seguintes funções: adicionar membros, remover membros, mostrar membros, obter registro e setar registro. O penúltimo método é responsável por retornar os membros presentes no arquivo 'register.txt', enquanto o último é responsável por escrever neste mesmo arquivo os membros adicionados e atualizar aqueles que foram removidos, além de atualizar a data final ao qual o membro poderá permanecer no grupo.
  O arquivo 'register.txt' é organizado da seguinte forma:
  - Cada linha é a especificação de um membro único: ['nome_membro', 'numero_celular', 'data_entrada', 'data_saida', 'plataforma_pagamento']
  - A data de entrada e saida deve ser dada no formato "DIA/MÊS/ANO"
  Por exemplo: suponha que, inicialmente, temos 2 membros no grupo. O primeiro deles é jgabriel, de número de celular 11223344, data de entrada 01/03/2024, data de saida 01/04/2024 e seu pagemento foi feito no picpay. O segundo é jorge, de numero 55667788, data de entrada 20/02/2024, data de saida 20/03/2024 e seu pagamento foi realizado no mercadopago. Sendo assim, o arquivo deveria estar organizado da seguinte forma:

      ['jgabriel', '11223344', '01/02/2024', '01/03/2024', 'picpay']

      ['jorge', '55667788', '20/02/2024', '20/03/2024', 'mercadopago']

  # 3. Comandos do BOT
  Ao rodar a aplicação, podemos passar os seguintes comandos:
    1. **/start**: deve ser dado logo no início do funcionamento para que os membros presentes no arquivo 'register.txt' sejam armazenados.
    2. **/add_member**: utilizado para adicionar um novo membro. Neste caso, será pedido o nome, número de celular, data de entrada, data de saída e plataforma de pagamento. Caso a data seja inválida, o membro não será adicionado e um aviso será dado. Caso contrário, o membro será adicionado e o arquivo 'register.txt' atualizado.
    3. **/remove_member**: utilizado para remover um membro. Neste caso, será pedido o nome. Caso esteja no grupo, será removido e o arquivo 'register.txt' atualizado. Caso contrário, um aviso será dado e nada acontecerá.
    4. **/update_member**: utilizado para atualizar a data de saída de um membro (no caso de pagamento da assinatura). Neste caso, será pedido o nome. Caso esteja no grupo, será adicionado um mês a data de saída. Caso contrário, um aviso será dado e nada acontecerá. Da mesma forma, qualquer alteração será atualizada no arquivo 'register.txt'
    5. **/show_members**: simplesmente mostra todos os membros do grupo.
    6. **/show_status**: mostra os membros em situação irregular, ou seja, que estão no grupo sem o devido pagamento da mensalidade, e também mostra os que estão perto de acabar a memsalidade (os que faltam 5 dias ou menos para o término do período permitido).
 
  
  
  
 
  
  

