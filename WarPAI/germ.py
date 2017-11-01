"""
SCOPE:

Player classes that interact with the Game API.
These player classes should have:
[1] A species attribute
[2] A perception model, simple feed-forward network for perceiving tile value that takes as inputs:
    -- the surrounding 3? 4? layers of tiles? with fog of war, of course.
    -- the attributes of the neighboring tile players
    -- the attributes of the neighboring tiles -- continent, continent multipliers, etc.

When a species secures a continent, all species-players should receive a bonus.

Species should be determined programmatically by something fairly concrete.
"""