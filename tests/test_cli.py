import os

from typer.testing import CliRunner

from app.cli import cli

runner = CliRunner()

# SID tests --------------------------------------------------------


def test_sid_deve_retornar_0_se_rodar():
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0


def test_sid_deve_retornar_um_texto_mostrando_o_sid():
    result = runner.invoke(cli, ['show', '--sid'])
    assert 'TWILIO_ACCOUNT_SID' in result.stdout


def test_sid_cria_arquivo_se_nao_existe():
    result = runner.invoke(cli, ['sid', 'teste', 'temp_file.txt'])
    assert result.exit_code == 0
    assert 'TWILIO_ACCOUNT_SID' in result.stdout
    os.remove('temp_file.txt')


def test_sid_ja_contem_no_arquivo():
    result = runner.invoke(cli, ['sid', 'teste'])
    assert result.exit_code == 0
    assert 'já existe no arquivo' in result.stdout


# listar tests -----------------------------------------------------


def test_listar_deve_retornar_todas_as_variaveis_cadastradas():
    result = runner.invoke(cli, ['show'])
    assert 'TWILIO_' in result.stdout


# destiny_phone tests ----------------------------------------------


def test_destiny_phone_ja_contem_no_arquivo():
    result = runner.invoke(cli, ['destiny-phone', 'teste'])
    assert result.exit_code == 0
    assert 'já existe no arquivo' in result.stdout


def test_destiny_phone_cria_arquivo_se_nao_existe():
    result = runner.invoke(
        cli, ['destiny-phone', 'teste', '--env', 'temp_file.txt']
    )
    assert result.exit_code == 0
    assert 'TWILIO_DESTINY_PHONE_NUMBER' in result.stdout
    os.remove('temp_file.txt')


def test_destiny_phone_cria_novo_numero_se_numero_nao_existe():
    with open('temp_file.txt', 'w') as file:
        file.write('TWILIO_DESTINY_PHONE_NUMBER="teste"')
    result = runner.invoke(
        cli, ['destiny-phone', 'teste1', '--env', 'temp_file.txt']
    )
    assert result.exit_code == 0
    assert 'TWILIO_DESTINY_PHONE_NUMBER' in result.stdout
    os.remove('temp_file.txt')


# token tests ------------------------------------------------------


def test_token_ja_contem_no_arquivo():
    result = runner.invoke(cli, ['token', 'teste'])
    assert result.exit_code == 0
    assert 'já existe no arquivo' in result.stdout


# twilio_phone tests -----------------------------------------------


def test_twilio_phone_ja_contem_no_arquivo():
    result = runner.invoke(cli, ['twilio-phone', 'teste'])
    assert result.exit_code == 0
    assert 'já existe no arquivo' in result.stdout
