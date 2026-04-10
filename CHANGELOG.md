# 1.8 - 10/03/2026
- Improved the code
- Fixed false positives
- Improved performance
- Removed jsbeautifier lib
- Added more regexes matches

<br>

# 1.7 - 10/05/2025
- Removed "banner.txt" file
- Removed ASCII art from banner
- Changed color and print scheme
- Changed "rich.print" to "rich.console.print"
- Improved the code
- Add -H option, now you can specify custom headers, for example:
    ```
    python3 main.py -u https://webhook.site/793d267f-c86a-48e6-94e6-9513d0f8917a -H "First-Header" "First-Header-Value" -H "Second-Header" "Second-Header-Value"
    GET 	https://webhook.site/793d267f-c86a-48e6-94e6-9513d0f8917a
    second-header 	Second-Header-Value
    first-header 	First-Header-Value
    ```
- Removed Heroku API Key regex because of false positives

<br>

# 1.6c - 20/07/2023
- Major changes
- Removed "assets" folder (moved banner img to imgur)

<br>

# 1.6b - 06/08/2022
- Added 2 new secrets regex patterns:
    - Asana Client ID
    - Asana Client Secret
- IPv4 regex pattern removed because of false positives

<br>

# 1.6a - 04/08/2022
- Added 4 new secrets regex patterns:
    - Shopify Access Token
    - Shopify Custom Access Token
    - Shopify Private App Access Token
    - Shopify Shared Secret
- Changed regex and jsbeautify import libs

<br>

# 1.6 - 31/07/2022
- Added 11 new secrets regex patterns:
    - URL Schemes
    - Adobe Client Secret
    - Alibaba AccessKey ID
    - Clojars API Token
    - Doppler API Token
    - Dynatrace API Token
    - EasyPost API Token
    - GitHub App Token
    - GitHub Personal Access Token
    - GitLab Personal Access Token
    - NPM Access Token
- Fixed GCP API Key regex
- Removed useless if/else code

<br>

# 1.5a - 28/07/2022
- Added 2 new secrets regex patterns:
    - Slack Webhook+
    - Slack OAuth Tokens

<br>

# 1.5 - 28/07/2022
- Added 9 new secrets regex patterns:
    - Artifactory API Token & Password
    - Cloudinary Basic Auth
    - Facebook Client ID
    - IPv4 Address
    - Linkedin Secret Key
    - Picatic API Key
    - Mailto String
    - Slack Token
    - URL Parameters
- Fixed error message when not parsing arguments
- Changed status messages icons
- Changed README.md banner
- Updated README.md

<br>

# 1.4 - 18/07/2022
- Added 5 new secrets regex patterns:
    - PGP Private Key Block
    - SSH DSA Private Key
    - SSH EC Private Key
    - SSH RSA Key
    - SSH ED25519 Public Key

- Added jsbeautifier lib to improve regex pattern matching
- Fixed blank regex pattern matching caused by not beautified code
- Fixed infinite JavaScript file scanning

<br>

# 1.3 - 04/07/2022
- Added and updated a bunch of secrets regex:
    - Cloudinary
    - Firebase URL
    - Slack Token
    - Facebook Access & API
    - Mailgun API Key
    - Heroku API Key
    - Picatic API Key
    - Paypal Braintree
    - Twitter Access & OAuth Token
    - GitHub URL
    - Stripe
    - Slack Webhook
    - Twilio API Key
    - Square Access Token & OAuth Secret

- Removed text file with URLs scanner to fix bugs

<br>

# 1.2b - 21/06/2022
- Pinkerton accept a text file with URLs now!

<br>

# 1.2 - 21/06/2022
- Secret searcher module finished!
- Improved the code

<br>

# 1.1 - 20/06/2022
- JavaScript file link extractor finished!
- Improved the code
- Thinking in a better color system...

<br>

# 1.0 - 09/06/2022
- Official Pinkerton release
