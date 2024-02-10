# Decky Controller Dock

This simple Decky plugin for the Steam Deck makes it easy to install and use scawp's
[Steam Deck Auto Disable Steam Controller](https://github.com/scawp/Steam-Deck.Auto-Disable-Steam-Controller)
script.

## scawp's script

This plugin contains the script from
[my own fork](https://github.com/TacticalLaptopBag/Steam-Deck.Auto-Disable-Steam-Controller/tree/patch-1)
, which is forked off of
[Mazebird's patch](https://github.com/Mazebird/Steam-Deck.Auto-Disable-Steam-Controller/tree/patch-1)
.

This is forked from Mazebird's patch because the original script broke with SteamOS 3.5,
and Mazebird made a fix which scawp has yet to pull into the main repo.
Seeing as scawp hasn't made a commit to the main branch in over a year,
I'm not certain if it will ever be merged.
See
[this issue](https://github.com/scawp/Steam-Deck.Auto-Disable-Steam-Controller/issues/5)
for more information.
If this change gets merged and I don't catch it, open an issue!

The reason for
[my own fork](https://github.com/TacticalLaptopBag/Steam-Deck.Auto-Disable-Steam-Controller/tree/patch-1)
is that this plugin contains the script itself.
In order for the script to be executed properly,
the udev rule config must point to the script that is contained inside the plugin.
