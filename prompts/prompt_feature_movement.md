# more efficient player input

## movement commands

- move left will have a shortcut command ml
- move right will have a shortcut command mr
- move up will have a shortcut command mu
- move down will have shortcut command md
- move x,y will have a shortcut command mx,y (example move 6,9 will be m6,9)

## turn based movement

- movement for player and monsters are turn based
- when the player moves, the monsters move according to their reinforcement
- monsters are given more reinforcement to move
- when using move x,y(or mx,y) the movement is resolved step by step(allowing monsters to move into the path) with a .5second pause between each move
- if monsters move next to the player this will interrupt the move

## monster behavior

- if the monster doesn't see the player, it will move in any random direction except the one it just moved from
- if the monster can see the player but can't attack, the monster will move closer to the player
- monster default vision range is now set to 10

## attacking, targeting

- attack will now require the monster name
  - example: attack Starchie will attack Starchie
- attack will also have a shortcut a
  - aStarchie will attack Starchie
- if the player does not specify a target, the log will display a list of available targets
