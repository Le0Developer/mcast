
from mcfunction.versions.mc_1_8.tellraw import tellraw, ParsedTellrawCommand
from mcfunction.nodes import EntityNode


def test_tellraw():
    parsed = tellraw.parse('tellraw @s {"text":"test successful"}')
    parsed: ParsedTellrawCommand

    assert isinstance(parsed.target, EntityNode)
    assert parsed.message.object['text'] == 'test successful'

    assert str(parsed) == 'tellraw @s {"text":"test successful"}'
