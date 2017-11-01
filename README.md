*SCOPE OF PROJECT*

[1] WarLighter_engine:
    a minimal engine that creates a rectangular grid where every tile is either 1 land or 1 ocean.
    continents are generated from continuous blocks of these 1-tile lands. (that will require some
    skill -- a continuity verifier)
    contains:
    --> functions to read/save maps (which are objects it can create)
    --> functions to randomly generate maps
    --> functions that load maps into board objects that are interactable (boards are composed of maps)
    --> a board object that has attributes for armies and control, and methodS for combat, etc.
[2] WarLight_engine:
    the full geometrical implementation. will be much harder, and does not block any other dev work
    so long as the Lighter_engine works.
[3] WarPy_terminal, a basic terminal-based single player game.
[4] WarPy_graphical, a basic graphical single player game
[5] WarPy_web, a basic web-based interactive single player browser game
[6] WarPy_server, a daemon for hosting interactive sessions
[7] WarPy_client, a renderer for loading interactive network sessions
[8] WarPAI, a package containing:
    --> Neural Networks model generators
    --> If/Else simple AIs
    --> Algorithmic solvers
    --> Etc.
[9] WarRoom, a programmable script for generating data sets by pitting models against maps.
[0] WarDB, a sqlite results, maps, etc data base. All data can be csv anyway.