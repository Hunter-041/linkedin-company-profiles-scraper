import csv
import json
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pandas as pd
from dicttoxml import dicttoxml

logger = logging.getLogger(__name__)

class Exporter:
    @staticmethod
    def _ensure_parent(path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def export_json(records: List[Dict[str, Any]], path: Path) -> None:
        Exporter._ensure_parent(path)
        with path.open("w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        logger.info("JSON exported to %s", path)

    @staticmethod
    def export_csv(records: List[Dict[str, Any]], path: Path) -> None:
        Exporter._ensure_parent(path)
        if not records:
            # still create an empty file with headers
            with path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([])  # empty header
            logger.info("Empty CSV exported to %s (no records).", path)
            return

        df = pd.DataFrame.from_records(records)
        df.to_csv(path, index=False)
        logger.info("CSV exported to %s", path)

    @staticmethod
    def export_xml(records: List[Dict[str, Any]], path: Path) -> None:
        Exporter._ensure_parent(path)
        # dicttoxml returns bytes
        xml_bytes = dicttoxml(
            records,
            custom_root="companies",
            item_name="company",
            attr_type=False,
        )
        with path.open("wb") as f:
            f.write(xml_bytes)
        logger.info("XML exported to %s", path)

    @staticmethod
    def export_excel(records: List[Dict[str, Any]], path: Path) -> None:
        Exporter._ensure_parent(path)
        df = pd.DataFrame.from_records(records)
        df.to_excel(path, index=False)
        logger.info("Excel exported to %s", path)

    @staticmethod
    def export_all(
        records: Iterable[Dict[str, Any]],
        output_prefix: Path,
        formats: List[str],
    ) -> None:
        records_list = list(records)
        formats = [f.lower().strip() for f in formats]

        for fmt in formats:
            if fmt == "json":
                Exporter.export_json(records_list, output_prefix.with_suffix(".json"))
            elif fmt == "csv":
                Exporter.export_csv(records_list, output_prefix.with_suffix(".csv"))
            elif fmt in ("xml", "xml2"):
                Exporter.export_xml(records_list, output_prefix.with_suffix(".xml"))
            elif fmt in ("xlsx", "excel"):
                Exporter.export_excel(records_list, output_prefix.with_suffix(".xlsx"))
            else:
                logger.warning("Unknown export format '%s' requested. Skipping.", fmt)