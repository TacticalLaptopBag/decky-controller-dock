import os
import shutil
# from urllib.request import urlretrieve

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code one directory up
# or add the `decky-loader/plugin` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky_plugin

# Dirs
RULES_DEST_DIR = "/etc/udev/rules.d"
SCRIPT_PATH = "/home/deck/homebrew/plugins/Controller-Dock/Steam-Deck.Auto-Disable-Steam-Controller"

DISABLED_PATH = f"{SCRIPT_PATH}/conf/disabled"

initialized = False

class Plugin:
    async def is_enabled(self):
        return not os.path.exists(DISABLED_PATH)


    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        global initialized;
        if initialized:
            return

        initialized = True
        decky_plugin.logger.info("Hello World!")

        shutil.copy2(f"{SCRIPT_PATH}/99-disable-steam-input.rules", RULES_DEST_DIR)
        decky_plugin.logger.info(f"Copied steam input rules to {RULES_DEST_DIR}")

        os.system("udevadm control --reload")
        decky_plugin.logger.info("Reloaded services")

        os.chmod(f"{SCRIPT_PATH}/disable_steam_input.sh", 0o555)
        decky_plugin.logger.info("Set permissions on scawp script")


    # Function called first during the unload process, utilize this to handle your plugin being removed
    async def _unload(self):
        decky_plugin.logger.info("Goodbye World!")


    async def disable(self):
        global enabled
        decky_plugin.logger.info("Disabling scawp's script...")
        # Create disabled file
        with open(DISABLED_PATH, "w") as file:
            os.chown(DISABLED_PATH, 1000, 1000)

        decky_plugin.logger.info("Disabled scawp's script")


    async def enable(self):
        global enabled
        decky_plugin.logger.info("Enabling scawp's script...")
        os.remove(DISABLED_PATH)
        decky_plugin.logger.info("Enabled scawp's script")


    # Migrations that should be performed before entering `_main()`.
    async def _migration(self):
        decky_plugin.logger.info("Migrating")
        
