
# Minecraft command parser

Command parser and reconstructor for minecraft commands in pure python (requires python3.7+).

This is currently version **[Minecraft 1.16 only](<#versions>)**.


## Parsing & Reconstructing

You can use the `parse_command` function to parse a command.

```python
from mcfunction import parse_command
from mcfunction.commands.summon import ParsedSummonCommand

command = parse_command('summon minecraft:ender_dragon ~ ~ ~')
# command is the parsed command
command: ParsedSummonCommand  # for type-hinting

# you can use 'str(command)' to construct the command from the parsed command
print(command)  # print() automatically calls str()
print(repr(command))  # bypasses str() and lets you see the real 'command'

# modify the node of the summoned entity
command.entity.name = 'wither'

# reconstruction will show the changed command
print(command)
```


## Creating ParsedCommand manually

You can create the `ParsedCommand` directly if you don't have a string for `parse_command`.

```python
from mcfunction import nodes
from mcfunction.commands.summon import ParsedSummonCommand

command = ParsedSummonCommand(
    'summon',  # first argument is always the command name  (for alias support)
    nodes.NamespaceIDNode('minecraft', 'elder_guardian'),
    nodes.PositionNode(
        nodes.CoordinateNode(0, relative=True),
        nodes.CoordinateNode(0, relative=True),
        nodes.CoordinateNode(0, relative=True)
    )
)

print(command)
```

## Creating your own commands

It's actually really simple. Let's assume you have a `greet` command and its
syntax is `greet <target> [message]`.

<details>
<summary>Greet Command</summary>
<p>

```python
from dataclasses import dataclass

from mcfunction.commands import Command, ParsedCommand, Parser
from mcfunction.nodes import EntityNode, RawNode
from mcfunction.parser_types import Entity, GreedyAny


# you don't need to use dataclasses, you can create the __init__ yourself
@dataclass()
class ParsedGreetCommand(ParsedCommand):
    command: str

    target: EntityNode  # the target of your command

    reason: RawNode = None  # raw text, but it's optional, so ' = None'

    # this is the construction function, this should return the command as
    #   string
    def __str__(self):
        if self.reason is not None:
            # EntityNode and RawNode have a __str__ too, so you can just use
            # them in f-strings like this
            return f'{self.command} {self.target} {self.reason}'
        return f'{self.command} {self.target}'


# now you can create your command
greet = Command('greet', parsed=ParsedGreetCommand)

# add your syntax
greet.add_variation(
    # parses a 'Entity' and puts the parsed node into the 'target' field
    Parser(Entity(), 'target'),
    # 'GreedyAny' parses all the remaining arguments into a single node
    Parser(GreedyAny(), 'reason')
)
# and add the variation without reason
greet.add_variation(
    Parser(Entity(), 'target')
)

# and now you have your own command, you can use 'greet.parse' or add the
# command to the command list to make it useable in 'parse_command'

# parsed = greet.parse('greet @a Hello World')

# from mcfunction.commands import commands, command_lookup
# commands.append(greet)
# command_lookup[greet.name] = greet
# from mcfunction import parse_command
# parsed = parse_command('greet @a Hello World')
```

</p>
</details>


## Parsing & Reconstruction of .mcfunction files

You can use the `parse_mcfunction` function to parse a mcfunction file.

You could parse each line with `parse_command`, but you'd need to ignore
comments and blank lines (so it doesn't crash).  `parse_mcfunction` handles
blank lines and comments for you.

```python
from mcfunction import parse_mcfunction
from mcfunction.mcfunction import NoCommand

commands = [
    '# summon enderdragon'
    'summon minecraft:ender_dragon ~ ~ ~',
    '',
    '#summon wither',  # both comment styles supported
    'summon minecraft:wither ~ ~ ~',
]
mcfunction = parse_mcfunction(commands)

# get the summon commands by simply accessing the list
summon_enderdragon = mcfunction.commands[1]
summon_wither = mcfunction.commands[4]

for command in mcfunction.commands:
    # only print commands, not blank lines or comments
    if not isinstance(command, NoCommand):
        print('command', command)

# you can access the comment
print(mcfunction.commands[0].comment.value)
# change it;
mcfunction.commands[0].comment.value = 'summon sheep'
summon_enderdragon.entity.name = 'sheep'
# you can also change the style
mcfunction.commands[2].command = '# '
```


## Versions

The current command syntaxes are (probably) only going to work on Minecraft 1.16.

Other versions are planned, but will take time.


## Dependencies

This project does not use any external dependencies, except for development/testing.

- `pytest`
  - pytest is used for testing the program, install it with
    `pip install pytest`
  - `make test` for testing

- `flake8`
  - flake8 is used for linting the program, install it with
    `pip install flake8`
  - `make lint` for linting

- `coverage`
  - coverage is used for generating test coverage, install it with
    `pip install coverage`
  - `make coverage` for generating the test coverage (requires `pytest`)
