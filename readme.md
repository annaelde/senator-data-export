# Senator Data Export

This script requests an XML document from senate.gov containing contact information for all current US Senators. It then parses the XML data and exports it to the following JSON format:

```
[
    {
        "firstName": "Marco",
        "lastName": "Rubio",
        "fullName": "Marco Rubio",
        "chartId": "R000595",
        "mobile": "(202) 224-3041",
        "address": [{ "postal": 20510, "state": "DC", "city": "Washington", "street": "284 Russell Senate Office Building" }]
    },
]
```

There's a single dependency, [uszipcode](https://uszipcode.readthedocs.io/?badge=latest), used to parse the address information accurately.

## Setup

### Requirements
- Python 3.6+

### Windows
Set up Python env
```
python3.6 -m venv ./env
./env/scripts/Activate.ps1
```
Install dependencies
```
pip install -r ./requirements.pip
```
Run script
```
python main.py
```

### Mac/Linux
Set up Python env
```
python3.6 -m venv ./env/py
source ./env/py/bin/activate
```
Install dependencies
```
pip install -r ./requirements.pip
```
Run script
```
python main.py
```