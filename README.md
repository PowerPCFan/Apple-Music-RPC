<h1 align="center">Apple-Music-RPC</h1>

<p align="center">A simple Rich Presence client for Apple Music on Windows.</p>

> [!NOTE]
> This script only works with iTunes from Apple.com - not iTunes from the Microsoft Store or Apple Music from the Microsoft Store.
>
> **You can download the latest 64-bit iTunes version from Apple [here](https://www.apple.com/itunes/download/win64).**

# Running the script
## Prerequisites and Initial Setup (*You only need to do this once*)
### Prerequisites
- Install `git` if not already installed
- Install a recent version of `Python`, like version `3.11`, `3.12`, or `3.13`. Versions older than `3.11` will likely cause issues.
### Initial Setup
- Clone the repository (`git clone https://github.com/PowerPCFan/Apple-Music-RPC.git` on Windows/Linux/macOS)
- `cd` into the script dir (`cd Apple-Music-RPC` on Windows/Linux/macOS)
- Create a virtual environment (`py -m venv venv` on Windows, `python3 -m venv venv` on Linux/macOS)
- Enter the virtual environment (`venv\Scripts\activate` on Windows, `source venv/bin/activate` on Linux/macOS)
- Install requirements (`pip install -r requirements.txt` on Windows/Linux/macOS)

## Execution
- `cd` into the script dir (`cd Apple-Music-RPC` on Windows/Linux/macOS)
- Enter the virtual environment (`venv\Scripts\activate` on Windows, `source venv/bin/activate` on Linux/macOS)
- `cd` the `app` directory (`cd app` on Windows/Linux/macOS)
- Run the script (`py main.py` on Windows, `python3 main.py` on Linux/macOS)