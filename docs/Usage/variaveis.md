# Configurando Variáveis de ambiente

Nesse projeto usamos o [Twilio](https://www.twilio.com/pt-br) para fazer o envio das mensagens.
E essa é basicamente a única configuração que precisamos fazer, para poder usar o nosso script.

Basta se cadastrar no site oficial, e você terá acesso aos tokens e números necessários para a autenticação, podendo assim enviar as mensagens.

><sub> Obs.: O Twilio é um serviço **pago**, mas disponibilizam um período de testes gratuito. Caso queira continuar após o período, confira a tabala de preços.</sub> 

![Imagem Twilio](../assets/imagen_twilio.png)

---

### **Inserindo credenciais**

Com as credenciais em mãos, é hora de inseri-las no código. Elas estão representadas pelas constantes: `ACCOUNT_SID, AUTH_TOKEN, PHONE_NUMBER, DESTINY_PHONE_NUMBER` dentro da função [`enviar_msg()`](/API/tasks/#tasks.envia.enviar_msg).

```python title="app/functions.py"
load_dotenv('/PATH/TO/twilio.env') # Altere para o caminho completo do seu arquivo twilio.env
ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
DESTINY_PHONE_NUMBER = os.environ['TWILIO_DESTINY_PHONE_NUMBER']
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)
```

---

É importante manter as credenciais da conta Twilio seguras, armazenando-as de maneira a impedir o acesso não autorizado. Um método comum é armazená-las em variáveis de ambiente que são acessadas no seu aplicativo. Isso os mantém fora do código e de outros lugares onde as credenciais não pertencem.
Para adicionar as variáveis automaticamente no nosso arquivo, temos os seguintes comandos no CLI do nosso programa que precisarão ser configurados antes de rodar o programa pela primeira vez: ```sid```,  ```token```, ```twilio-phone``` e ```destiny-phone```.

///warning | Importante
Você só pode adicionar um SID, um TOKEN e um TWILIO_PHONE, então cuidado ao adicioná - los.
///

Para adicionar a sua credencial `ACCOUNT_SID` digite no seu terminal:

```bash
palmeiras sid SEU_ACCOUNT_SID
```
O mesmo comando pode ser usado para os demais, como no exemplo:

```bash
palmeiras token SEU_ACCOUNT_TOKEN
```
ou
```bash
palmeiras twilio-phone SEU_TWILIO_PHONE
```

Já no caso do `destiny-phone`, é possível adicionar um ou mais de um número por vez, tendo em vista que podemos querer encaminhar as mensagens para vários números. Para ele digite os números que deseja adicionar separados por espaços:

```bash
palmeiras destiny-phone SEU_DESTINY_PHONE1 SEU_DESTINY_PHONE2 ...
```

/// tip | Atenção
Importante lembrar, que todos os `destiny_phone` devem ser cadastrados e devidamente ativados no seu painel da Twilio. Sem isso, eles não irão receber as mensagens.
/// 

E sim, para cada número cadastrado, será cobrado pela mensagem enviada. A ideia inicial é para que seja um projeto simples, pessoal. Más que também pode ser explorado de formas mais amplas, caso queiram.
