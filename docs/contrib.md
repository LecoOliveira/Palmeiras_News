# Como contribuir

Primeiramente, gostaria de agradecer por ter chegado até aqui. Esse é um projeto de estudo e tenho aprendido bastante com ele desde o início. 
Então, qualquer ajuda, por menor que ela seja, será de **GRANDE** valia! *Muito obrigado*! :star2::muscle:

## O projeto

Esse é um projeto bem simples, constituído basicamente de um agendador de tarefas feito com o <a href="https://rocketry.readthedocs.io/en/stable/" target="_blank">Rocketry</a>, que controla o fluxo de um web scraping feito usando o <a href="https://beautiful-soup-4.readthedocs.io/en/latest/" target="_blank">BeatifulSoup</a>. E para configurar as variáveis de ambiente do usuário, e dar uma carinha *bonitinha* pro nosso programa, construí um CLI com o <a href="https://typer.tiangolo.com/" target="_blank">Typer</a>.

### Estrutura

O projeto é estruturado basicamente em três pastas:

|   PASTA   |                       DESCRIÇÃO                                                    |
|-----------|------------------------------------------------------------------------------------|
| **app**   | Diretório base do nosso projeto, onde está todo o código principal e também o CLI. |
| **tests** | Onde armazenamos todos os nossos testes.                                           |
| **docs**  | Diretório para armazenar a documentação.                                           |

#### app
##### tasks
Nosso app é praticamente todo baseado nas tasks do Rocketry que estão dentro de `app/tasks`.

###### texto_msg()

A função principal é a <a href="/API/tasks/#tasks.texto.texto_msg" target="_blank">`texto_msg()`</a> no arquivo `texto.py`. Ela é uma task do Rocketry que roda todo dia verificando se a condição <a href="/API/conditions/#conditions.data_igual" target="_blank">`data_igual()`</a> retorna `True`. Se sim, ela faz um web scraping no site oficial, extrai o texto e retorna em uma lista, separando titulo do conteúdo.

```py title="texto_msg()"
[
  'Jogo: ',
  'Palmeiras x Flamengo l Campeonato Brasileiro (14ª rodada)',
  'Data e hora: ',
  '08/07/2023 l 21h',
  'Local: ',
  'Allianz Parque, em São Paulo (SP)'
]
```

###### formata_texto()

A task seguinte é a <a href="/API/tasks/#tasks.formata.formata_texto" target="_blank">`formata_texto()`</a> no arquivo `formata.py`.

Como o nome sugere, ela formata o texto recebido pela `texto_msg()` e o deixa pronto para envio. Para isso, usamos uma função do Rocketry chamada `after_success()`, que fica monitorando a task anterior, e quando bem sucedida, pega a lista retornada com o texto a ser formatado.

```py
@group.task(after_success(texto_msg))
def formata_texto(texto: list = Return(texto_msg)) -> str:

```
O `formata_texto()` por sua vez, retorna uma string já devidamente formatada.

```py title="formata_texto()"
'Jogo: Palmeiras x Flamengo | Campeonato Brasileiro (14ª rodada)'

'Data e hora: 08/07/2023 | 21h'

'Local: Allianz Parque, em São Paulo (SP)'

```
###### enviar_msg()

A última task é a que envia o texto já formatado para o(s) destinatário(s).

A <a href="/API/tasks/#tasks.envia.enviar_msg" target="_blank">`enviar_msg()`</a> usa as variáveis de ambiente cadastradas para enviar a mensagens.

```python
for destiny_phone in phones:
  message = CLIENT.messages.create(
      body=texto, from_=PHONE_NUMBER, to=destiny_phone
  )
```

---
###### Group

Como cada task foi feita em um arquivo diferente, todas essas tasks são tratadas como um Grouper Rocketry, que são "invocadas" no arquivo <a href="https://github.com/LecoOliveira/Palmeiras_News/blob/main/app/main.py" target="_blank">`main.py`</a> como vemos a seguir:

```python title="No arquivo da task"
group = Grouper()
```

```python title="No arquivo main"
app = Rocketry()

app.include_grouper(texto.group)
app.include_grouper(envia.group)
app.include_grouper(formata.group)
```

Então, se for criar uma task nova com o Rocketry, siga essa exemplo.

---
#### tests

Para os testes, optei por usar o <a href="https://docs.pytest.org/en/7.3.x/" target="_blank">pytest</a> por ter mais familiaridade. As configurações dele podem ser encontradas no arquivo <a href="https://github.com/LecoOliveira/Palmeiras_News/blob/main/pyproject.toml" target="_blank">pyproject.toml</a> na raiz do projeto. Você vai notar que temos bastante testes rodando, mas alguns são bem básicos, só para ver se a coisa toda ta legal e rodando bem. Caso queira implementar outros testes mais aprofundados, sinta-se a vontade.

/// tip | IMPORTANTE
Caso implemente algo na aplicação, **SEMPRE** teste! Os testes são fundamentais para o funcionamento do projeto.
///

---
#### docs

Para a documentação, estou utilizando o <a href="https://www.mkdocs.org/" target="_blank">mkdocs</a> com o tema <a href="https://squidfunk.github.io/mkdocs-material/" target="_blank">mkdocs-material</a> e você pode encontrar todas as configurações no arquivo <a href="https://github.com/LecoOliveira/Palmeiras_News/blob/main/mkdocs.yml" target="_blank">mkdocs.yml</a>. 

Também estou utilizando o <a href="https://mkdocstrings.github.io/" target="_blank">mkdocstrings</a> que está gerando a documentação da nossa API automaticamente usando as docstrings das nossas funções no python (seguindo o padrão <a href="https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html">docstrings do google</a>).

Então você verá que todos arquivos da pasta `/API` possuem o seguinte formato:

```md
::: tasks.texto
    options:
      show_root_toc_entry: false 
```

Então, se implementar uma nova função, documente seguindo os exemplos das funções que já existem no projeto, e depois crie um arquivo .md na pasta `/API` com `:::` seguido do caminho onde sua função está (ex: `::: tasks.texto`). Isso fará com que o mkdocstrings encontre sua docstring e documente sua função automaticamente.

As instruções de uso estão documentadas no arquivo `index.md`, então se acrescentar qualquer funcionalidade à nossa aplicação, é lá que terá que documentar.

---

## Comandos necessários

### Ferramentas

Esse projeto usa duas ferramentas para desenvolvimento:

- <a href="https://python-poetry.org/" target="_blank">Poetry</a>: Para o gerenciamento do ambiente e instalação de bibliotecas
- <a href="https://github.com/illBeRoy/taskipy" target="_blank">Taskipy</a>: Para automação de tarefas rotineiras. Como executar os testes, linters, documentação e etc...

Então, garanta que tem o poetry instalado para essa contribuição:

```{ .bash .copy }
pipx install poetry
```

### Passos para executar tarefas específicas

Aqui estão listados comandos que você pode usar para executar tarefas corriqueiras. Como clonar o repositório, como instalar as dependências, executar os testes e etc...

#### Como clonar o repositório

```{ .bash .copy }
git clone https://github.com/LecoOliveira/Palmeiras_News.git
```

#### Como instalar as dependências

```{ .bash .copy }
poetry install
```

#### Como executar o CLI

```{ .bash .copy title="Para comandos do CLI" }
poetry run palmeiras [subcomando]
```
```{ .bash .copy title="Para rodar o programa" }
poetry run palmeiras-run
```

#### Como executar a verificação de código

```{ .bash .copy }
task lint
```

#### Como executar os testes

```{ .bash .copy }
task test
```

#### Como executar a documentação

```{ .bash .copy }
task docs
```