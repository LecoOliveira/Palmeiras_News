from app.tasks.formata import *


def test_formata_texto_deve_retronar_um_str():
    assert isinstance(formata_texto(), str)
