# web_scraping_and_web_automation
Web Scraping and Web Automation with Selenium

## Description
This program download fifty search result of a online shop website, [Digikala](https://www.digikala.com/) and show their information(title, link, picture, price) and price chart in a dashboard.


https://github.com/negar-shamshiri/web_scraping_and_web_automation/assets/35175024/cf3388af-8f99-4cc3-9251-1666af5967e3


## Install chrome driver in WSL
for using seleniom in wsl or wsl2, install chromedriver from this [website](https://www.gregbrisebois.com/posts/chromedriver-in-wsl2/) then run the code.

## How to Run
First, in main repo directory, run the following code to add `src` to your `PYTHONPATH`:
```
export PYTHONPATH=${PWD}
```

Then run:
```
python src/webScraping_webAutomation/webScraping_webAutomation.py
```
to generate a word cloud of json data in `DATA_DIR`
