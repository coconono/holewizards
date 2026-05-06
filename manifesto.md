# OK BUT I HEARD THIS AI STUFF WAS BAD FOR YOU

Look, I don't write code by hand. It gives me anxiety. I can't do it. I'm not apologizing.

I use github copilot for my day day job and its helped me quite a bit. I haven't lost the entire company's data because I like to think I'm not an idiot(which I somethings have to fix) I decided to try it on making a game because I wanted to see where the ethicality of it all began and ended. Can I bring to Steam(not EARLY ACCESS) a working not slop game? Could I even from a single .md file build out the core logic pieces so I could focus on the arty parts(like writing the flavor texts and commissioning arts)?

I'd like to say I know completely what I'm doing but this isn't a place for lying to myself or anyone else. I have a rough idea of doing all the code via prompt files, writing a bunch of words, commissioning some art and

I think asking it to do the boring bit(code) is ok. Asking it to make art or write the text? NO GO.

## A plan

- write the prompt_initial.md file
  - I think the fancy vibe coder people want you to call it planning.md file or whatever. I don't care. Its a file name.
- have github copilot build out the project
  - it will make a bunch of mistakes, which is fine. This is how we learn how the project is built, which is important as we move into more complex steps.
- write flavor text
  - intro
  - outro
  - monster descriptions
  - weapon, armor, item, spell descriptions
- github release
  - itially it'll be something someone clones down and runs in their python environment
- refine interface
  - we need a graphical game for Steam. That means art, sounds, QoL, etc.
  - any coding will be built via in prompt_whatever.md files to better control the project without getting lost
- start building out weapons, armor, spells, monsters, etc.
  - initial attempts will be to randomly generate these things, implement tools to adjust and save as artisticly desired
- once we've got the assets more defined, commission artists
  - I have a bunch of young folk that do nothing but doodle. Easy money.
- build "portable" version
  - something that doesn't require the user to be comfortable with python
  - start with a compressed file, extract and run executuable model
- build installer, test releases on github
  - single click method, puts the files in the expected places on OS
- once it starts to visually come together, do an itch.io release
- setup discord or similar chat service for tech support
  - hoodwink people into moderating it
  - check out some bots
