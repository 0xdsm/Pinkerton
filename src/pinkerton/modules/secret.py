from re import compile, sub
from requests import get, Response, exceptions
from rich.console import Console

console = Console()

_STATEMENT_BOUNDARY = compile(r'([;{}])')


def _normalize_js(content: str) -> str:
    """
    O(n) normalization: inserts newlines at JS statement boundaries.
    Limits the scope of greedy .* patterns that would otherwise span
    the entire file in single-line minified JavaScript.
    """
    return _STATEMENT_BOUNDARY.sub(r'\1\n', content)

_PATTERNS: dict = {
    # AWS
    "Amazon AWS Access Key ID": compile(r'AKIA[0-9A-Z]{16}'),
    "Amazon MWS Auth Token": compile(
        r'amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    ),
    "Amazon AWS S3 URL": compile(
        r's3\.amazonaws\.com/+|[a-zA-Z0-9_\-]+\.s3\.amazonaws\.com'
    ),

    # Google
    "Google API Key": compile(r'AIza[0-9A-Za-z\-_]{35}'),
    "Google OAuth Access Token": compile(r'ya29\.[0-9A-Za-z\-_]+'),
    "Google Cloud Platform OAuth": compile(
        r'[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com'
    ),
    "Google GCP Service Account": compile(r'"type"\s*:\s*"service_account"'),
    "Google Captcha Key": compile(r'6L[0-9A-Za-z\-_]{38}'),

    # Firebase
    "Firebase Key": compile(r'AAAA[A-Za-z0-9_\-]{7}:[A-Za-z0-9_\-]{140}'),
    "Firebase URL": compile(r'[a-zA-Z0-9\-]+\.firebaseio\.com'),

    # GitHub
    "GitHub Personal Access Token": compile(r'ghp_[0-9a-zA-Z]{36}'),
    "GitHub App Token": compile(r'(?:ghu|ghs)_[0-9a-zA-Z]{36}'),
    "GitHub Access Token": compile(r'[a-zA-Z0-9_\-]+:[a-zA-Z0-9_\-]+@github\.com'),
    "GitHub URL": compile(r"(?i)github.*['\"][0-9a-zA-Z]{35,40}['\"]"),

    # GitLab
    "GitLab Personal Access Token": compile(r'glpat-[0-9a-zA-Z\-_]{20}'),

    # Slack
    "Slack Token": compile(
        r'xox[pboa]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32}'
    ),
    "Slack Webhook": compile(
        r'https://hooks\.slack\.com/services/T\w{8}/B\w{8}/\w{24}'
    ),
    "Slack Webhook Short": compile(
        r'T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}'
    ),
    "Slack OAuth v2 Bot Token": compile(
        r'xoxb-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}'
    ),
    "Slack OAuth v2 Config Token": compile(
        r'xoxe\.xoxp-1-[0-9a-zA-Z]{166}'
    ),

    # Stripe
    "Stripe API Key": compile(r'sk_live_[0-9a-zA-Z]{24}'),
    "Stripe Restricted API Key": compile(r'rk_live_[0-9a-zA-Z]{24}'),

    # Shopify
    "Shopify Private App Access Token": compile(r'shppa_[a-fA-F0-9]{32}'),
    "Shopify Shared Secret": compile(r'shpss_[a-fA-F0-9]{32}'),
    "Shopify Custom Access Token": compile(r'shpca_[a-fA-F0-9]{32}'),
    "Shopify Access Token": compile(r'shpat_[a-fA-F0-9]{32}'),

    # Social / Marketing
    "Twitter Access Token": compile(r"(?i)twitter.*[1-9][0-9]+-\w{40}"),
    "Twitter OAuth": compile(r"(?i)twitter.*['\"][a-zA-Z0-9_]{35,44}['\"]"),
    "Twitter Client ID": compile(r"(?i)twitter(?:.{0,20})?['\"][0-9a-z]{18,25}"),
    "Facebook Access Token": compile(r'EAACEdEose0cBA[0-9A-Za-z]+'),
    "Facebook OAuth": compile(r"(?i)facebook.*['\"][0-9a-f]{32}['\"]"),
    "Facebook Client ID": compile(r"(?i)(?:facebook|fb)(?:.{0,20})?['\"][0-9]{13,17}"),
    "LinkedIn Secret Key": compile(r"(?i)linkedin(?:.{0,20})?['\"][0-9a-z]{16}['\"]"),

    # Artifactory
    "Artifactory API Token": compile(r'(?:\s|=|:|"|^)AKC[a-zA-Z0-9]{10,}'),
    "Artifactory Password": compile(r'(?:\s|=|:|"|^)AP[\dABCDEF][a-zA-Z0-9]{8,}'),

    # Payment
    "PayPal Braintree Access Token": compile(
        r'access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}'
    ),
    "Square Access Token": compile(r'sq0atp-[0-9A-Za-z\-_]{22}'),
    "Square OAuth Secret": compile(r'sq0csp-[0-9A-Za-z\-_]{43}'),

    # Cloud / SaaS
    "Cloudinary Basic Auth": compile(r'cloudinary://[0-9]{15}:[0-9A-Za-z]+@[a-z]+'),
    "Picatic API Key": compile(r'sk_live_[0-9a-z]{32}'),
    "Adobe Client Secret": compile(r"(?i)\bp8e-[a-zA-Z0-9]{32}"),
    "Alibaba AccessKey ID": compile(r"\bLTAI[a-zA-Z0-9]{20}\b"),
    "Clojars API Token": compile(r"(?i)CLOJARS_[a-z0-9]{60}"),
    "Doppler API Token": compile(r"dp\.pt\.[a-zA-Z0-9]{43}"),
    "Dynatrace API Token": compile(r"dt0c01\.[a-zA-Z0-9]{24}\.[a-z0-9]{64}"),
    "EasyPost API Token": compile(r"EZAK[a-zA-Z0-9]{54}"),
    "NPM Access Token": compile(r"\bnpm_[a-z0-9]{36}\b"),
    "Mailgun API Key": compile(r'key-[0-9a-zA-Z]{32}'),
    "MailChimp API Key": compile(r'[0-9a-f]{32}-us[0-9]{1,2}'),
    "Twilio API Key": compile(r'SK[0-9a-fA-F]{32}'),
    "Asana Client ID": compile(
        r"(?i)asana[0-9a-z\-_\t .]{0,20}[\s'\"]{0,3}(?:=|>|:=|\|\|:|<=|=>|:)['\"\s=`]{0,5}([0-9]{16})['\"\n\r\s`;]"
    ),
    "Asana Client Secret": compile(
        r"(?i)asana[0-9a-z\-_\t .]{0,20}[\s'\"]{0,3}(?:=|>|:=|\|\|:|<=|=>|:)['\"\s=`]{0,5}([a-z0-9]{32})['\"\n\r\s`;]"
    ),

    # Authentication
    "Authorization Bearer": compile(r'[Bb]earer [a-zA-Z0-9_\-\.=]+'),
    "Authorization Basic": compile(r'[Bb]asic [a-zA-Z0-9=:_\+/\-]{5,100}'),
    "JWT Token": compile(
        r'ey[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_.+/=]+'
    ),

    # Private keys
    "PGP Private Key Block": compile(r'-----BEGIN PGP PRIVATE KEY BLOCK-----'),
    "SSH DSA Private Key": compile(r'-----BEGIN DSA PRIVATE KEY-----'),
    "SSH EC Private Key": compile(r'-----BEGIN EC PRIVATE KEY-----'),
    "SSH OpenSSH Private Key": compile(r'-----BEGIN OPENSSH PRIVATE KEY-----'),
    "RSA Private Key": compile(r'-----BEGIN RSA PRIVATE KEY-----'),
    "SSH ed25519 Public Key": compile(r'ssh-ed25519'),

    # Generic (high false-positive risk)
    "Generic API Key": compile(
        r"(?i)api[_]?key\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{32,45})['\"]"
    ),
    "Generic Secret": compile(
        r"(?i)secret\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{32,45})['\"]"
    ),

    # Other
    "Mailto": compile(
        r'(?<=mailto:)[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9.\-]+'
    ),
}


def _scan_content(content: str, source: str) -> None:
    """Run all patterns against normalized content and print matches."""
    normalized = _normalize_js(content)
    for name, pattern in _PATTERNS.items():
        matches = pattern.findall(normalized)
        if matches:
            console.print(
                f"\n[[green]+[/]] [yellow]{name}[/] found in [yellow]{source}[/]: {matches}\n",
                highlight=False,
            )


def scan(url: str, custom_headers: dict) -> None:
    """Fetch a remote JavaScript file and scan it for exposed secrets."""
    try:
        response: Response = get(url, headers=custom_headers, timeout=30)
        response.raise_for_status()
    except exceptions.RequestException as req_error:
        console.print(
            f"[[red]![/]] Failed to fetch [yellow]{url}[/]: {req_error}",
            highlight=False,
        )
        return
    _scan_content(response.text, url)


def scan_file(path: str) -> None:
    """Read a local JavaScript file and scan it for exposed secrets."""
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            content = f.read()
    except OSError as os_error:
        console.print(
            f"[[red]![/]] Failed to read [yellow]{path}[/]: {os_error}",
            highlight=False,
        )
        return
    _scan_content(content, path)
