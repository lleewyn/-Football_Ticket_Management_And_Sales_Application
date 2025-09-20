from tkinter import Tk
from tkinter import messagebox
import Modules.User.Landing_Page.Main_Page_View as usmv
import Modules.User.My_Tickets.My_Tickets_View as mtv
import Modules.User.User_Information.User_Information_View as uiv
import Modules.Login.Login_View as lg

class User_Main_Page_process:
    @staticmethod
    def home_button_handle(obj):
        obj.window.destroy()
        new_window = Tk()
        app = usmv.MainPage_View(new_window, obj.user_info)
        app.window.mainloop()

    @staticmethod
    def my_tickets_button_handle(obj):
        obj.window.destroy()
        new_window = Tk()
        app = mtv.MyTickets_View(new_window, obj.user_info)
        app.window.mainloop()

    @staticmethod
    def user_info_button_handle(obj):
        obj.window.destroy()
        new_window = Tk()
        app = uiv.UserInformation_View(new_window, obj.user_info)
        app.window.mainloop()

    @staticmethod
    def back_login_button_handle(obj):
        confirm = messagebox.askyesno(
            title="Confirm Logout",
            message="Are you sure you want to log out?",
            parent=obj.window)
        if confirm:
            obj.window.destroy()
            app = lg.Login_View()
            app.window.mainloop()
        else:
            return