# Configurando Variáveis de ambiente

Nesse projeto usamos o [Twilio](https://www.twilio.com/pt-br) para fazer o envio das mensagens.
E essa é basicamente a única configuração que precisamos fazer, para poder usar o nosso script.

Basta se cadastrar no site oficial, e você terá acesso aos tokens e números necessários para a autenticação, podendo assim enviar as mensagens.

><sub> Obs.: O Twilio é um serviço **pago**, mas disponibilizam um período de testes gratuito. Caso queira continuar após o período, confira a tabala de preços.</sub> 

![Imagem Twilio](../assets/imagen_twilio.png)

---

### **Inserindo credenciais**

Com as credenciais em mãos, é hora de inseri-las no código. Elas estão representadas pelas constantes: `ACCOUNT_SID, AUTH_TOKEN, PHONE_NUMBER, DESTINY_PHONE_NUMBER` dentro da função [`enviar_msg()`](../API/functions.md).

```python title="app/functions.py"
load_dotenv('/PATH/TO/twilio.env') # Altere para o caminho completo do seu arquivo twilio.env
ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
DESTINY_PHONE_NUMBER = os.environ['TWILIO_DESTINY_PHONE_NUMBER']
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)
```

---

É importante manter as credenciais da conta Twilio seguras, armazenando-as de maneira a impedir o acesso não autorizado. Um método comum é armazená-las em variáveis de ambiente que são acessadas no seu aplicativo. Isso os mantém fora do código e de outros lugares onde as credenciais não pertencem. Vamos dar uma olhada em como trabalhar com variáveis de ambiente. Aqui estamos utilizando o Linux, mas se esta usando Windows, pode conferir como configuras suas variáveis [aqui](https://www.twilio.com/docs/usage/secure-credentials). 


```bash title="bash"
echo "export TWILIO_ACCOUNT_SID='ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'" > twilio.env
echo "export TWILIO_AUTH_TOKEN='your_auth_token'" >> twilio.env
echo "export TWILIO_PHONE_NUMBER='your_phone_number'" >> twilio.env
echo "export TWILIO_DESTINY_PHONE_NUMBER='destiny_phone_number'" >> twilio.env
```

><sub> O `destiny_phone_number` é o número para onde será enviada a mensagem, mas não pode ser qualquer número. Ele deve ser devidamente cadastrado e ativado no seu painel na Twilio.</sub>


/// tip | Atenção
Por segurança, as credenciais da conta Twilio devem ser armazenadas em uma variável de ambiente.
Veja mais informações de como armazenar as [variáveis de ambiente](https://www.twilio.com/docs/usage/secure-credentials) e de [como acessa-las](https://www.twilio.com/blog/environment-variables-python).
///  


Examples:
```python
    >>> data_jogo()
    '24/05'
```