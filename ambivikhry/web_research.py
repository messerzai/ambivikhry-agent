from __future__ import annotations

"""Read-only internet research adapter for the triad experiment.

The adapter performs ordinary HTTPS GET requests and returns bounded text.
It never receives credentials, writes to the network, or executes downloaded
content. Hosts may inject a stricter fetcher when sandboxing is required.
"""

from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import html
import re


@dataclass
class ResearchResult:
    url: str
    status: int
    title: str
    text: str

    def as_dict(self) -> dict[str, object]:
        return {
            "source": self.url,
            "status": self.status,
            "title": self.title,
            "text": self.text,
        }


class WebResearch:
    def __init__(self, *, timeout: float = 10.0, max_bytes: int = 200_000):
        self.timeout = timeout
        self.max_bytes = max_bytes

    def fetch(self, url: str) -> ResearchResult:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("only absolute http(s) URLs are allowed")

        req = Request(
            url,
            headers={"User-Agent": "Ambivikhry-Research/1.0"},
            method="GET",
        )
        with urlopen(req, timeout=self.timeout) as response:
            raw = response.read(self.max_bytes)
            charset = response.headers.get_content_charset() or "utf-8"
            body = raw.decode(charset, errors="replace")
            title_match = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
            title = html.unescape(re.sub(r"\s+", " ", title_match.group(1)).strip()) if title_match else ""
            text = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", body)
            text = re.sub(r"<[^>]+>", " ", text)
            text = html.unescape(re.sub(r"\s+", " ", text)).strip()
            return ResearchResult(str(response.url), int(response.status), title, text)
