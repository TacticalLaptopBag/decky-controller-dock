import os

# The decky plugin module is located at decky-loader/plugin
# For easy intellisense checkout the decky-loader code one directory up
# or add the `decky-loader/plugin` path to `python.analysis.extraPaths` in `.vscode/settings.json`
import decky_plugin


class Plugin:
    # Asyncio-compatible long-running code, executed in a task when the plugin is loaded
    async def _main(self):
        decky_plugin.logger.info("Hello World!")
        rules_dest_dir = "/etc/udev/rules.d"
        plugin_path = os.path.dirname(os.path.realpath(__file__))
        script_path = os.path.join(plugin_path, "Steam-Deck.Auto-Disable-Steam-Controller", "disable_steam_input.sh")
        decky_plugin.logger.info(f"Determined plugin_path to be {plugin_path}")

        controller_rules = os.path.join(rules_dest_dir, "99-disable-steam-input_controller.rules")
        with open(controller_rules, "w") as rules_file:
            # echo 'KERNEL=="input*", SUBSYSTEM=="input", ENV{ID_INPUT_JOYSTICK}=="1", ACTION=="add", RUN+="/home/deck/.local/share/scawp/SDADSC/disable_steam_input.sh disable %k %E{NAME} %E{UNIQ} %E{PRODUCT}"' | sudo tee -a "$rules_install_dir/99-disable-steam-input.rules"
            # echo 'KERNEL=="input*", SUBSYSTEM=="input", ENV{ID_INPUT_JOYSTICK}=="1", ACTION=="remove", RUN+="/home/deck/.local/share/scawp/SDADSC/disable_steam_input.sh enable %k %E{NAME} %E{UNIQ} %E{PRODUCT}"' | sudo tee -a "$rules_install_dir/99-disable-steam-input.rules"
            rules_file.write('KERNEL=="input*", SUBSYSTEM=="input", ENV{ID_INPUT_JOYSTICK}=="1", ACTION=="add", RUN+="\''+script_path+'\' disable %k %E{NAME} %E{UNIQ} %E{PRODUCT}"')
            rules_file.write("\n")
            rules_file.write('KERNEL=="input*", SUBSYSTEM=="input", ENV{ID_INPUT_JOYSTICK}=="1", ACTION=="remove", RUN+="\''+script_path+'\' enable %k %E{NAME} %E{UNIQ} %E{PRODUCT}"')
            rules_file.write("\n")
        decky_plugin.logger.info(f"Wrote steam input controller rules to {controller_rules}")

        os.system("udevadm control --reload")
        decky_plugin.logger.info("Reloaded services")

        os.chmod(script_path, 0o555)
        decky_plugin.logger.info("Set permissions on scawp's script")


    # Function called first during the unload process, utilize this to handle your plugin being removed
    async def _unload(self):
        decky_plugin.logger.info("Goodbye World!")
        pass

    # Migrations that should be performed before entering `_main()`.
    async def _migration(self):
        decky_plugin.logger.info("Migrating")
        # Here's a migration example for logs:
        # - `~/.config/decky-template/template.log` will be migrated to `decky_plugin.DECKY_PLUGIN_LOG_DIR/template.log`
        # decky_plugin.migrate_logs(os.path.join(decky_plugin.DECKY_USER_HOME,
        #                                        ".config", "decky-controller-dock", "template.log"))
        # Here's a migration example for settings:
        # - `~/homebrew/settings/template.json` is migrated to `decky_plugin.DECKY_PLUGIN_SETTINGS_DIR/template.json`
        # - `~/.config/decky-template/` all files and directories under this root are migrated to `decky_plugin.DECKY_PLUGIN_SETTINGS_DIR/`
        # decky_plugin.migrate_settings(
        #     os.path.join(decky_plugin.DECKY_HOME, "settings", "template.json"),
        #     os.path.join(decky_plugin.DECKY_USER_HOME, ".config", "decky-controller-dock"))
        # Here's a migration example for runtime data:
        # - `~/homebrew/template/` all files and directories under this root are migrated to `decky_plugin.DECKY_PLUGIN_RUNTIME_DIR/`
        # - `~/.local/share/decky-template/` all files and directories under this root are migrated to `decky_plugin.DECKY_PLUGIN_RUNTIME_DIR/`
        # decky_plugin.migrate_runtime(
        #     os.path.join(decky_plugin.DECKY_HOME, "template"),
        #     os.path.join(decky_plugin.DECKY_USER_HOME, ".local", "share", "decky-controller-dock"))
