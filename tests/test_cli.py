from typer.testing import CliRunner

from app.cli import cli

runner = CliRunner()


def test_sid_deve_retornar_0_se_rodar():
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0


def test_sid_deve_retornar_um_texto():
    result = runner.invoke(cli, ['show', '--sid'])
    assert 'TWILIO_ACCOUNT_SID' in result.stdout


def test_sid_deve_retornar_a_lista_de_variaveis():
    result = runner.invoke(cli, ['show'])
    assert 'TWILIO_ACCOUNT_SID' in result.stdout


def test_destiny_phone_ja_contem_no_arquivo():
    result = runner.invoke(cli, ['destiny-phone', 'teste'])
    assert result.exit_code == 0
    assert 'teste' in result.stdout
    assert 'já existe no arquivo' in result.stdout


def test_sid_ja_contem_no_arquivo():
    result = runner.invoke(cli, ['sid', 'teste'])
    assert result.exit_code == 0
    assert 'já existe no arquivo' in result.stdout


def test_token_ja_contem_no_arquivo():
    result = runner.invoke(cli, ['token', 'teste'])
    assert result.exit_code == 0
    assert 'já existe no arquivo' in result.stdout


def test_twilio_phone_ja_contem_no_arquivo():
    result = runner.invoke(cli, ['twilio-phone', 'teste'])
    assert result.exit_code == 0
    assert 'já existe no arquivo' in result.stdout
