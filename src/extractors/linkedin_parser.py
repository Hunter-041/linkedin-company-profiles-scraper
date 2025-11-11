import json
import logging
import random
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from .utils_cleaner import clean_text, safe_int, safe_str, extract_year

logger = logging.getLogger(__name__)

@dataclass
class LinkedInCompanyScraper:
    """
    Lightweight LinkedIn company scraper.

    This implementation works with *public* company pages and is designed
    to be robust and fail-safe. If LinkedIn changes its markup or if
    network access is unavailable, it will simply return partial data
    rather than crash.
    """

    timeout: int = 15
    max_retries: int = 3
    backoff_factor: float = 1.5
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
    proxy_groups: Optional[Dict[str, Dict[str, str]]] = None

    def _get_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({"User-Agent": self.user_agent})
        return session

    def _resolve_proxies(self, proxy_group: Optional[str]) -> Optional[Dict[str, str]]:
        if not proxy_group or not self.proxy_groups:
            return None
        proxies = self.proxy_groups.get(proxy_group)
        if not proxies:
            logger.info("Proxy group '%s' not found in settings; continuing without.", proxy_group)
            return None
        logger.debug("Using proxy group '%s'.", proxy_group)
        return proxies

    def scrape_profiles(
        self,
        urls: List[str],
        proxy_group: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        if not urls:
            return []

        session = self._get_session()
        proxies = self._resolve_proxies(proxy_group)
        results: List[Dict[str, Any]] = []

        for idx, url in enumerate(urls, start=1):
            logger.info("Scraping %d/%d: %s", idx, len(urls), url)
            try:
                html = self._fetch_company_page(session, url, proxies)
                company = self._parse_company(html, url)
                results.append(company)
            except Exception as exc:  # noqa: BLE001
                logger.exception("Failed to scrape %s: %s", url, exc)
                # At least return a skeleton result so user sees what failed
                results.append(
                    {
                        "company_name": None,
                        "company_profile": url,
                        "error": safe_str(exc),
                    }
                )

        return results

    def _fetch_company_page(
        self,
        session: requests.Session,
        url: str,
        proxies: Optional[Dict[str, str]] = None,
    ) -> str:
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = session.get(url, timeout=self.timeout, proxies=proxies)
                if 200 <= response.status_code < 300:
                    return response.text
                logger.warning(
                    "Non-OK status %s when requesting %s (attempt %d/%d)",
                    response.status_code,
                    url,
                    attempt,
                    self.max_retries,
                )
            except requests.RequestException as exc:
                last_exc = exc
                logger.warning(
                    "RequestException when requesting %s (attempt %d/%d): %s",
                    url,
                    attempt,
                    self.max_retries,
                    exc,
                )
            # Backoff with small jitter
            sleep_for = self.backoff_factor * (2 ** (attempt - 1)) + random.uniform(0, 0.5)
            time.sleep(sleep_for)

        if last_exc:
            raise last_exc
        raise RuntimeError(f"Failed to fetch {url}")

    def _parse_company(self, html: str, url: str) -> Dict[str, Any]:
        """
        Parse a LinkedIn company page.

        The HTML structure on LinkedIn changes over time, and may differ
        by locale. This parser focuses on resilient patterns:
        - JSON-LD structured data in <script type="application/ld+json">
        - OpenGraph tags and meta tags
        - Fallback to <title> and heuristic extraction
        """
        soup = BeautifulSoup(html, "lxml")

        data = {
            "company_name": None,
            "company_profile": url,
            "company_website": None,
            "company_address_type": None,
            "company_street": None,
            "company_locality": None,
            "company_region": None,
            "company_postal_code": None,
            "company_country": None,
            "company_employees_on_linkedin": None,
            "company_followers_on_linkedin": None,
            "company_logo": None,
            "company_cover_image": None,
            "company_slogan": None,
            "company_twitter_description": None,
            "company_about_us": None,
            "company_industry": None,
            "company_size": None,
            "company_headquarters": None,
            "company_organization_type": None,
            "company_founded": None,
            "company_specialties": None,
        }

        # Try JSON-LD blocks first
        self._parse_from_json_ld(soup, data)
        # Fallbacks from meta tags and titles
        self._parse_from_meta_and_title(soup, data)

        return data

    def _parse_from_json_ld(self, soup: BeautifulSoup, target: Dict[str, Any]) -> None:
        scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        for script in scripts:
            try:
                txt = script.string or script.text
                if not txt:
                    continue
                parsed = json.loads(txt)
            except json.JSONDecodeError:
                continue

            if isinstance(parsed, list):
                for entry in parsed:
                    if isinstance(entry, dict):
                        self._apply_json_ld(entry, target)
            elif isinstance(parsed, dict):
                self._apply_json_ld(parsed, target)

    def _apply_json_ld(self, node: Dict[str, Any], target: Dict[str, Any]) -> None:
        node_type = safe_str(node.get("@type")).lower()
        if "organization" not in node_type and "corp" not in node_type and "company" not in node_type:
            return

        name = clean_text(node.get("name"))
        if name:
            target["company_name"] = name

        url = clean_text(node.get("url"))
        if url:
            target["company_website"] = url

        # Address may be an object or list
        address = node.get("address")
        if isinstance(address, list) and address:
            address = address[0]

        if isinstance(address, dict):
            target["company_address_type"] = clean_text(address.get("@type"))
            target["company_street"] = clean_text(address.get("streetAddress"))
            target["company_locality"] = clean_text(address.get("addressLocality"))
            target["company_region"] = clean_text(address.get("addressRegion"))
            target["company_postal_code"] = clean_text(address.get("postalCode"))
            target["company_country"] = clean_text(
                address.get("addressCountry")
                if isinstance(address.get("addressCountry"), str)
                else getattr(address.get("addressCountry"), "name", None)
            )

        description = clean_text(node.get("description"))
        if description and not target.get("company_about_us"):
            target["company_about_us"] = description

        # Employee count and followers are rarely in JSON-LD, but just in case:
        employees = node.get("numberOfEmployees") or node.get("employees")
        if employees and not target.get("company_employees_on_linkedin"):
            target["company_employees_on_linkedin"] = safe_int(employees)

        if not target.get("company_logo"):
            logo = node.get("logo")
            if isinstance(logo, dict):
                target["company_logo"] = clean_text(logo.get("url"))
            else:
                target["company_logo"] = clean_text(logo)

        if not target.get("company_industry"):
            industry = clean_text(node.get("industry"))
            if industry:
                target["company_industry"] = industry

        if not target.get("company_founded"):
            founded = extract_year(safe_str(node.get("foundingDate") or node.get("foundingYear")))
            if founded:
                target["company_founded"] = founded

        if not target.get("company_size"):
            employees_range = node.get("employeesRange") or node.get("employeeRange")
            if employees_range:
                target["company_size"] = clean_text(employees_range)

        if not target.get("company_headquarters"):
            hq = node.get("foundingLocation") or node.get("location")
            if isinstance(hq, dict):
                target["company_headquarters"] = clean_text(
                    hq.get("name") or hq.get("addressLocality") or hq.get("addressRegion")
                )
            elif isinstance(hq, str):
                target["company_headquarters"] = clean_text(hq)

        if not target.get("company_specialties"):
            specialties = node.get("knowsAbout") or node.get("specialty") or node.get("specialties")
            if isinstance(specialties, list):
                target["company_specialties"] = ", ".join(
                    [s for s in (clean_text(x) for x in specialties) if s]
                )
            elif isinstance(specialties, str):
                target["company_specialties"] = clean_text(specialties)

    def _parse_from_meta_and_title(self, soup: BeautifulSoup, target: Dict[str, Any]) -> None:
        # Title -> often "Company name | LinkedIn"
        if not target.get("company_name"):
            if soup.title and soup.title.string:
                title = clean_text(soup.title.string)
                if title:
                    # Strip trailing "| LinkedIn" or similar patterns
                    pieces = [p.strip() for p in title.split("|") if p.strip()]
                    if pieces:
                        target["company_name"] = pieces[0]

        # Description meta
        if not target.get("company_about_us"):
            desc = self._find_meta_content(soup, ["description", "og:description"])
            if desc:
                target["company_about_us"] = clean_text(desc)
                if not target.get("company_twitter_description"):
                    target["company_twitter_description"] = clean_text(desc)

        # Logo
        if not target.get("company_logo"):
            logo = self._find_meta_content(soup, ["og:logo", "og:image", "twitter:image"])
            if logo:
                target["company_logo"] = clean_text(logo)

        # Cover image (often main image)
        if not target.get("company_cover_image"):
            cover = self._find_meta_content(soup, ["og:image", "twitter:image"])
            if cover:
                target["company_cover_image"] = clean_text(cover)

        # Slogan might appear in og:title or meta tags
        if not target.get("company_slogan"):
            headline = self._find_meta_content(soup, ["og:title", "twitter:title"])
            if headline:
                headline = clean_text(headline)
                if headline and target.get("company_name") and headline != target["company_name"]:
                    target["company_slogan"] = headline

        # Followers and employees are often rendered as text; heuristics only.
        # We avoid brittle CSS selectors and just search for obvious patterns.
        body_text = soup.get_text(" ", strip=True)
        if body_text:
            # Very rough heuristic for followers
            if not target.get("company_followers_on_linkedin"):
                followers = self._extract_number_near_keyword(body_text, "followers")
                if followers is not None:
                    target["company_followers_on_linkedin"] = followers

            if not target.get("company_employees_on_linkedin"):
                employees = self._extract_number_near_keyword(body_text, "employees")
                if employees is not None:
                    target["company_employees_on_linkedin"] = employees

    @staticmethod
    def _find_meta_content(soup: BeautifulSoup, keys: List[str]) -> Optional[str]:
        for key in keys:
            tag = soup.find("meta", attrs={"name": key}) or soup.find(
                "meta", attrs={"property": key}
            )
            if tag and tag.get("content"):
                return tag["content"]
        return None

    @staticmethod
    def _extract_number_near_keyword(text: str, keyword: str) -> Optional[int]:
        # Example patterns: "10,001+ employees", "1,234 followers"
        keyword = keyword.lower()
        tokens = text.split()
        for i, token in enumerate(tokens):
            if keyword in token.lower() and i > 0:
                candidate = tokens[i - 1]
                # Remove suffixes like "+" or "·"
                candidate = candidate.rstrip("+·")
                value = safe_int(candidate)
                if value is not None:
                    return value
        return None