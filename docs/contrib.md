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
A task seguinte é a <a href="/API/tasks/#tasks.formata.formata_texto" target="_blank">`formata_texto()`</a> no arquivo `formata.py`.

Como o nome sugere, ela formata o texto recebido pela `texto_msg()` e deixa pronto para envio. Para isso, usamos uma função do Rocketry chamada `after_success()`, que fica monitorando a task anterior, e quando bem sucedida, pega a lista retornada com o texto a ser formatado.

```py
@group.task(after_success(texto_msg))
def formata_texto(texto: list = Return(texto_msg)) -> str:

```

```py title="formata_texto()"
'Jogo: Palmeiras x Flamengo | Campeonato Brasileiro (14ª rodada)'

'Data e hora: 08/07/2023 | 21h'

'Local: Allianz Parque, em São Paulo (SP)'

```

---
#### tests

Para os testes optei por usar o <a href="https://docs.pytest.org/en/7.3.x/" target="_blank">pytest</a> por ter mais familiaridade. As configurações dele podem ser encontradas no arquivo <a href="https://github.com/LecoOliveira/Palmeiras_News/blob/main/pyproject.toml" target="_blank">pyproject.toml</a> na raiz do projeto. Você vai notar que temos bastante testes rodando, mas alguns são bem básicos, só para ver se a coisa toda ta legal e rodando bem. Caso queira implementar outros testes mais aprofundados, sinta-se a vontade.

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