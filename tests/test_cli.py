import os

from typer.testing import CliRunner

from app.cli import cli

runner = CliRunner()

# SID tests --------------------------------------------------------


def test_sid_deve_retornar_0_se_rodar():
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0


def test_sid_deve_retornar_um_texto_mostrando_o_sid():
    with open('temp_file.txt', 'w') as file:
        file.write('TWILIO_ACCOUNT_SID="teste"')
    result = runner.invoke(cli, ['listar', '--sid', '--env', 'temp_file.txt'])
    assert result.exit_code == 0
    assert 'TWILIO_ACCOUNT_SID' in result.stdout
    os.remove('temp_file.txt')


def test_sid_cria_arquivo_se_nao_existe():
    result = runner.invoke(cli, ['sid', 'teste', '--env', 'temp_file.txt'])
    assert result.exit_code == 0
    assert 'TWILIO_ACCOUNT_SID' in result.stdout
    os.remove('temp_file.txt')


def test_sid_ja_contem_no_arquivo():
    with open('temp_file.txt', 'w') as file:
        file.write('TWILIO_ACCOUNT_SID="teste"')
    result = runner.invoke(cli, ['sid', 'teste', '--env', 'temp_file.txt'])
    assert result.exit_code == 0
    assert 'já existe', 'no arquivo' in result.stdout
    os.remove('temp_file.txt')


# listar tests -----------------------------------------------------


def test_listar_deve_retornar_todas_as_variaveis_cadastradas():
    with open('temp_file.txt', 'w') as file:
        file.write('TWILIO_ACCOUNT_SID="teste"')
    result = runner.invoke(cli, ['listar', '--env', 'temp_file.txt'])
    assert result.exit_code == 0
    assert 'TWILIO_' in result.stdout
    os.remove('temp_file.txt')


def test_listar_deve_retornar_mensagem_de_erro_ao_ler_arquivo():
    result = runner.invoke(cli, ['listar', '--sid', '--env', 'temp_file.txt'])
    assert result.exit_code == 0
    assert 'Erro ao ler o arquivo' in result.stdout


def test_listar_deve_retornar_mensagem_de_erro_ao_nao_identificar_a_variavel():
    with open('temp_file.txt', 'w'):
        result = runner.invoke(
            cli, ['listar', '--sid', '--env', 'temp_file.txt']
        )
        assert result.exit_code == 0
        assert 'Nenhuma variável de ambiente' in result.stdout
        os.remove('temp_file.txt')


def test_listar_deve_retornar_um_erro_ao_nao_encontrar_arquivo():
    result = runner.invoke(cli, ['listar', '--env', 'temp_file.txt'])
    assert result.exit_code == 0
    assert 'Nenhum arquivo' in result.stdout


# destiny_phone tests ----------------------------------------------


def test_destiny_phone_formato_invalido():
    result = runner.invoke(
        cli, ['destiny-phone', '+551194022', '--env', 'temp_file.txt']
    )
    assert result.exit_code == 0
    assert 'O número deve conter' in result.stdout


def test_destiny_phone_cria_arquivo_se_não_existe():
    result = runner.invoke(
        cli, ['destiny-phone', '+551194022222', '--env', 'temp_file.txt']
    )
    assert result.exit_code == 0
    assert 'com sucesso' in result.stdout
    os.remove('temp_file.txt')


def test_destiny_phone_cria_arquivo_se_nao_existe():
    result = runner.invoke(
        cli, ['destiny-phone', '+55000000000000', '--env', 'temp_file.txt']
    )
    assert result.exit_code == 0
    assert 'TWILIO_DESTINY_PHONE_NUMBER' in result.stdout
    os.remove('temp_file.txt')


def test_destiny_phone_cria_novo_numero_se_numero_nao_existe():
    with open('temp_file.txt', 'w') as file:
        file.write('TWILIO_DESTINY_PHONE_NUMBER="+1111900000000"')
    result = runner.invoke(
        cli, ['destiny-phone', '+00000000000000', '--env', 'temp_file.txt']
    )
    assert result.exit_code == 0
    assert 'TWILIO_DESTINY_PHONE_NUMBER' in result.stdout
    os.remove('temp_file.txt')


def test_destiny_phone_retorna_erro_se_numero_ja_existe():
    with open('temp_file.txt', 'w') as file:
        file.write('TWILIO_DESTINY_PHONE_NUMBER="+1111900000000"')
    result = runner.invoke(
        cli, ['destiny-phone', '+1111900000000', '--env', 'temp_file.txt']
    )
    assert result.exit_code == 0
    assert 'já existe', 'no arquivo' in result.stdout
    os.remove('temp_file.txt')


# token tests ------------------------------------------------------


def test_token_cria_arquivo_se_nao_existe():
    result = runner.invoke(cli, ['token', 'test', '--env', 'temp_file.txt'])
    assert result.exit_code == 0
    assert 'TWILIO_AUTH_TOKEN' in result.stdout
    os.remove('temp_file.txt')


def test_token_ja_contem_no_arquivo():
    with open('temp_file.txt', 'w') as file:
        file.write('TWILIO_AUTH_TOKEN="teste')
    result = runner.invoke(cli, ['token', 'teste', '--env', 'temp_file.txt'])
    assert result.exit_code == 0
    assert 'já existe', 'no arquivo' in result.stdout
    os.remove('temp_file.txt')


# twilio_phone tests -----------------------------------------------


def test_twilio_phone_ja_contem_no_arquivo():
    with open('temp_file.txt', 'w') as file:
        file.write('TWILIO_PHONE_NUMBER="teste"')
    result = runner.invoke(
        cli, ['twilio-phone', 'teste', '--env', 'temp_file.txt']
    )
    assert result.exit_code == 0
    assert 'já existe', 'no arquivo' in result.stdout
    os.remove('temp_file.txt')


# delete tests -----------------------------------------------------


def test_delete_exclui_variavel():
    with open('temp_file.txt', 'w') as file:
        file.write('TWILIO_ACCOUNT_SID="teste"')
    result = runner.invoke(cli, ['delete', 'sid', '--env', 'temp_file.txt'])
    assert result.exit_code == 0
    assert 'TWILIO_ACCOUNT_SID' in result.stdout
    os.remove('temp_file.txt')


def test_delete_nao_encontra_variavel():
    file = open('temp_file.txt', 'w')
    result = runner.invoke(cli, ['delete', 'sid', '--env', 'temp_file.txt'])
    assert result.exit_code == 0
    assert 'O arquivo não contém nenhum' in result.stdout
    file.close()
    os.remove('temp_file.txt')
