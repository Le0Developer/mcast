
from mcfunction.versions.mc_1_11.locate import locate, ParsedLocateCommand


def test_locate():
    parsed = locate.parse('locate test')
    parsed: ParsedLocateCommand

    assert parsed.structure.value == 'test'

    assert str(parsed) == 'locate test'
