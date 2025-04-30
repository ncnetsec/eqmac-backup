import plistlib
import base64
import json
import csv
import sys
import os
import re
import math
from pathlib import Path

def read_plist_file(plist_path):
    """Read the plist file and return the expertEqualizerPresets data."""
    try:
        with open(plist_path, 'rb') as f:
            plist_data = plistlib.load(f)
        return plist_data.get('expertEqualizerPresets')
    except Exception as e:
        print(f"Error reading plist file: {e}")
        sys.exit(1)

def is_base64(s):
    """Check if a string is likely base64-encoded."""
    if not isinstance(s, str):
        return False
    base64_pattern = r'^[A-Za-z0-9+/=]+$'
    return bool(re.match(base64_pattern, s)) and len(s) % 4 == 0

def decode_data(data):
    """Decode or parse the expertEqualizerPresets data."""
    try:
        print(f"Raw data type: {type(data)}")
        print(f"Raw data (first 100 chars): {str(data)[:100]}... (length: {len(str(data))})")
        
        if isinstance(data, list):
            print("Data is already a parsed JSON list.")
            return data
        
        if isinstance(data, bytes):
            data = data.decode('utf-8', errors='ignore')
        
        if is_base64(data):
            print("Attempting base64 decode...")
            decoded = base64.b64decode(data)
            decoded_str = decoded.decode('utf-8')
            print(f"Decoded data (first 100 chars): {decoded_str[:100]}")
            return json.loads(decoded_str)
        
        print("Attempting direct JSON parse...")
        return json.loads(data)
        
    except Exception as e:
        print(f"Error decoding or parsing data: {e}")
        sys.exit(1)

def bandwidth_to_q(bandwidth):
    """Convert bandwidth (in octaves) to Q factor."""
    try:
        bw = float(bandwidth)
        if bw <= 0:
            return 1.0  # Default Q if bandwidth is invalid
        # Q = sqrt(2^BW) / (2^BW - 1/(2^BW))
        term = 2 ** bw
        q = math.sqrt(term) / (term - 1 / term)
        return round(q, 2)
    except (ValueError, ZeroDivisionError):
        return 1.0

def get_filter_type(type_id):
    """Map filter type ID to eqMac type string."""
    type_map = {
        0: 'PK',  # Peaking filter
        9: 'LS',  # Low-shelf
        10: 'HS'  # High-shelf
    }
    return type_map.get(type_id, 'PK')  # Default to PK if unknown

def sanitize_filename(name):
    """Sanitize preset name for use as a filename."""
    # Replace invalid characters with underscore
    return re.sub(r'[<>:"/\\|?*]', '_', name.strip())

def write_text_files(presets, output_dir):
    """Write a text file for each preset in eqMac format."""
    try:
        for preset in presets:
            preset_name = preset.get('name', 'Unnamed')
            filename = f"{sanitize_filename(preset_name)}.txt"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                # Write Preamp line
                global_val = float(preset.get('global', 0))
                f.write(f"Preamp: {global_val:.2f} dB\n")
                
                # Write Filter lines
                for i, band in enumerate(preset.get('bands', []), 1):
                    frequency = float(band.get('frequency', 0))
                    gain = float(band.get('gain', 0))
                    bandwidth = float(band.get('bandwidth', 0))
                    type_id = band.get('type', 0)
                    bypass = band.get('bypass', False)
                    
                    state = 'OFF' if bypass else 'ON'
                    filter_type = get_filter_type(type_id)
                    q = bandwidth_to_q(bandwidth)
                    
                    f.write(f"Filter {i}: {state} {filter_type} Fc {frequency} Hz Gain {gain:.2f} dB Q {q}\n")
            
            print(f"Wrote text file: {filepath}")
    except Exception as e:
        print(f"Error writing text files: {e}")
        sys.exit(1)

def write_to_csv(presets, output_file):
    """Write the presets data to a CSV file."""
    try:
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            header = ['Preset_ID', 'Preset_Name', 'Global', 'IsDefault', 'Band_Frequency', 'Band_Gain', 'Band_Bandwidth', 'Band_Type', 'Band_Bypass']
            writer.writerow(header)
            
            for preset in presets:
                preset_id = preset.get('id', '')
                preset_name = preset.get('name', '')
                global_val = preset.get('global', 0)
                is_default = preset.get('isDefault', False)
                
                for band in preset.get('bands', []):
                    row = [
                        preset_id,
                        preset_name,
                        global_val,
                        is_default,
                        band.get('frequency', 0),
                        band.get('gain', 0),
                        band.get('bandwidth', 0),
                        band.get('type', 0),
                        band.get('bypass', False)
                    ]
                    writer.writerow(row)
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python eqmac_plist_to_csv.py <output_csv_file>")
        sys.exit(1)
    
    output_file = sys.argv[1]
    output_dir = os.path.dirname(output_file) or '.'
    
    plist_path = Path.home() / 'Library' / 'Preferences' / 'com.bitgapp.eqmac.plist'
    
    if not os.path.exists(plist_path):
        print(f"Plist file not found at: {plist_path}")
        sys.exit(1)
    
    presets_data = read_plist_file(plist_path)
    if not presets_data:
        print("No expertEqualizerPresets found in plist file.")
        sys.exit(1)
    
    presets = decode_data(presets_data)
    
    write_to_csv(presets, output_file)
    print(f"Successfully wrote CSV to {output_file}")
    
    write_text_files(presets, output_dir)
    print("Finished writing text files for all presets")

if __name__ == "__main__":
    main()