# Controller Dock

This plugin is a simple wrapper around scawp's [Steam-Deck.Auto-Disable-Steam-Controller](https://github.com/scawp/Steam-Deck.Auto-Disable-Steam-Controller/) script.
This script makes it much easier to treat your Steam Deck as a portable home console.
If you connect any external controllers, then the Steam Deck's built-in controller will be disconnected.
This prevents users from having to fight with the built-in controller taking over in the controller order.

For more information about the script, see scawp's repo linked above.

## Installation

Install the plugin from the Decky store and the script will already be working!
Just hook up a controller to see.

## Permissions

The only permission requirement for Controller Dock is root access.
This is only used to create files in `/etc/udev/rules.d`.
The rule files created in this directory are what activate the script.
Since this directory is owned by root, and is not other-writable, root access is required.
