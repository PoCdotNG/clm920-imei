# CLM920 Modem IMEI Repair Tool

## Overview

This python script is designed to modify the IMEI of a CLM920 LTE router. It performs tasks such as logging into the router, retrieving device information, and setting a new IMEI.
Rapidly developed, to be considered as a working proof of concept.

**Warning:** Altering a device's IMEI is illegal in certain jurisdictions. Use this tool responsibly and in compliance with local laws.

## Requirements

- Python 3.x
- Dependencies: Install them using `pip install -r requirements.txt`
    - `requests`
    - `stdnum`

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/clm920-imei-repair.git
    cd clm920-imei-repair
    ```

2. Install the required Python packages:

    ```bash
    pip install requests stdnum
    ```

## Usage

### Command-line Arguments

- `--ip`: (Required) The IP address of the CLM920 router (e.g., `192.168.0.1`).
- `--password`: (Required) The admin password for the router.
- `--imei`: (Required) The new IMEI to set (e.g., `335841028069386`).

### Example Command

```bash
python clm920.py --ip 192.168.0.1 --password admin --imei 335841028069386

```

## License : GPLv3

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Contributing?

Feel free to create an MR or send feedback by github issues.


