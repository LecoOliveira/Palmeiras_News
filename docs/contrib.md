# Como contribuir

Primeiramente, gostaria de agradecer por ter chegado até aqui. Esse é um projeto de estudo e tenho aprendido bastante com ele desde o início. 
Então, qualquer ajuda, por menor que ela seja, será de **GRANDE** valia! *Muito obrigado*! :star2::muscle:


## O projeto

Esse é um projeto bem simples, constituído basicamente de um agendador de tarefas feito com o <a href="https://rocketry.readthedocs.io/en/stable/" target="_blank">Rocketry</a>, que controla o fluxo de um web scraping feito usando o <a href="https://beautiful-soup-4.readthedocs.io/en/latest/" target="_blank">BeatifulSoup</a>. E para configurar as variáveis de ambiente do usuário, e dar uma carinha *bonitinha* pro nosso programa, construí um CLI com o <a href="https://typer.tiangolo.com/" target="_blank">Typer</a>.

### Estrutura

O projeto é estruturado basicamente em três pastas:

|   PASTA   |                       DESCRIÇÃO                                               |
|-----------|-------------------------------------------------------------------------------|
| **app**   |Pasta base do nosso projeto, onde está todo o código principal e também o CLI. |
| **tests** | Onde armazenamos todos os nossos testes.                                      |
| **docs**  | E a pasta responsável pela documentação.                                      |

#### app



#### tests

Para os testes optei por usar o <a href="https://docs.pytest.org/en/7.3.x/" target="_blank">pytest</a> por ter mais familiaridade. As configurações dele podem ser encontradas no arquivo <a href="https://github.com/LecoOliveira/Palmeiras_News/blob/main/pyproject.toml" target="_blank">pyproject.toml</a> na raiz do projeto. Você vai notar que temos bastante testes rodando, mas alguns são bem básicos, só para ver se a coisa toda ta legal e rodando bem. Caso queira implementar outros testes mais aprofundados, sinta-se a vontade.

/// tip | IMPORTANTE
Caso implemente algo na aplicação, **SEMPRE** teste!
Os testes são fundamentais para o funcionamento do projeto.
///


#### docs

Para a documentação, estou utilizando o <a href="https://www.mkdocs.org/" target="_blank">mkdocs</a> com o tema <a href="https://squidfunk.github.io/mkdocs-material/" target="_blank">mkdocs-material</a> e você pode encontrar todas as configurações no arquivo <a href="https://github.com/LecoOliveira/Palmeiras_News/blob/main/mkdocs.yml" target="_blank">mkdocs.yml</a>. 

Também estou utilizando o <a href="https://mkdocstrings.github.io/" target="_blank">mkdocstrings</a> que está gerando a documentação da nossa API automaticamente usando as docstrings das nossas funções no python (seguindo o padrão <a href="https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html">docstrings do google</a>).

Então você verá alguns arquivos com os seguintes códigos em `/API`:

```md
# Funções principais
::: tasks.texto
    options:
      show_root_toc_entry: false 
::: tasks.formata
    options:
      show_root_toc_entry: false
::: tasks.envia
    options:
      show_root_toc_entry: false
```