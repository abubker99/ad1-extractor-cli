#!/usr/bin/env python3
import os
import sys
from ad1.parser import AD1

def sanitize_path(raw_path):
    # Convert Windows backslashes to forward slashes
    p = raw_path.replace("\\", "/")
    # Split into parts and clean each segment
    parts = [part for part in p.split("/") if part and part != "."]
    # Filter out empty or root-level markers
    clean_parts = []
    for part in parts:
        if part in ("[root]",):
            continue
        # Remove trailing colon if it is a drive letter (e.g., "C:")
        if len(part) == 2 and part[1] == ":":
            part = part[0]
        clean_parts.append(part)
    return os.path.join(*clean_parts) if clean_parts else ""

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 dump.py <image.ad1> <output_directory>")
        sys.exit(1)

    image_path = sys.argv[1]
    out_dir = os.path.abspath(sys.argv[2])
    os.makedirs(out_dir, exist_ok=True)

    print(f"[*] Loading AD1 image: {image_path}")
    img = AD1(image_path)

    extracted_count = 0
    failed_count = 0

    def extract_node(node):
        nonlocal extracted_count, failed_count

        rel_path = sanitize_path(node.path)
        dest_path = os.path.join(out_dir, rel_path)

        if node.is_dir or hasattr(node, "children") and len(node.children) > 0:
            os.makedirs(dest_path, exist_ok=True)
            for child in node.children:
                extract_node(child)
        else:
            if os.path.isdir(dest_path):
                # Avoid attempting to overwrite an already created directory
                return

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            if node.size == 0:
                try:
                    open(dest_path, "wb").close()
                except OSError:
                    pass
                return

            try:
                data = img.read_file(node)
                with open(dest_path, "wb") as f:
                    f.write(data)
                extracted_count += 1
                if extracted_count % 50 == 0:
                    print(f"[*] Extracted {extracted_count} files...", end="\r")
            except Exception as e:
                failed_count += 1
                print(f"\n[-] Failed to extract {node.path}: {e}")

    print("[*] Extracting files...")
    extract_node(img.root)
    print(f"\n[+] Complete! Extracted: {extracted_count} files (Failed: {failed_count})")
    print(f"[+] Output stored in: {out_dir}")

if __name__ == "__main__":
    main()
