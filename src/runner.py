import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure src directory is on sys.path so namespace packages resolve
CURRENT_FILE = Path(__file__).resolve()
SRC_DIR = CURRENT_FILE.parent
REPO_ROOT = SRC_DIR.parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from extractors.linkedin_parser import LinkedInCompanyScraper  # type: ignore  # noqa: E402
from outputs.exporters import Exporter  # type: ignore  # noqa: E402

def setup_logging(verbosity: int) -> None:
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

def load_settings(config_path: Optional[str]) -> Dict[str, Any]:
    if config_path:
        path = Path(config_path)
    else:
        path = SRC_DIR / "config" / "settings.example.json"

    if not path.is_file():
        logging.warning("Settings file not found at %s, using in-code defaults.", path)
        return {}

    try:
        with path.open("r", encoding="utf-8") as f:
            settings = json.load(f)
        logging.info("Loaded settings from %s", path)
        return settings
    except json.JSONDecodeError as exc:
        logging.error("Failed to parse settings file %s: %s", path, exc)
        return {}

def load_input(input_path: str) -> Dict[str, Any]:
    path = Path(input_path)
    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: {path}")

    try:
        text = path.read_text(encoding="utf-8")
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("Input JSON must be an object at top level.")
        return data
    except json.JSONDecodeError as exc:
        raise ValueError(f"Input file is not valid JSON: {exc}") from exc

def resolve_output_formats(
    input_data: Dict[str, Any],
    settings: Dict[str, Any],
    cli_formats: Optional[List[str]],
) -> List[str]:
    if cli_formats:
        return [f.lower() for f in cli_formats]

    if "output_formats" in input_data and isinstance(input_data["output_formats"], list):
        return [str(f).lower() for f in input_data["output_formats"]]

    output_cfg = settings.get("output", {})
    if isinstance(output_cfg, dict):
        formats = output_cfg.get("formats")
        if isinstance(formats, list):
            return [str(f).lower() for f in formats]

    # Fallback default
    return ["json", "csv"]

def resolve_output_prefix(
    cli_output_prefix: Optional[str],
    settings: Dict[str, Any],
) -> Path:
    if cli_output_prefix:
        return Path(cli_output_prefix)

    output_cfg = settings.get("output", {})
    directory = None
    if isinstance(output_cfg, dict):
        directory = output_cfg.get("directory")

    if directory:
        return REPO_ROOT / str(directory) / "linkedin_companies"

    return REPO_ROOT / "data" / "linkedin_companies"

def build_scraper(settings: Dict[str, Any]) -> LinkedInCompanyScraper:
    timeout = int(settings.get("request_timeout", 15))
    max_retries = int(settings.get("max_retries", 3))
    backoff_factor = float(settings.get("backoff_factor", 1.5))
    user_agent = str(
        settings.get(
            "user_agent",
            (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            ),
        )
    )

    proxy_groups = settings.get("proxy_groups", {})
    if not isinstance(proxy_groups, dict):
        proxy_groups = {}

    return LinkedInCompanyScraper(
        timeout=timeout,
        max_retries=max_retries,
        backoff_factor=backoff_factor,
        user_agent=user_agent,
        proxy_groups=proxy_groups,
    )

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="LinkedIn Company Profiles Scraper runner.",
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Path to input JSON file containing 'company_profile_urls'.",
    )
    parser.add_argument(
        "--config",
        "-c",
        required=False,
        help="Path to settings JSON file. Defaults to src/config/settings.example.json.",
    )
    parser.add_argument(
        "--output-prefix",
        "-o",
        required=False,
        help=(
            "Output file prefix without extension. "
            "If omitted, uses directory/formats from settings."
        ),
    )
    parser.add_argument(
        "--format",
        "-f",
        required=False,
        action="append",
        dest="formats",
        help="Output format to generate (json, csv, xml, excel). May be used multiple times.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="Increase log verbosity (can be used multiple times).",
    )
    return parser.parse_args(argv)

def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    setup_logging(args.verbose)

    try:
        input_data = load_input(args.input)
    except (FileNotFoundError, ValueError) as exc:
        logging.error("Failed to load input: %s", exc)
        return 1

    settings = load_settings(args.config)
    scraper = build_scraper(settings)

    urls = input_data.get("company_profile_urls") or input_data.get("urls")
    if not isinstance(urls, list) or not urls:
        logging.error(
            "Input must contain non-empty 'company_profile_urls' or 'urls' list."
        )
        return 1

    urls = [str(u).strip() for u in urls if str(u).strip()]
    if not urls:
        logging.error("No valid LinkedIn URLs found in input after cleaning.")
        return 1

    proxy_group = input_data.get("proxy_group")
    if proxy_group is not None:
        proxy_group = str(proxy_group).strip() or None

    logging.info("Starting scrape for %d companies.", len(urls))

    companies = scraper.scrape_profiles(urls, proxy_group=proxy_group)
    logging.info("Scraping finished with %d results.", len(companies))

    # Decide outputs
    formats = resolve_output_formats(input_data, settings, args.formats)
    output_prefix = resolve_output_prefix(args.output_prefix, settings)

    logging.info(
        "Exporting data to formats %s with prefix %s",
        formats,
        output_prefix,
    )

    Exporter.export_all(companies, output_prefix, formats=formats)

    logging.info("All done.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())