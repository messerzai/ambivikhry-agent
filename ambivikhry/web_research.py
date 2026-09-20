from __future__ import annotations

"""Bounded, read-only web research with provenance metadata."""

from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import hashlib
import html
import re


@dataclass
class ResearchResult:
    url: str
    status: int
    title: str
    text: str
    content_sha256: str
    bytes_read: int

    def as_dict(self) -> dict[str, object]:
        return {
            "source": self.url,
            "status": self.status,
            "title": self.title,
            "text": self.text,
            "content_sha256": self.content_sha256,
            "bytes_read": self.bytes_read,
        }


class WebResearch:
    """Read-only HTTP(S) fetcher.

    It does not execute downloaded content, send credentials, or perform
    network writes. Redirects are followed by the standard library, so callers
    should apply an allowlist/sandbox policy when URLs are untrusted.
    """

    def __init__(self, *, timeout: float = 10.0, max_bytes: int = 200_000):
        self.timeout = timeout
        self.max_bytes = max_bytes

    def fetch(self, url: str) -> ResearchResult:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("only absolute http(s) URLs are allowed")
        if parsed.username or parsed.password:
            raise ValueError("credential-bearing URLs are not allowed")
        if parsed.hostname and parsed.hostname.lower() in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("local hosts are not allowed")

        req = Request(
            url,
            headers={"User-Agent": "Ambivikhry-Research/1.1"},
            method="GET",
        )
        with urlopen(req, timeout=self.timeout) as response:
            raw = response.read(self.max_bytes)
            charset = response.headers.get_content_charset() or "utf-8"
            body = raw.decode(charset, errors="replace")
            title_match = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
            title = (
                html.unescape(re.sub(r"\s+", " ", title_match.group(1)).strip())
                if title_match
                else ""
            )
            text = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", body)
            text = re.sub(r"<[^>]+>", " ", text)
            text = html.unescape(re.sub(r"\s+", " ", text)).strip()
            return ResearchResult(
                url=str(response.url),
                status=int(response.status),
                title=title,
                text=text,
                content_sha256=hashlib.sha256(raw).hexdigest(),
                bytes_read=len(raw),
            )
