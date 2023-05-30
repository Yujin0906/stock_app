'''
주식 정보 검색 어플리케이션의 메인 윈도우 모듈
MVC 모델에서 View를 담당하는 모듈
'''

import tkinter as tk
import tkinter.ttk as ttk
from typing import Final # 상수를 지정하기 위한 클래스
from main_window import MainWin # 부모 윈도우 클래스

class StockSearchWin(MainWin):
    '''
    MainWin클래스에서 상속받는 서브 클래스이다
    View에 관련된 모든 작업들을 이 클래스에서 처리한다
    '''
    def __init__(self, 
                 event_handler, # Controller 객체
                 title: str = 'Main Window', 
                 width: int = 1000, 
                 height: int = 650, 
                 resize: tuple = (True, True)) -> None:
        super().__init__(title, width, height, resize)
        self.eh = event_handler
        
    def _initLayout(self):
        '''윈도우 생성 후 레이아웃을 만듦'''
        self.topPanel = tk.PanedWindow(self._win, # 부모 윈도우
                                       height=30, # 높이
                                       relief='groove', # Border
                                       orient=tk.HORIZONTAL) # 방향
        self.topPanel.pack(side='top', fill='x')
        self.leftPanel = tk.PanedWindow(self._win,
                                        width=150,
                                        relief='groove',
                                        orient=tk.VERTICAL)
        self.leftPanel.pack(side='left',fill='y')
        self.rightPanel = tk.PanedWindow(self._win)
        self.rightPanel.pack(side='left',fill='both', expand=True)
        
        self.__initTopPanelLayout()
        self.__initLeftPanelLayout()
        self.__initRightPanelLayout()
        
    def __initTopPanelLayout(self):
        # 검색 레이블 생성
        self.lbSearch = ttk.Label(self.topPanel, text='검색')
        self.lbSearch.grid(row=0, column=0) # grid 배열함
        
        # 검색 입력란 생성
        self.editSearch = ttk.Entry(self.topPanel, width=30)
        self.editSearch.grid(row=0, column=1)
        
        # Go(검색) 버튼
        self.icon1 = tk.PhotoImage(file=MainWin.get_current_path('go.png')) # 이미지 객체 생성
        self.btnGo = ttk.Button(self.topPanel,
                                text='Go',
                                image=self.icon1,
                                width=10
                                #compound='left',
                                )
        self.btnGo.grid(row=0, column=2)
        
        # 검색 결과값이 임시 저장될 콤보박스
        self.cbSearched = ttk.Combobox(self.topPanel,
                                       state='readonly' # 읽기 전용
                                       )
        self.cbSearched['values'] = [1,2,3]
        self.cbSearched.current(0) # 출력값(노출되는 값)의 인덱스를 지정
        self.cbSearched.grid(row=0,column=3)
        self.btnFavor = ttk.Button(self.topPanel,
                                text='즐겨찾기',
                                # image=self.icon1,
                                width=10
                                # compound='left',
                                )
        self.btnFavor.grid(row=0, column=4)
    
    def __initLeftPanelLayout(self):
        '''왼쪽 패널의 하위 위젯들을 생성하고 배치함'''
        # 즐겨찾기 라벨
        self.lbFavor = ttk.Label(self.leftPanel, text='즐겨찾기')
        self.lbFavor.pack(side='top', fill='x')
        
        # 즐겨찾기 리스트박스
        self.lboxFavor = tk.Listbox(self.leftPanel,
                                    width=20,
                                    selectmode='single')
        self.lboxFavor.pack(side='top', fill='both', expand=True)
        
    def __initRightPanelLayout(self):
        width_big:Final = 25
        width_field:Final = 20
        width_field_small:Final = 15
        height_mid_panel:Final = 300
        ftBig:Final = 20
        ftNormal:Final = 12
        ftMalgun:Final = 'Malgun Gothic'
        
        self.rpTopPanel = tk.PanedWindow(self.rightPanel, bg='red') # rp = RightPanel
        self.rpTopPanel.pack(side='top', fill='x')
        
        # 위젯들을 배치할 것임
        # 코드 라벨
        self.lbCode = ttk.Label(self.rpTopPanel,
                                text='CODE',
                                width=width_field)
        self.lbCode.grid(row=0, column=0, sticky='w')
        
        # 종목명 레이블 위젯 생성
        self.lbJong = ttk.Label(self.rpTopPanel,
                                text='종목',
                                width=width_big,
                                font=(ftMalgun, 24, 'bold'))
        self.lbJong.grid(row=1, column=0, columnspan=4, sticky='w')
        
        # 종가(일반 주가) 레이블
        self.lbValue = ttk.Label(self.rpTopPanel,
                                 text='종가',
                                 width=width_field,
                                 font=(ftMalgun, ftBig),
                                 foreground='red')
        
        self.lbValue.grid(row=2, column=0, sticky='nsw')

        # 전일비
        self.lbChange = ttk.Label(self.rpTopPanel,
                                  text='전일대비',
                                  width=width_big+5,
                                  font=(ftMalgun, ftNormal),
                                  foreground='red')
        self.lbChange.grid(row=3,column=0, sticky='nsw')
        
        # 미들 윈도우 영역                
        self.rpMidPanel = tk.PanedWindow(self.rightPanel,
                                         bg='blue',
                                         height=height_mid_panel)
        self.rpMidPanel.pack(side='top', fill='x')
        
        self.rpBottomPanel = tk.PanedWindow(self.rightPanel,bg='green')
        self.rpBottomPanel.pack(side='top', fill='both', expand=True)
        
        
        
class Dummy:
    pass
        
dumy = Dummy()
sswin = StockSearchWin(dumy) # 객체화, 생성
sswin.Window.mainloop() # 윈도우 메인루프
