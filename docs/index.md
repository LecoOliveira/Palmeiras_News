<img class="logo" src="./assets/palmeiras_news.png" width="50%">
<p align="center">
    <em>Receba informações do próximo jogo em seu celular</em>
</p>
<div align="center">
<a href="https://github.com/LecoOliveira/Palmeiras_News/blob/main/LICENSE" target="_blank">
<img alt="GitHub" src="https://img.shields.io/github/license/LecoOliveira/Palmeiras_news?label=License&logo=gnu&style=plastic&color=dark-green">
</a>
<a href="https://codecov.io/github/LecoOliveira/Palmeiras_News" target="_blank">
<img alt="Codecov" src="https://img.shields.io/codecov/c/github/LecoOliveira/Palmeiras_news?label=Coverage&style=plastic&logo=codecov&color=dark-green">
</a>
<a href="https://github.com/LecoOliveira/Palmeiras_News/actions" target="_blank">
<img alt="GitHub Workflow Status (with event)" src="https://img.shields.io/github/actions/workflow/status/LecoOliveira/Palmeiras_news/pipeline.yml?style=plastic&logo=github&label=CI/CD&color=dark-green">
</a>
</div>

---
**Código fonte:** <a href="https://github.com/LecoOliveira/Palmeiras_News" target="_blank">https://github.com/LecoOliveira/Palmeiras_News</a>

---
Palmeiras news é um projeto para estudo e aprendizado de Python e suas bibliotecas.

É um script simples que realiza uma raspagem (webscraping) no site do Palmeiras, e envia as informações do próximo jogo por SMS utilizando o <a href="https://www.twilio.com/pt-br" target="_blank">Twilio</a>. Todo o processo é automatizado, ele verifica se o dia atual tem jogo, e se tiver, espera o momento que sai a escalação e envia todos os dados para você.

---
## Instalação

Para fazer a instalação usaremos o pip:

<div class="termy">

```bash
$ pip install palmeiras-news

---> 100%
palmeiras-news instalado com sucesso
```

</div>

---
## Como usar

Esse projeto é um script simples, e faz tudo sozinho depois que é inicializado. As únicas coisas que você vai precisar fazer
é configurar suas variáveis de ambiente onde serão armazenadas as credenciais da sua conta Twilio.

Caso queira pode usar o `--help` para receber uma ajuda rápida:

<div class="termy">

```bash
$ palmeiras --help

 Usage: palmeiras [OPTIONS] COMMAND [ARGS]...                             
                                                                          
 Interface para configuração de variáveis de ambiente que serão usadas no 
 Palmeiras_news.                                                          
                                                                          
╭─ Options ──────────────────────────────────────────────────────────────╮
│ --help                                           Show this message and │
│                                                  exit.                 │
╰────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────╮
│ delete         Comando que deleta uma variável de ambiente do arquivo. │
│ destiny-phone  Configura os números para onde serão enviadas as        |
|                mensagens.                                              │
│ listar         Lista todas as variáveis de ambiente cadastradas.       │
│ sid            Configura o TWILIO_ACCOUNT_SID na variável de ambiente. │
│ token          Configura o TWILI_AUTH_TOKEN na variável de ambiente.   │
│ twilio-phone   Configura o TWILIO_PHONE_NUMBER na variável de          │
│                ambiente.                                               │
╰────────────────────────────────────────────────────────────────────────╯
```
</div>
<center><sup>*Logo de cara, podemos observar todos os comandos de configuração listados na sessão `Commands`*</sup></center>

---

### Obtendo credenciais

Nesse projeto usamos o [Twilio](https://www.twilio.com/pt-br) para fazer o envio das mensagens.
Basta se cadastrar no site oficial, e você terá acesso aos tokens e números necessários para a autenticação, podendo assim enviar as mensagens.

><sub> Obs.: O Twilio é um serviço **pago**, mas disponibilizam um período de testes gratuito. Caso queira continuar após o período, confira a tabala de preços.</sub> 

![Imagem Twilio](assets/imagem_twilio.png)

---
### Configurando variáveis

Com as credenciais em mãos, é hora de inseri-las no código.


É importante manter as credenciais da conta Twilio seguras, armazenando-as de maneira a impedir o acesso não autorizado. Um método comum é armazená-las em variáveis de ambiente que são acessadas no seu aplicativo. Isso os mantém fora do código e de outros lugares onde onde poderiam ser acessadas sem autorização.

Para adicionar as variáveis automaticamente no nosso arquivo, temos os seguintes comandos no CLI do nosso programa que precisarão ser configurados antes de rodar o programa pela primeira vez: ```sid```,  ```token```, ```twilio-phone``` e ```destiny-phone```.

///warning | Importante
Você só pode adicionar um SID, um TOKEN e um TWILIO_PHONE, então cuidado ao adicioná - los. Caso erre ao configurá-los, 
você pode usar a opção `delete` para deletar e configurar novamente.
///

Para configurar a sua credencial (seja ela o `sid`, `token` ou `twilio-phone`) digite no seu terminal o comando `palmeiras` seguindo da credencial que deseja adicionar, como no exemplo a seguir:

<div class="termy">

```bash
$ palmeiras sid SEU_ACCOUNT_SID

---> 100%
[15:44:12] TWILIO_ACCOUNT_SID configurado com sucesso!

```
</div>
<center><sup>*Faça isso para todas as credenciais*</center></sup>

---

Já no caso do `destiny-phone`, é possível adicionar um ou mais números por vez. Para ele digite os números que deseja adicionar separados por espaços:

<div class="termy">

```bash
$ palmeiras destiny-phone SEU_DESTINY_PHONE1 SEU_DESTINY_PHONE2

---> 100%
[20:59:45] TWILIO_DESTINY_PHONE_NUMBER SEU_DESTINY_PHONE1 SEU_DESTINY_PHONE2 configurado(s) com sucesso.
```
</div>

/// tip | Atenção
Importante lembrar, que todos os `destiny_phone` devem ser cadastrados e devidamente ativados no seu painel da Twilio. Sem isso, eles não receberão as mensagens.
/// 

E sim, para cada número cadastrado, será cobrado pela mensagem enviada. A ideia inicial é para que seja um projeto simples, pessoal. E para isso os créditos dados como teste pela Twilio já ajudarão. Mas caso goste e queira continuar usando, pode comprar mais créditos, fica bem barato cada mensagem (consulte a [tabela de preços](https://www.twilio.com/pt-br/sms/pricing/br)).

---
### Listando variáveis

Depois de configuradas suas variáveis de ambiente, você pode visualizá-las para confirmar se foram configuradas de forma correta.
Para isso, use o comando `listar`. Se não passar nenhuma flag será retornado todas as variáveis cadastradas:

<div class="termy">

```bash
$ palmeiras listar

[21:37:23] TWILIO_AUTH_TOKEN="e5xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
           TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"              
           TWILIO_DESTINY_PHONE_NUMBER="+55xxxxxxxxxxx"                         
           TWILIO_PHONE_NUMBER="+127xxxxxxxx"
```
</div>

Para listar uma variável específica digite a flag da mesma:
<div class="termy">

```bash
$ palmeiras listar --sid

[11:41:16] TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
</div>
<center><sup>*Se houver dúvidas use o `palmeiras listar --help`*</center></sup>

---

### Deletando variáveis

Caso queira deletar ou reconfigurar alguma variável, você pode usar o comando `delete` seguido pela flag da variável que deseja alterar. 
Como no exemplo `--twilio-phone`:

<div class="termy">

```bash
$ palmeiras delete --twilio-phone

---> 100%
[22:00:38] TWILIO_PHONE_NUMBER removido com sucesso.
```
</div>

///warning | Cuidado
O programa precisará de todas as variáveis para funcionar, então não esqueça de cadastrar outra após deletar a anterior.
///

---

## Rodando o programa

Depois de cadastrada todas as credenciais, é só rodar o comando no terminal:

``` { .bash .copy }
palmeiras-run &
```
Nosso app ficará rodando em segundo plano, esperando para serem executadas as tasks.