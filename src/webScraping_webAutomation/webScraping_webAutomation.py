import time

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class WebScraping:
    """
    Generate table and graph by web scraping and web automation from sites
    """
    def __init__(self, url: str):
        """
        Args:
            url (str): URL path of sites
        """
        self.app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
        self.search_input = dbc.Input(
            placeholder='جستجو',
            style={'text-align': 'right',
                   'margin-top': '20px'},
            debounce=True,)
        self.search_btn = dbc.Button(
            'جستجو کن', style={'margin-top': '20px',
                               'width': '200px',
                               'marginLeft': '600px'})

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options)
        self.driver.get(url)

        self.my_div = html.Div()
        self.my_graph = dcc.Graph(figure={})

    def GenerateDashPage(self):
        @self.app.callback(
            Output(self.search_btn, component_property='n_clicks'),
            Output(self.my_div, component_property='children'),
            Output(self.my_graph, component_property='figure'),
            Input(self.search_btn, component_property='n_clicks'),
            Input(self.search_input, component_property='value'),)
        def extract_content_by_input(n_clicks, value):
            if n_clicks:
                search_btn_scraping = WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".color-500.d-flex.ai-center.text-body-2")))
                search_btn_scraping.click()

                search_input_scraping = WebDriverWait(self.driver, 100).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".px-2.TextField_TextField__input__hFMFl.text-subtitle.w-100.TextField_TextField__bwN9_.TextField_TextField--primary__IZ6Ku.color-500.text-body-2.text-body-2")))
                search_input_scraping.send_keys(f'{value}')
                search_input_scraping.send_keys(Keys.ENTER)
                time.sleep(10)

                products_info = self.get_contents()
                children = self.create_table(products_info)
                figure = self.create_graph(products_info)

                return n_clicks, children, figure

        self.app.layout = dbc.Container([dbc.Row(
            [self.search_input,
             self.search_btn,
             self.my_div,
             self.my_graph], className='text-center')])

    def get_contents(self):
        links = ''
        titles = ''
        prices = ''
        img_src = ''
        products_info = []

        for i in range(1, 51):
            self.driver.execute_script('window.scrollTo(0,9000)')
            time.sleep(0.3)

            search_links = self.driver.find_element(
                By.XPATH,
                f'//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a')
            links = str(search_links.get_attribute('href'))

            search_content = self.driver.find_element(
                By.XPATH,
                f'//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a/div/article/div[2]/div[1]/div/div/div[1]/div/picture/img')
            titles = str(search_content.get_attribute('alt'))

            search_content = self.driver.find_element(
                By.XPATH,
                f'//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a/div/article/div[2]/div[1]/div/div/div[1]/div/picture/img')
            img_src = search_content.get_attribute('data-src')

            try:
                search_price = self.driver.find_element(
                    By.XPATH,
                    f'//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[4]/div[1]/div[2]/span')
            except Exception:
                search_price = self.driver.find_element(
                    By.XPATH,
                    f'//*[@id="ProductListPagesWrapper"]/section/div[2]/div[{i}]/a/div/article/div[2]/div[2]/div[4]/div[1]/div/span'    )
            prices = str(search_price.get_attribute('innerHTML'))+"\n"

            products_info.append((titles, prices, links, img_src))
        
        return products_info

    def create_table(self, products_info):
        rows = [html.Tr([
            html.Th('تصویر'),
            html.Th('قیمت(تومان)'),
            html.Th('عنوان'),
            html.Th('ردیف'), ])]

        for i, (titles, prices, links, img_src) in enumerate(products_info):
            img = html.Img(src=img_src, width='100px', height='100px')
            d = html.Tr([html.Td(img), html.Td(prices), html.A(titles, href=links), html.Td(i+1)])
            rows.append(d)
        children = [html.Table(rows, style={'width': '100%', 'margin-top': '50px', 'border-bottom': '1px solid #ddd', 'border-color': '#46637f'})]
        return children

    def create_graph(self, products_info):
        prices = [info[1] for info in products_info]
        number_list = [int(price.replace(',', '')) for price in prices]
        table_layout = go.Layout(title="نمودار قیمت", xaxis_title="شماره ردیف", yaxis_title="قیمت", template="plotly_dark", )
        figure = go.Figure(data=go.Scatter(x=list(range(1, len(number_list)+1)), y=number_list), layout=table_layout,)
        return figure


if __name__ == '__main__':
    web_scraping = WebScraping('https://www.digikala.com/')
    web_scraping.GenerateDashPage()
    web_scraping.app.run_server(port='8000')
