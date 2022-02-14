# Futsal parser

Futsal parser is a Python scripts for getting data from [AMFR](https://amfr.ru) and [LNFS](http://www.lnfs.es) leagues to count fantasy points.

## Installation

Use the Git to download futsal code.

```bash
git clone https://github.com/khwabscript/futsal-parser
cd futsal-parser
```

And then install dependencies using pip
```bash
pip install -r requirements.txt
```

## Usage
Get AMFR data

(If you do it first time during the season, it can take a long time - monitor the progress in superliga folder)


```python
python src/get-amfr-player-events.py
```

Get LNFS data

```python
python src/get-lnfs-player-evetns.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.