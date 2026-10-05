# ad1-extractor-cli

CLI tool to extract AccessData (`.ad1`) forensic images.

## Installation

```bash
git clone [https://github.com/anir0y/ad1-viewer.git](https://github.com/anir0y/ad1-viewer.git)
cd ad1-viewer
git clone [https://github.com/](https://github.com/)<YOUR_USERNAME>/ad1-extractor-cli.git
cp ad1-extractor-cli/dump.py .
chmod +x dump.py
```

## Usage

```bash
python3 dump.py <path_to_evidence.ad1> <output_directory>
```

### Example

```bash
python3 dump.py ~/Desktop/Evidence.ad1 ~/Desktop/extracted_evidence
```
