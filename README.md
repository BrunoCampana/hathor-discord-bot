# hathor-discord-bot
Um demo app que integra-se com a Hathor Network. Um bot no Discord que conecta-se com a Hathor Network.

Neste exemplo, criamos um bot no Discord. O bot é então adicionado a um server. Uma vez o código executando, o bot lê continuamente as mensagens no server. Sempre que algum usuário remeter uma mensagem iniciando com “I need HTR” e contendo um endereço válido na Hathor Network no formato HTR[<endereço_válido>] , o bot irá tentar efetuar uma transferência no valor de 0.01 HTR para o usuário. Caso o endereço seja válido e o bot tenha fundos na wallet, ele conseguirá efetuar a transação. Caso contrário, ele irá informar que não conseguiu explicando o motivo. 

O sistema descrito envolve três componentes: (i) Discord API; (ii) Hathor headless wallet; e (iii) o código-fonte do bot propriamente dito, o módulo hathor_discord_bot.py . O diagrama abaixo ilustra a arquitetura do sistema descrito:

```
Discord API <--> hathor discord bot <--> Hathor headless wallet <--> Public Hathor full node <--> Hathor Network
```

Observe que o código no módulo `hathor_discord_bot.py` integra-se com a plataforma Discord pela API pública do mesmo, e com a aplicação de carteira Hathor headless wallet. É nessa aplicação de carteira que encontra-se a wallet que o bot usará para enviar HTR para os usuários. 
A Hathor headless wallet por sua vez, conecta-se a um full node público da Hathor Network, testnet ou mainnet.

## Passo a passo para executar o demo app

1. Use sua conta no Discord para criar um server novo (comum) na plataforma, para você executar o teste.
2. Use sua conta para entrar no Discord developer portal e cria um “app”.
3. Acesse o menu do seu recém-criado “app”: Settings > OAuth2 > URL Generator.
  a. Em scopes, selecione “bot”.
  b. Em “bot permissions”, selecione pelo menos as seguintes: 
    i. “Read Messages/View Channels”;
    ii. “Send Messages”.
  c. Copie a URL gerada e use-a em seu browser para adicionar o bot no server que você criou no passo 1.
4. Ainda no menu de seu app: Settings > Bot.
  a. Habilite a opção “Message content intent”.
5. No módulo hathor_discord_bot.py, substitua em todo o módulo, os placeholders a seguir pelos valores que estiver usando, referentes a sua instância da aplicação Hathor headless wallet:
  - `<your_test_wallet_id>`.
  - `<your_test_wallet_seed_key>`.
  - `<discord_bot_token>`.
6. Você obtém seu `<discord_bot_token>` no Discord developer portal, selecionando seu app e navegando no menu do mesmo, em: Settings > Bot.
7. Você precisar executar uma instância da aplicação Hathor headless wallet. Para saber como fazer isso, veja [Hathor headless wallet pathway.](https://hathor.gitbook.io/hathor/guides/headless-wallet).
8. O valor da variável `wallet_base_url` já encontra-se definido para conectar-se a uma instância da aplicação de carteira Hathor headless wallet em http://localhost:8000. Caso sua aplicação de Hathor headless wallet esteja disponível em outro local, altere essa variável.
9. O valor da variável `full_node_base_url` já encontra-se definido para conectar-se ao Hathor full node público em https://node2.mainnet.hathor.network. Você pode alterar esse full node se quiser. O bot faz uma conexão direta com o full node, pela API web do mesmo. Isso serve para o bot consultar se o address provido é válido, evitando remeter à aplicação de carteira (Hathor headless wallet) uma transação para um address inválido. Note que para fins de simplicidade essa conexão não está representada no diagrama de arquitetura de componentes do sistema apresentado.
10. Vá até seu servidor do Discord e confirme que o bot encontra-se adicionado ao mesmo, e offline.
11. Execute o módulo `hathor_discord_bot.py`.
12. Com o bot executando, verifique se o status do mesmo altera-se para online em seu servidor de testes.
13. Use seu usuário para pedir ao bot que envie HTR para você postando no canal “general” do server a seguinte frase: “I need HTR: HTR[<address_de_recebimento_aqui>]”. Substitua o placeholder `<address_de_recebimento_aqui>` por um endereço válido da Hathor Network onde você quer receber o HTR do bot.
14. Se o endereço provido for válido e a wallet gerenciada pelo bot tiver fundos, o bot enviará ao endereço provido 0.01 HTR. Você poderá checar na wallet dona do endereço recipiente se o valor realmente foi depositado.
15. O bot enviará uma mensagem no canal “general” do server informando que enviou o valor para sua wallet. Caso o endereço provido seja inválido, o bot irá lhe informar no canal e pedirá para você prover um endereço válido. Caso o bot não tenha fundos, ou ele não conseguir estabelecer a conexão com a Hathor headless wallet, ou qualquer outro problema tenha ocorrido que tenha impedido o bot de efetuar a transferência, ele irá informar que não conseguiu remeter a transferência.
16. Pronto! Você agora tem um bot no Discord que se integra com a Hathor Network!

Por questão de segurança pessoal, recomendamos você a usar uma wallet (seed phrase) específica e exclusiva para TESTES. NÃO use esta wallet para receber, enviar e armazenar valores reais.
