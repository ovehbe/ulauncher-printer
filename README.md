# Simple Print Extension for Ulauncher

A minimal Ulauncher extension that prints text to a specified printer using the `lp` command.

## How It Works

1. Set the extension keyword (default `p`) in your Ulauncher preferences.
2. Set your desired printer name (default is empty, meaning system default printer).
3. Type your keyword followed by the text you want to print.
4. Press Enter to send the text to your specified (or default) printer.

## Requirements

- `lp` command available (usually part of [CUPS](https://www.cups.org/)).
- Python 3 (as required by Ulauncher).

## Installation

1. Copy or clone this repo into your local Ulauncher extensions folder:
   - `~/.config/ulauncher/extensions/` (on most Linux systems).
2. Restart Ulauncher or reload extensions.
3. Configure the extension in Ulauncher preferences:
   - **Keyword**: The keyword to trigger the extension (e.g. `p`).
   - **Printer Name**: The name of the printer. Leave empty for the default printer.

## Usage

1. Open Ulauncher (default `Ctrl + Space`).
2. Type your keyword (e.g. `p`), then type the text you want to print.  
   Example: `p Hello, World!`
3. Press Enter. The text is piped to `lp`.

## License

See [LICENSE](LICENSE) for details.

