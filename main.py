from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        print("Sign Up button pressed")
        self.manager.current="sign_up_screen" #this is how to change screen
    
    def login(self,usname,pword):
        with open('users.json') as file:
            users=json.load(file)
            if usname in users and users[usname]['password']==pword:
                self.manager.current="login_screen_success"
            else:
                self.ids.login_wrong.text='Wrong username or password'

class RootWidget(ScreenManager):
    pass

#classes go for screens <> in kivy file

class SignUpScreen(Screen):
    def add_user(self,usname,pword):
        with open('users.json') as file:
            users=json.load(file)
        
        users[usname] = {'username': usname, 'password':pword,
            'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        print(users)
        
        with open('users.json','w') as file:
            json.dump(users, file)
        self.manager.current="sign_up_screen_success"
        #this is how to change screen


class SignUpScreenSuccess(Screen):
    def go_to_login(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"    

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"  

    def get_quote(self,feel):
        feel=feel.lower()
        available_feelings=glob.glob("quotes/*txt")

        available_feelings=[Path(filename).stem for filename in available_feelings]
        
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding='utf8') as file:
                quotes = file.readlines()
            self.ids.quote.text=random.choice(quotes)
        else:
            self.ids.quote.text="Try another feeling"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class MainApp(App): 
    def build(self):
        return RootWidget()



if __name__ == "__main__":
    MainApp().run()
