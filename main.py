#!/usr/bin/env python3
import subprocess
import logging

from ulauncher.api.client.EventListener import KeywordQueryEventListener, KeywordEnterEventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

LOG = logging.getLogger(__name__)

class PrintExtension(Extension):
    def __init__(self):
        super(PrintExtension, self).__init__()
        self.subscribe(KeywordQueryEventListener, KeywordQueryListener())
        self.subscribe(KeywordEnterEventListener, KeywordEnterListener())

class KeywordQueryListener(KeywordQueryEventListener):
    def on_event(self, event, extension):
        """
        Called when user types the extension's keyword + text in Ulauncher.
        """
        query = event.get_argument() or ""
        LOG.debug(f"User typed: {query}")

        return [
            ExtensionResultItem(
                icon='images/icon.png',
                name=f"Print: {query}",
                description="Press Enter to print the above text",
                on_enter=ExtensionCustomAction(
                    {"text_to_print": query}, 
                    keep_app_open=False
                ),
            )
        ]

class KeywordEnterListener(KeywordEnterEventListener):
    def on_event(self, event, extension):
        """
        Called when user presses Enter on the displayed result.
        """
        data = event.get_data() or {}
        text_to_print = data.get("text_to_print", "")
        
        # Get printer name from extension preferences
        printer = extension.preferences.get("printer", "")

        if not text_to_print.strip():
            LOG.warning("No text to print. Doing nothing.")
            return

        LOG.info(f"Printing '{text_to_print}' to printer: '{printer or 'default'}'")

        try:
            # If printer is specified, use 'lp -d <printer>'; else just 'lp'
            if printer.strip():
                subprocess.run(["lp", "-d", printer], input=text_to_print.encode("utf-8"), check=True)
            else:
                subprocess.run(["lp"], input=text_to_print.encode("utf-8"), check=True)

        except Exception as e:
            LOG.error(f"Printing failed: {e}")

if __name__ == "__main__":
    PrintExtension().run()

