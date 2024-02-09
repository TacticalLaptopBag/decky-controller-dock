import os
import shutil
# from urllib.request import urlretrieve

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code one directory up
# or add the `decky-loader/plugin` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky_plugin

# scawp's repo
# REPO_URL = "http://raw.githubusercontent.com/scawp/Steam-Deck.Auto-Disable-Steam-Controller/main"

# Mazebird's repo
REPO_URL = "http://raw.githubusercontent.com/Mazebird/Steam-Deck.Auto-Disable-Steam-Controller/patch-1"

# Dirs
TMP_DIR = "/tmp/scawp.SDADSC.install"
RULES_INSTALL_DIR = "/etc/udev/rules.d"
SCRIPT_INSTALL_DIR = "/home/deck/.local/share/scawp/SDADSC"
SCRIPT_CONF_DIR = f"{SCRIPT_INSTALL_DIR}/conf"

SCRIPT_DEST_PATH = f"{SCRIPT_INSTALL_DIR}/disable_steam_input.sh"
DEVICE_LIST_DEST_PATH = f"{SCRIPT_CONF_DIR}/simple_device_list.txt"
RULES_DEST_PATH = f"{RULES_INSTALL_DIR}/99-disable-steam-input.rules"
DISABLED_PATH = f"{SCRIPT_CONF_DIR}/disabled"

enabled = not os.path.exists(DISABLED_PATH)

initialized = False

class Plugin:
    # A normal method. It can be called from JavaScript using call_plugin_function("method_1", argument1, argument2)
    async def add(self, left, right):
        return left + right

    def _download_file(file_name):
        url = f"{REPO_URL}/{file_name}"
        dest = f"{TMP_DIR}/{file_name}"
        decky_plugin.logger.info(f"Downloading {url}")
        # return urlretrieve(url, f"{TMP_DIR}/{file_name}")[0]
        os.system(f"curl -o \"{dest}\" \"{url}\"")
        return dest

    def _remove_path(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)

    async def is_enabled(self):
        global enabled
        return enabled

    def install():
        decky_plugin.logger.info("Installing scawp's script...")

        if os.path.exists(SCRIPT_DEST_PATH):
            decky_plugin.logger.info("scawp's script is already installed!")
            return False
        
        decky_plugin.logger.info(f"Making tmp directory {TMP_DIR}")
        if os.path.exists(TMP_DIR):
            decky_plugin.logger.warn("Found existing tmp directory! Did previous installation fail?")
        
        os.mkdir(TMP_DIR)
        
        decky_plugin.logger.info("Downloading files...")
        script_path = Plugin._download_file("disable_steam_input.sh")
        device_list_path = Plugin._download_file("simple_device_list.txt")
        rules_path = Plugin._download_file("99-disable-steam-input.rules")

        decky_plugin.logger.info(f"Making script directory {SCRIPT_INSTALL_DIR}")
        os.makedirs(SCRIPT_CONF_DIR, exist_ok=True)

        decky_plugin.logger.info(f"Copying {device_list_path} to {DEVICE_LIST_DEST_PATH}")
        shutil.copy2(device_list_path, DEVICE_LIST_DEST_PATH)

        decky_plugin.logger.info(f"Copying {script_path} to {SCRIPT_DEST_PATH}")
        shutil.copy2(script_path, SCRIPT_DEST_PATH)

        decky_plugin.logger.info("Setting script permissions")
        os.chmod(SCRIPT_DEST_PATH, 0o555)

        decky_plugin.logger.info(f"Copying {rules_path} to {RULES_DEST_PATH}")
        shutil.copy2(rules_path, RULES_DEST_PATH)

        decky_plugin.logger.info("Setting file ownership")
        os.system(f"chown 1000:1000 -R {SCRIPT_INSTALL_DIR}")
        os.system(f"chown 1000:1000 -R {SCRIPT_INSTALL_DIR}")

        decky_plugin.logger.info("Reloading udevadm")
        os.system("udevadm control --reload")

        decky_plugin.logger.info("Cleaning up")
        shutil.rmtree(TMP_DIR)

        decky_plugin.logger.info("Successfully installed scawp's script!")
        return True


    def uninstall(self):
        decky_plugin.logger.info("Uninstalling scawp's script...")

        decky_plugin.logger.info(f"Removing {SCRIPT_INSTALL_DIR}")
        Plugin._remove_path(SCRIPT_INSTALL_DIR)

        decky_plugin.logger.info(f"Removing {RULES_DEST_PATH}")
        Plugin._remove_path(RULES_DEST_PATH)

        decky_plugin.logger.info("Reloading udevadm")
        os.system("udevadm control --reload")

        decky_plugin.logger.info("Successfully uninstalled scawp's script!")


    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        global initialized;
        if initialized:
            return

        initialized = True

        decky_plugin.logger.info("Hello World!")
        Plugin.install()

    # Function called first during the unload process, utilize this to handle your plugin being removed
    async def _unload(self):
        decky_plugin.logger.info("Goodbye World!")
        Plugin.uninstall(self)

    async def disable(self):
        global enabled
        decky_plugin.logger.info("Disabling scawp's script...")
        # Create disabled file
        with open(DISABLED_PATH, "w") as file:
            os.system(f"chown 1000:1000 {DISABLED_PATH}")
            pass

        enabled = False
        decky_plugin.logger.info("Disabled scawp's script")

    async def enable(self):
        global enabled
        decky_plugin.logger.info("Enabling scawp's script...")
        Plugin._remove_path(DISABLED_PATH)
        enabled = True
        decky_plugin.logger.info("Enabled scawp's script")

    # Migrations that should be performed before entering `_main()`.
    async def _migration(self):
        decky_plugin.logger.info("Migrating")
        
