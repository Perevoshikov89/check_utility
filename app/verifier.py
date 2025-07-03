from pathlib import Path
import xml.etree.ElementTree as ET


def remove_signature(xml_path: Path, output_dir: Path) -> Path:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for elem in root.findall(".//{*}Signature"):
        parent = root.find(".//{*}Signature/..")
        if parent is not None:
            parent.remove(elem)

    clean_path = output_dir / (xml_path.stem + "_clean.xml")
    tree.write(clean_path, encoding="utf-8", xml_declaration=True)
    return clean_path
