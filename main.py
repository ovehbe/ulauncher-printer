import subprocess
from ulauncher.api.client.EventListener import KeywordQueryEventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.item.ResultItem import ResultItem

class PrinterExtension(Extension):
    def __init__(self):
        super(PrinterExtension, self).__init__()
        self.subscribe(KeywordQueryEventListener(), KeywordQueryEventListener)

class KeywordQueryEventListener(KeywordQueryEventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        printer_name = extension.preferences.get("printer_name")

        if not printer_name:
            return RenderResultListAction([
                ResultItem(
                    title="Printer not configured!",
                    subtitle="Set the printer name in the extension settings.",
                    on_enter=None
                )
            ])

        if query:
            return RenderResultListAction([
                ResultItem(
                    title=f"Send to printer: {query}",
                    subtitle=f"Printer: {printer_name}",
                    on_enter=ExtensionCustomAction({"printer": printer_name, "text": query})
                )
            ])

        return RenderResultListAction([
            ResultItem(
                title="No text provided!",
                subtitle="Type the text to print after the keyword.",
                on_enter=None
            )
        ])

    def on_custom_action(self, data, extension):
        printer = data.get("printer")
        text = data.get("text")

        try:
            subprocess.run(["lp", "-d", printer, "-o", "raw"], input=text.encode("utf-8"), check=True)
            return RenderResultListAction([
                ResultItem(
                    title="Printed successfully!",
                    subtitle=f"Text: {text}",
                    on_enter=None
                )
            ])
        except Exception as e:
            return RenderResultListAction([
                ResultItem(
                    title="Failed to print!",
                    subtitle=f"Error: {str(e)}",
                    on_enter=None
                )
            ])

if __name__ == "__main__":
    PrinterExtension().run()

