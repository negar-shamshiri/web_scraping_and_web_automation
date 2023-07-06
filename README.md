# web_scraping_and_web_automation
Web Scraping and Web Automation with Selenium

## Description
This program downloads fifty search results of a online shop website, [Digikala](https://www.digikala.com/) and shows their information(titles, links, pictures, prices) and price chart in a dashboard.


https://github.com/negar-shamshiri/web_scraping_and_web_automation/assets/35175024/b64f8862-43ec-44dd-959b-a51184c883c3


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
