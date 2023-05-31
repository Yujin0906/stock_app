'''
App 객체
MVC 모델의 Controller 역할을 담당하는 모듈
이 모듈에서 App을 실행한다.
'''
import time, json
import tkinter as tk
import tkinter.ttk as ttk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# 우리의 모듈들
from main_window import MainWin
from stock_window import StockSearchWin
from stock_data import StockData

class StockSearchApp:
    def __init__(self,
                 title="Stock Search Application",
                 width:int=640,
                 height:int=480,
                 resize:tuple=(True, True)) -> None:
        
        # 메인 윈도우 생성
        self.MainWindow = StockSearchWin(self, # 가장 중요한 부분임! 다시 복습하기
                                         title=title,
                                         width=width,
                                         height=height,
                                         resize=resize) # 객체화, 생성
        self.li_url = {}
        
        # 메인 데이터 (Model)
        self.data = StockData()
        
    @property
    def Window(self) -> tk.Tk:
        return self.MainWindow.Window

    def OnBtnGoClick(self, win:StockSearchWin, obj:ttk.Button):
        # 검색란에 있는 값을 읽어서 크롤링을 한다.
        # 크롤링을 selenium을 이용해서 browsing...
        
        # 검색란에 있는 텍스트를 toFind라는 변수에 저장
        toFind = win.editSearch.get()
        
        print(toFind)
        
        if toFind=='':
            return
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        
        config_path = MainWin.get_current_path('config.json')
        with open(config_path, 'r', encoding='utf-8') as fconf:
            conf_data = json.load(fconf)
            
        url = conf_data['Search URL']
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        toSearchEntry = driver.find_element(By.XPATH, '//*[@id="stock_items"]')
        toSearchEntry.send_keys(toFind) # 입력란에 검색할 워드를 대입함
        toSearchEntry.send_keys(Keys.ENTER)
        
        time.sleep(1) # 검색 결과를 위해 1초 기다림
        
        # 검색 결과를 가져와서 그 내용을 콤보박스에 대입함
        no_res = driver.find_element(By.XPATH, '//*[@id="content"]/div[3]')
        if no_res.get_attribute('class')=='no_data': # class 속성이 'no_data'라는 태그를 찾았으면 검색 결과가 없는 것이니...
            win.cbSearched['values'] = ['검색 결과 없음']
            win.cbSearched.current(0) # 첫 번째 데이터를 나타내라
            return
        
        tbody = driver.find_element(By.XPATH, '//*[@id="content"]/div[4]/table/tbody')
        name_elems = tbody.find_elements(By.CLASS_NAME, 'tit')
        
        # {키 : 벨류} ==> 키는 종목명, 벨류는 종목명에 대한 상세 정보 URL
        self.li_url = {elem.text: elem.find_element(By.TAG_NAME, 'a').get_attribute('href') for elem in name_elems}
        win.cbSearched['values'] = list(self.li_url.keys())
        win.cbSearched.current(0)
        
        # 검색이 끝난 후 현재 선택된 콤보박스의 텍스트로 첫 번째 검색 시도
        self.__SearchStockName(win, win.cbSearched.get())
        
        driver.quit()
        
    def OnSearchedComboBoxSelected(self, event, win:StockSearchWin, obj:ttk.Combobox):
        stock_name = obj.get() # combo box에 나타나있는 텍스트를 가져온다
        self.__SearchStockName(win, stock_name)
        
    def __SearchStockName(self, win:StockSearchWin, stock_name:str):
        # 종목명 레이블을 설정한다.
        win.lbJong.configure(text=stock_name)
        
        # 검색단계에서 추출한 url을 가져온다
        url = self.li_url[stock_name]
        
        # Chrome driver를 이용하여 검색
        driver = webdriver.Chrome()
        driver.get(url)
        
        # 종목 코드
        code = driver.find_element(By.XPATH, '//*[@id="middle"]/div[1]/div[1]/div/span[1]').text.strip()
        win.lbCode.configure(text=f'CODE : {code}')
        
        # 현재가를 가져오기 전에 주가가 올랐는지 내렸는지부터 검사한다
        color = 'black' # 기본 컬러는 블랙 
        no_today = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/div/p[1]/em')
        if no_today.get_attribute('class')=='no_up':
            color = 'red'
        elif no_today.get_attribute('class')=='no_down':
            color = 'blue'
        
        # 현재가
        jongga = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/div/p[1]')
        jongga_text = jongga.text.strip('\n').replace('\n', '')
        win.lbValue.configure(text=jongga_text, foreground=color)
        
        # 전일비
        change = driver.find_element(By.XPATH, '//*[@id="chart_area"]/div[1]/div/p[2]')
        change_text = change.text.strip('\n').replace('\n', '')
        win.lbValue.configure(text=change_text, foreground=color)
        
        pass

app = StockSearchApp(title="주식 정보 검색",
                     width=1000,
                     height=800)
app.Window.mainloop()

# sswin.Window.mainloop() # 윈도우 메인루프
