<img class="logo" src="./assets/palmeiras_news.png" width="50%">
<p align="center">
    <em>Receba informações do próximo jogo em seu celular</em>
</p>

---
**Código fonte:** <a href="https://github.com/LecoOliveira/Palmeiras_News" target="_blank">https://github.com/LecoOliveira/Palmeiras_News</a>

---
Palmeiras news é um projeto para estudo e aprendizado de Python e suas bibliotecas. Esse script realiza uma raspagem (webscraping) no site do Palmeiras, e envia as informações do próximo jogo por SMS utilizando o <a href="https://www.twilio.com/pt-br" target="_blank">Twilio</a>.

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

Mas antes disso, vamos consultar o `--help` para receber uma simples ajuda:

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

Logo de cara, podemos observar todos os comandos de configuração listados na sessão `Commands`.
    
- **delete:** É auto explicativo, ele deleta uma configuração já feita, e que você queira excluir por algum motivo.
- **destiny-phone:** Adiciona números para onde serão enviadas as mensagens. Podendo ser um ou mais números separados por espaço.