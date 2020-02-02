from datetime import datetime
from tkinter import *
from tkinter import messagebox
import psutil
from PIL import Image, ImageTk
from lcu_driver import Connector
import tkinter.scrolledtext as scrolledtext

Window_Width = 600
Window_Height = 300
connector = Connector()


class MainWindow:
    owned_champion_count = 0
    owned_champions = []
    owned_skins = []
    owned_skin_count = 0
    skins_purchased_date = {}
    champions_purchased_date = {}

    def __init__(self, master):
        master.iconbitmap('Icon.ico')
        self.owned_champions.sort()
        self.master = master
        master.title('Champion and Skin Information')
        canvas = Canvas(master, height=Window_Height, width=Window_Width)
        canvas.pack()
        main_window_background = Image.open('main_window_background.jpg')
        main_window_background = main_window_background.resize((614, 341), Image.ANTIALIAS)
        main_window_background = ImageTk.PhotoImage(main_window_background)
        main_background = Label(master, image=main_window_background)
        main_background.image = main_window_background
        main_background.place(relwidth=1, relheight=1)

        champion_info = Text(master, fg='#e6e6ff', bg='#0E0E0E', borderwidth=2, relief="groove")
        champion_info.place(relx=0.35, rely=0.2, relwidth=0.27, relheight=0.07)
        champion_info.insert('end', 'Champions:\t\t')
        champion_info.insert('end', self.owned_champion_count)
        skin_info = Text(master, fg='#e6e6ff', bg='#0E0E0E', borderwidth=2, relief="groove")
        skin_info.place(relx=0.35, rely=0.6, relwidth=0.27, relheight=0.07)
        skin_info.insert('end', 'Skins:\t\t')
        skin_info.insert('end', self.owned_skin_count)

        champions = Button(master, text="Champion List", fg='#e6e6ff',
                           bg='#0E0E0E', command=lambda: self.champion_window(False))
        champions.place(relx=0.03, rely=0.8, relwidth=0.2, relheight=0.1)
        champions_date = Button(master, text="With Purchased Date", fg='#e6e6ff',
                                bg='#0E0E0E', command=lambda: self.champion_window(True))
        champions_date.place(relx=0.03, rely=0.91, relwidth=0.2, relheight=0.08)

        skins = Button(master, text="Skin List", fg='#e6e6ff',
                       bg='#0E0E0E', command=lambda: self.skin_window(False))
        skins.place(relx=0.77, rely=0.8, relwidth=0.2, relheight=0.1)
        skins_date = Button(master, text="With Purchased Date", fg='#e6e6ff',
                            bg='#0E0E0E', command=lambda: self.skin_window(True))
        skins_date.place(relx=0.77, rely=0.91, relwidth=0.2, relheight=0.08)

    def champion_window(self, date):
        if date:
            championw = Toplevel(self.master)
            ChampionsWindow(championw, True)
        else:
            championw = Toplevel(self.master)
            ChampionsWindow(championw, False)

    def skin_window(self, date):
        if date:
            skinw = Toplevel(self.master)
            SkinsWindow(skinw, True)
        else:
            skinw = Toplevel(self.master)
            SkinsWindow(skinw, False)


class SkinsWindow:
    def __init__(self, master, date):
        self.master = master
        master.iconbitmap('Icon.ico')
        master.title('Skins')
        master.resizable(0, 0)
        skin_canvas = Canvas(master, height=650, width=650)
        skin_canvas.pack()
        skin_background = Image.open("skin_window_background.jpg")
        skin_background = skin_background.resize((1323, 677), Image.ANTIALIAS)
        skin_bg = ImageTk.PhotoImage(skin_background)
        skin_background_window = Label(master, image=skin_bg)
        skin_background_window.image = skin_bg
        skin_background_window.place(relwidth=1, relheight=1)
        text = scrolledtext.ScrolledText(skin_background_window, fg='#e6e6ff', bg='#0E0E0E', borderwidth=2,
                                         relief="groove")
        text['font'] = ('Courier', '12')
        text.place(relx=0.025, rely=0.02, relwidth=0.95, relheight=0.96)
        text.insert('end', 'To Copy Paste: Highlight all text then CTRL+C to copy and \nCTRL+V to paste\n\n')
        text.insert('end', 'SKINS:\n')
        if not date:
            temp = MainWindow.owned_champions[0]
            for x in range(len(MainWindow.owned_champions)):
                owned = False
                for i in range(len(MainWindow.owned_skins)):
                    if temp in MainWindow.owned_skins[i]:
                        text.insert('end', '\n' + MainWindow.owned_skins[i])
                        owned = True
                    else:
                        temp = MainWindow.owned_champions[x]
                if owned:
                    text.insert('end', '\n')
        else:
            temp = MainWindow.owned_champions[0]
            for x in range(len(MainWindow.owned_champions)):
                owned = False
                for i in range(len(MainWindow.owned_skins)):
                    if temp in MainWindow.owned_skins[i]:
                        text.insert('end', '\n' + MainWindow.owned_skins[i])
                        text.insert('end', '\t\t\t -')
                        text.insert('end', datetime.fromtimestamp(
                            MainWindow.skins_purchased_date[MainWindow.owned_skins[i]] / 1000.0).strftime(
                            '%B %d %Y %I:%M %p'))
                        owned = True
                    else:
                        temp = MainWindow.owned_champions[x]
                if owned:
                    text.insert('end', '\n')


class ChampionsWindow:
    def __init__(self, master, date):
        self.master = master
        master.iconbitmap('Icon.ico')
        master.title('Champions')
        master.resizable(0, 0)
        champion_canvas = Canvas(master, height=650, width=650)
        champion_canvas.pack()
        champion_background = Image.open("Champion_window_background.jpg")
        champion_background = champion_background.resize((1114, 660), Image.ANTIALIAS)
        champion_bg = ImageTk.PhotoImage(champion_background)
        champions_background_window = Label(master, image=champion_bg)
        champions_background_window.image = champion_bg
        champions_background_window.place(relwidth=1, relheight=1)
        text = scrolledtext.ScrolledText(champions_background_window, fg='#e6e6ff', bg='#0E0E0E', borderwidth=2,
                                         relief="groove")
        text['font'] = ('Courier', '12')
        text.place(relx=0.025, rely=0.02, relwidth=0.95, relheight=0.96)
        text.insert('end', 'To Copy Paste: Highlight all text then CTRL+C to copy and \nCTRL+V to paste\n\n')
        text.insert('end', 'CHAMPIONS:\n')
        if not date:
            for x in MainWindow.owned_champions:
                text.insert('end', '\n' + x)
        else:
            for x in range(len(MainWindow.owned_champions)):
                text.insert('end', '\n' + MainWindow.owned_champions[x] + '\t\t -')
                text.insert('end', datetime.fromtimestamp(
                    MainWindow.champions_purchased_date[MainWindow.owned_champions[x]] / 1000.0).strftime(
                    '%B %d %Y %I:%M %p'))
                text.insert('end', '\n')


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
                    if champion_data[x]['alias'] == 'MonkeyKing':
                        MainWindow.owned_champions.append('Wukong')
                        MainWindow.champions_purchased_date['Wukong'] = champion_data[x]['ownership']['rental'][
                            'purchaseDate']
                    else:
                        MainWindow.owned_champions.append(champion_data[x]['alias'])
                        MainWindow.champions_purchased_date[champion_data[x]['alias']] = \
                            champion_data[x]['ownership']['rental']['purchaseDate']
            skin_get = await connector.request('get', '/lol-champions/v1/inventories/' + summoner + '/skins-minimal')
            skin_get = await skin_get.json()
            for x in range(len(skin_get)):
                if skin_get[x]['ownership']['rental']['purchaseDate'] != 0:
                    MainWindow.owned_skin_count += 1
                    MainWindow.owned_skins.append(skin_get[x]['name'])
                    MainWindow.skins_purchased_date[skin_get[x]['name']] = skin_get[x]['ownership']['rental'][
                        'purchaseDate']
        else:
            exit(0)

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