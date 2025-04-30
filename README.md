# eqMac Equalizer Settings Backup

This Python script extracts equalizer settings from the eqMac application on macOS, converts them into a human-readable CSV file, and generates individual text files for each preset in a format compatible with eqMac's text rendering. This allows users to back up their expert equalizer presets and restore them easily.

## Features

- Reads the `expertEqualizerPresets` data from `~/Library/Preferences/com.bitgapp.eqmac.plist`.
- Supports both base64-encoded and raw JSON data formats.
- Outputs a comprehensive CSV file with all preset details (ID, name, global preamp, bands).
- Generates a text file for each preset in eqMac's native format, suitable for copying and pasting back into eqMac.
- Converts bandwidth to Q-factor for accurate filter representation.
- Sanitizes preset names for safe file naming.

## Requirements

- **Python 3.6+** (standard library modules only: `plistlib`, `base64`, `json`, `csv`, `sys`, `os`, `re`, `math`, `pathlib`).
- **macOS** with eqMac installed.
- The eqMac plist file at `~/Library/Preferences/com.bitgapp.eqmac.plist`.

## Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/your-username/eqmac-backup.git
   cd eqmac-backup
   ```

2. Ensure Python 3 is installed:
   ```bash
   python3 --version
   ```

## Usage

Run the script with a single command-line argument specifying the output CSV file path. The script will generate the CSV and individual preset text files in the same directory.

```bash
python3 eqmac_plist_to_csv.py <output_csv_file>
```

**Example**:
```bash
python3 eqmac_plist_to_csv.py ~/Downloads/eqmac_presets.csv
```

This will:
- Create `~/Downloads/eqmac_presets.csv` with all preset data.
- Generate text files (e.g., `Test-10.txt`, `Test-31.txt`) in `~/Downloads/` for each preset.

### Output Files

- **CSV File** (`eqmac_presets.csv`):
  - Columns: `Preset_ID`, `Preset_Name`, `Global`, `IsDefault`, `Band_Frequency`, `Band_Gain`, `Band_Bandwidth`, `Band_Type`, `Band_Bypass`.
  - Each row represents a band within a preset.

- **Text Files** (e.g., `Test-10.txt`):
  - Format compatible with eqMac's text rendering:
    ```
    Preamp: -2.66 dB
    Filter 1: ON PK Fc 32 Hz Gain 5.49 dB Q 1.41
    Filter 2: ON PK Fc 64 Hz Gain -2.60 dB Q 1.41
    ...
    ```
  - One file per preset, named after the preset name (sanitized for safe file naming).

## Notes

- **Q-Factor Calculation**: Bandwidth (in octaves) is converted to Q using the formula:
  \[
  Q = \frac{\sqrt{2^{BW}}}{\sqrt{2^{BW}} - \frac{1}{\sqrt{2^{BW}}}}
  \]
  For example, a bandwidth of 1.0 yields \( Q \approx 1.41 \).

- **Filter Types**: The script maps filter types as follows:
  - `0`: Peaking (PK)
  - `9`: Low-shelf (LS)
  - `10`: High-shelf (HS)

- **Error Handling**: The script includes robust error handling for missing files, invalid data formats, and decoding issues.

- **Backup Warning**: Before modifying the eqMac plist file, back it up to avoid accidental data loss:
  ```bash
  cp ~/Library/Preferences/com.bitgapp.eqmac.plist ~/Library/Preferences/com.bitgapp.eqmac.plist.bak
  ```

## Troubleshooting

- **Plist File Not Found**:
  Ensure eqMac is installed and has generated the plist file at `~/Library/Preferences/com.bitgapp.eqmac.plist`.

- **Data Format Issues**:
  The script supports both base64-encoded and raw JSON `expertEqualizerPresets` data. If errors occur, inspect the plist file:
  ```bash
  plutil -p ~/Library/Preferences/com.bitgapp.eqmac.plist
  ```

- **Q or Filter Type Mismatches**:
  If Q values or filter types don't match eqMac's UI, verify the bandwidth and type IDs in the plist data. Contact the maintainer with details.

## Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the APACHE 2.0 License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with assistance from Grok, created by xAI.
- Inspired by the need to back up eqMac equalizer settings for easy restoration.
