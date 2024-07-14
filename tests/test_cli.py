import os
import tempfile

from typer.testing import CliRunner

from app.cli.palmeiras import app

runner = CliRunner()

# # SID tests --------------------------------------------------------


def test_id_deve_retornar_um_texto_mostrando_o_id():
    with tempfile.NamedTemporaryFile() as file:
        file.write(b'BOT_ID="teste"')
        file.read()
        result = runner.invoke(app, ['listar', '--id', '--env', file.name])

        assert result.exit_code == 0
        assert 'BOT_ID' in result.stdout


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


def test_bot_token_retorna_erro_se_numero_ja_existe():
    with tempfile.NamedTemporaryFile() as file:
        file.write(b'BOT_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxx')
        file.seek(0)
        result = runner.invoke(
            app, ['bot_token', '--env', file.name, 'xxxxxxxxxxxxxxxxx']
        )

        assert result.exit_code == 1
        assert 'já existe', 'no arquivo' in result.stdout


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
