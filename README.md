# browser_google_checker

<h3>This script does the following:</h3>

Get keywords and target urls from local txt file 

Uses Selenium Webdriver to open Google US in browser

Scrape Google search results for target keyword(s)

Download all search results from Google pages 1-4 to a txt file

<h3>Installation & setup</h3>

Download the latest version of Fireflox Geckodriver from here and then add to your $PATH:

https://github.com/mozilla/geckodriver/releases/tag/v0.24.0

```
export PATH=$PATH:/path/to/geckodriver

```

Then create a Python virtualenv, start it, pip install the requirements then run the Python file and pass your keywords and urls file at the same time. 

```

virtualenv env

source env/bin/activate

pip install requirements.txt

python brwsr_rank_chk.py YOUR-KEYWORDS-FILE YOUR-URLS-FILE

```
