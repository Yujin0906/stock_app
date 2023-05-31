'''
Tkinter를 사용하여 윈도우 프로그램을 만들기 위한 베이스 메인 윈도우 클래스를 정의하는 모듈
여기에서 기본 틀을 만들고ㄴ 이 클래스를 상속받아서 App.에 필요한 메인 윈도우를 만들 것이다.
'''
import os
import tkinter as tk
from tkinter import font

from abc import abstractclassmethod # 추상 메소드

class MainWin:
    def __init__(self,
                 title:str='Main Window',  # 윈도우 타이틀
                 width:int=640,            # 윈도우 넓이
                 height:int=480,           # 윈도우 높이
                 resize:tuple=(True, True) # 윈도우 가로, 세로 사이즈 변경 가능 여부 지정
                 ) -> None:
        
        # _(언더바 1개) : protected(상속은 되고 외부에 노출이 안됨(파이썬에서는 노출이 되기도 함)) 멤버 변수임
        self._win = tk.Tk()    # 메인 윈도우 생성
        self._win.title(title) # 메인 윈도우의 타이틀을 지정함
        left = (self._win.winfo_screenwidth() - width) // 2 # 초기 윈도우를 화면의 가운데 놓기 위해 left 값을 계산해줌
        top = (self._win.winfo_screenheight() - height) // 2
        coordination = f'{width}x{height}+{left}+{top}'
        self._win.geometry(coordination) # 윈도우의 초기 위치를 지정함
        self._win.resizable(resize[0], resize[1]) # 윈도우 리사이즈 가능 여부
        
        #
        self._initLayout()
        self.set_min_size()
        
    @property
    def Window(self) -> tk.Tk:
        '''메인 윈도우 객체를 반환함'''
        return self._win # 메소드지만 Window라는 이름의 속성값으로 반환한다.
    
    def set_min_size(self, width:int=300, height:int=300):
        '''
        사이즈가 변경될 때 윈도우의 최소 미니멈 사이즈를 결정한다. 
        이보다 더 작게 만들 수 없게 함
        '''
        self._win.minsize(width, height)    
    
    # 추상메소드 정의
    @abstractclassmethod
    def _initLayout(self): ...
    '''상속받는 서브 클래스가 이 메소드를 반드시 구현해야됨'''

    @staticmethod # staticmethod는 self가 들어가지 않음
    def get_current_path(file_name:str) -> str:
      # 현재 실행 파일의 경로와 file_name을 join해서 파일명을 가져오기
      cur_dir = os.path.dirname(os.path.abspath(__file__))
      file_path = os.path.join(cur_dir, file_name)
      
      return file_path