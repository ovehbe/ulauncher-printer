import subprocess
import logging

from ulauncher.api.client.EventListener import KeywordQueryEventListener, KeywordEnterEventListener
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.client.Extension import Extension

LOG = logging.getLogger(__name__)

class PrintExtension(Extension):
    def __init__(self):
        super(PrintExtension, self).__init__()
        self.subscribe(KeywordQueryEventListener, KeywordQueryEventListenerImpl())
        self.subscribe(KeywordEnterEventListener, KeywordEnterEventListenerImpl())

class KeywordQueryEventListenerImpl(KeywordQueryEventListener):
    def on_event(self, event, extension):
        """
        Called when the user types the extension keyword in Ulauncher.
        """
        query = event.get_argument() or ""
        LOG.debug(f"User typed query: {query}")

        # We want to show a single item that, when pressed, will trigger printing
        # We'll pass the query text along in an ExtensionCustomAction
        return [
            ExtensionResultItem(
                icon='images/icon.png',
                name=f"Print: {query}",
                description="Press Enter to print the above text to the specified printer.",
                on_enter=ExtensionCustomAction(
                    {
                        'text_to_print': query
                    },
                    keep_app_open=False
                )
            )
        ]


class KeywordEnterEventListenerImpl(KeywordEnterEventListener):
    def on_event(self, event, extension):
        """
        Called when the user presses Enter on a result item.
        """
        data = event.get_data()
        text_to_print = data.get('text_to_print', '')

        # Retrieve user-specified printer from preferences
        printer_name = extension.preferences.get('printer')

        LOG.info(f"Printing: {text_to_print} to printer: {printer_name}")

        if not text_to_print.strip():
            LOG.warning("No text provided to print.")
            return

        try:
            # If printer_name is empty, 'lp' will use the default printer.
            if printer_name:
                subprocess.run(
                    ["lp", "-d", printer_name],
                    input=text_to_print.encode('utf-8'),
                    check=True
                )
            else:
                subprocess.run(
                    ["lp"],
                    input=text_to_print.encode('utf-8'),
                    check=True
                )

        except Exception as e:
            LOG.error(f"Failed to print. Error: {e}")

if __name__ == '__main__':
    PrintExtension().run()

