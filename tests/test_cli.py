import os
import tempfile

from typer.testing import CliRunner

from app.cli.palmeiras import app

runner = CliRunner()

# # SID tests --------------------------------------------------------


# def test_sid_deve_retornar_0_se_rodar():
#     result = runner.invoke(app, ['--help'])
#     assert result.exit_code == 0


def test_id_deve_retornar_um_texto_mostrando_o_id():
    with tempfile.NamedTemporaryFile() as file:
        file.write(b'BOT_ID="teste"')
        file.read()
        result = runner.invoke(app, ['listar', '--id', '--env', file.name])

        assert result.exit_code == 0
        assert 'BOT_ID' in result.stdout


# def test_id_cria_arquivo_se_nao_existe():
#     with tempfile.NamedTemporaryFile() as file:
#         result = runner.invoke(app, ['id', '--env', file.name, 'teste'])

#         assert result.exit_code == 0
#         assert 'BOT_ID' in result.stdout


# def test_sid_ja_contem_no_arquivo():
#     with tempfile.NamedTemporaryFile() as file:
#         file.write(b'TWILIO_ACCOUNT_SID="teste"')
#         file.seek(0)
#         result = runner.invoke(app, ['sid', '--env', file.name, 'teste'])

#         assert result.exit_code == 0
#         assert 'já existe', 'no arquivo' in result.stdout


# listar tests -----------------------------------------------------


def test_listar_deve_retornar_todas_as_variaveis_cadastradas():
    with tempfile.NamedTemporaryFile() as file:
        file.write(b'BOT_ID="teste"')
        file.seek(0)
        result = runner.invoke(app, ['listar', '--env', file.name])

        assert result.exit_code == 0
        assert 'BOT_ID' in result.stdout


def test_listar_deve_retornar_mensagem_de_erro_ao_ler_arquivo():
    result = runner.invoke(app, ['listar', '--id', '--env', 'temp_file.txt'])

    assert result.exit_code == 0
    assert 'Erro ao ler o arquivo' in result.stdout


def test_listar_deve_retornar_mensagem_de_erro_ao_nao_identificar_a_variavel():
    with tempfile.NamedTemporaryFile() as file:
        result = runner.invoke(app, ['listar', '--id', '--env', file.name])

        assert result.exit_code == 0
        assert 'Nenhuma variável de ambiente' in result.stdout


def test_listar_deve_retornar_um_erro_ao_nao_encontrar_arquivo():
    result = runner.invoke(app, ['listar', '--env', 'temp_file.txt'])

    assert result.exit_code == 0
    assert 'Nenhum arquivo' in result.stdout


# destiny_phone tests ----------------------------------------------


# def test_destiny_phone_formato_invalido():
#     result = runner.invoke(
#         app, ['destiny-phone', '--env', 'temp_file.txt', '+551194022']
#     )

#     assert result.exit_code == 0
#     assert 'número deve conter' in result.stdout


# def test_destiny_phone_cria_arquivo_se_não_existe():
#     with tempfile.NamedTemporaryFile() as file:
#         result = runner.invoke(
#             app, ['destiny-phone', '--env', file.name, '+551194022222']
#         )

#         assert result.exit_code == 0
#         assert 'com sucesso', 'TWILIO_DESTINY_PHONE_NUMBER' in result.stdout


def test_bot_token_fecha_arquivo():
    file = tempfile.TemporaryFile()
    result = runner.invoke(
        app,
        [
            'bot_token',
            '--env',
            file,
            'blablabla',
        ],
    )
    os.remove(f'<_io.BufferedRandom name={file.name}>')
    file.close()

    assert result.exit_code == 1
    assert 'com sucesso', 'BOT_TOKEN' in result.stdout


# def test_destiny_phone_cria_novo_numero_se_numero_nao_existe():
#     with tempfile.NamedTemporaryFile() as file:
#         file.write(b'TWILIO_DESTINY_PHONE_NUMBER="+1111900000000"')
#         file.seek(0)
#         result = runner.invoke(
#             app, ['destiny-phone', '--env', file.name, '+00000000000000']
#         )

#         assert result.exit_code == 0
#         assert 'TWILIO_DESTINY_PHONE_NUMBER' in result.stdout


# def test_destiny_phone_configura_mais_de_um_numero():
#     numero_1 = '+55000000000000'
#     numero_2 = '+55222222222222'

#     with tempfile.NamedTemporaryFile() as file:
#         result = runner.invoke(
#             app, ['destiny-phone', '--env', file.name, numero_1, numero_2]
#         )

#         assert numero_1, numero_2 in result.stdout
#         assert result.exit_code == 0


def test_bot_token_retorna_erro_se_numero_ja_existe():
    with tempfile.NamedTemporaryFile() as file:
        file.write(b'BOT_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxx')
        file.seek(0)
        result = runner.invoke(
            app, ['bot_token', '--env', file.name, 'xxxxxxxxxxxxxxxxx']
        )

        assert result.exit_code == 1
        assert 'já existe', 'no arquivo' in result.stdout


# token tests ------------------------------------------------------


# def test_token_cria_arquivo_se_nao_existe():
#     with tempfile.NamedTemporaryFile() as file:
#         result = runner.invoke(app, ['token', '--env', file.name, 'test'])

#         assert result.exit_code == 0
#         assert 'TWILIO_AUTH_TOKEN' in result.stdout


# def test_token_ja_contem_no_arquivo():
#     with tempfile.NamedTemporaryFile() as file:
#         file.write(b'TWILIO_AUTH_TOKEN="teste')
#         result = runner.invoke(app, ['token', '--env', file.name, 'teste'])

#         assert result.exit_code == 0
#         assert 'já existe', 'no arquivo' in result.stdout


# twilio_phone tests -----------------------------------------------


# def test_twilio_phone_ja_contem_no_arquivo():
#     with tempfile.NamedTemporaryFile() as file:
#         file.write(b'TWILIO_PHONE_NUMBER="teste"')
#         result = runner.invoke(
#             app, ['twilio-phone', '--env', file.name, 'teste']
#         )

#         assert result.exit_code == 0
#         assert 'já existe', 'no arquivo' in result.stdout


# delete tests -----------------------------------------------------


def test_delete_exclui_variavel():
    with tempfile.NamedTemporaryFile(mode='w+') as file:
        file.write('BOT_ID="teste"')
        file.seek(0)
        result = runner.invoke(app, ['delete', '--env', file.name, 'id'])

        assert result.exit_code == 0
        assert 'BOT_ID' in result.stdout


def test_delete_nao_encontra_variavel():
    with tempfile.NamedTemporaryFile() as file:
        result = runner.invoke(app, ['delete', '--env', file.name, 'id'])

        assert result.exit_code == 0
        assert 'O arquivo não contém nenhum' in result.stdout


def test_telegram_token_cria_arquivo_se_nao_existe_retorna_erro():
    with tempfile.NamedTemporaryFile() as file:
        result = runner.invoke(app, ['bot_token', '--env', file.name, 'test'])

        assert result.exit_code == 1
        assert 'BOT_TOKEN' in result.stdout
