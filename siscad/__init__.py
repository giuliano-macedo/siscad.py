from pathlib import Path

script_path = Path(__file__).parent
__version__ = (script_path / "_version.py").read_text().strip()

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
# Mozilla/<version> (<system-information>) <platform> (<platform-details>) <extensions>
import requests
import platform

HEADERS = {
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "User-Agent": f"python-requests/{requests.__version__} ({platform.platform()}) {__package__}-{__version__}",
    "pypi-url": "https://pypi.org/project/siscad",
}
from .Siscad import Siscad
