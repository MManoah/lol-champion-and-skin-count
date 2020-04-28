from tkinter import *
from tkinter import messagebox
import psutil
from PIL import Image, ImageTk
from lcu_driver import Connector

Window_Width = 200
Window_Height = 200
connector = Connector()


class MainWindow:
    owned_champion_count = 0
    owned_skin_count = 0

    def __init__(self, master):
        master.iconbitmap('Icon.ico')
        self.master = master
        master.title('Champion and Skin Count')
        canvas = Canvas(master, height=Window_Height, width=Window_Width)
        canvas.pack()
        main_window_background = Image.open('main_window_background.jpg')
        main_window_background = main_window_background.resize((365, 203), Image.ANTIALIAS)
        main_window_background = ImageTk.PhotoImage(main_window_background)
        main_background = Label(master, image=main_window_background)
        main_background.image = main_window_background
        main_background.place(relwidth=1, relheight=1)

        champion_info = Text(master, fg='#e6e6ff', bg='#0E0E0E', borderwidth=2, relief="groove")
        champion_info.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)
        champion_info.insert('end', 'Champions:\t\t')
        champion_info.insert('end', self.owned_champion_count)
        skin_info = Text(master, fg='#e6e6ff', bg='#0E0E0E', borderwidth=2, relief="groove")
        skin_info.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.1)
        skin_info.insert('end', 'Skins:\t\t')
        skin_info.insert('end', self.owned_skin_count)


def on_startup():
    @connector.event
    async def connect():
        summoner = await connector.request('get', '/lol-summoner/v1/current-summoner')
        if summoner.status == 200:
            data = await summoner.json()
            summoner = str(data['summonerId'])
            champion_get = await connector.request('get',
                                                   '/lol-champions/v1/inventories/' + summoner + '/champions')
            champion_data = await champion_get.json()
            for x in range(len(champion_data)):
                if champion_data[x]['ownership']['owned']:
                    MainWindow.owned_champion_count += 1
            skin_get = await connector.request('get', '/lol-champions/v1/inventories/' + summoner + '/skins-minimal')
            skin_get = await skin_get.json()
            for x in range(len(skin_get)):
                if skin_get[x]['ownership']['rental']['purchaseDate'] != 0:
                    MainWindow.owned_skin_count += 1
        else:
            messagebox.showerror("ERROR", "THERE WAS AN ERROR")
            exit(1)

    connector.start()


def process_exists():
    for p in psutil.process_iter():
        try:
            if p.name() == 'LeagueClient.exe':
                return True
        except psutil.Error:
            return False


if __name__ == '__main__':
    if process_exists():
        on_startup()
        root = Tk()
        root.resizable(0, 0)
        application = MainWindow(root)
        root.mainloop()
    else:
        messagebox.showerror("ERROR", "LEAGUE CLIENT IS NOT OPEN")
