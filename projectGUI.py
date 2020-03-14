import os
from tkinter import *
from tkinter import messagebox,ttk
from PIL import Image,ImageTk
import requests
from bs4 import BeautifulSoup

class Window(Frame):
    def __init__(self, master=None):
        '''The constructor method creates the main window to be used in the application'''
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.tactics = ['4-3-3', '4-2-3-1', '4-4-2', '4-5-1', '5-3-2', '3-5-2', '4-1-2-1-2', '4-3-2-1']
        self.teams = []
        self.home_first_11=[]
        self.away_first_11=[]
        self.home_bench=[]
        self.away_bench=[]
        self.score_counter_1 = 0
        self.score_counter_2=0
        self.main_image = Image.open("Heracles.jpg")
        self.main_photo = ImageTk.PhotoImage(self.main_image)
        '''A dictionary responsible for the latest results functionality in which the key represents the league 
        selected by the user and the value represents a distinctive part of the weblink from soccerway.com for the respective league'''
        self.leagues={'England':'england/premier-league/20192020/regular-season/r53145',
        'Italy':'italy/serie-a/20192020/regular-season/r54890',
        'Spain':'spain/primera-division/20192020/regular-season/r53502',
        'Germany':'germany/bundesliga/20192020/regular-season/r53499',
        'France':'france/ligue-1/20192020/regular-season/r53638',
        'Romania':'romania/liga-i/20192020/relegation-round/r54246'}
        label = Label(image=self.main_photo)
        label.image = self.main_photo
        label.pack()
    def init_window(self):
        '''The init window represents the menu construction of the main app window'''
        self.master.title("FootballApp")
        self.pack(fill=BOTH, expand=1)
        menu = Menu(self.master)
        self.master.config(menu=menu)
        match_configuration = Menu(menu,tearoff=0)
        match_configuration.add_command(label="Create match",command=self.match_configuration)
        match_configuration.add_command(label="Latest results",command=self.latest_results)
        menu.add_cascade(label="Match configuration", menu=match_configuration)
        create = Menu(menu,tearoff=0)
        create.add_command(label="Create teams",command=self.create_teams)
        create.add_command(label="Create players",command=self.create_players)
        menu.add_cascade(label="Create", menu=create)
        menu.add_command(label='Start match',command=self.start_match)
        menu.add_command(label="Exit", command=self.quit_app)
    def quit_app(self):
        '''A method responsible for the exit from app with a message confirmation'''
        answer = messagebox.askyesno('Exit', 'Are you sure you want to exit ?')
        if answer == True:
            self.master.destroy()
        else:
            messagebox.showinfo('Return', 'You are now returned to the main screen')

    def latest_results(self):
        '''A method for construction the window where the user can pick a league and see the latest result from scrapping
        the soccerway.com website'''
        self.last_results=Tk(self.init_window())
        self.last_results.title('Latest results')
        label1=Label(self.last_results,text='Pick a league')
        label1.grid(row=0,column=0,sticky=NW)
        league_selection=[x for x in self.leagues.keys()]
        self.leagues_list=ttk.Combobox(self.last_results,values=league_selection)
        self.leagues_list.grid(row=0,column=1,sticky=NW)
        button1=ttk.Button(self.last_results,text='Show results',command=self.get_results)
        button1.grid(row=1,column=0,sticky=NW)
        self.last_results.geometry('1400x700+0+0')
        self.last_results.configure(background='grey')
        self.last_results.mainloop()

    def get_results(self):
        '''The method for scrapping and processing the data received from soccerway.com
        This represents the command of the button Show results in the latest results window
        the home teams,away teams and score are separately processed in lists and then
        shown in listboxes in the latest results window'''
        country=self.leagues_list.get()
        for key,value in self.leagues.items():
            if key==country:
                site=value
        response = requests.get(f'https://int.soccerway.com/national/{site}/')
        soup = BeautifulSoup(response.text, 'html.parser')
        teams_a_lenght = (len(soup.findAll('table')[0].findAll('td', class_='team team-a')))
        a = 0
        home_team = []
        while a >= 0 and a <= teams_a_lenght - 1:
            team1_elements = soup.findAll('table')[0].findAll('td', class_='team team-a')[a].text.replace('\n','').replace(' ', '')
            a += 1
            home_team.append(team1_elements)
        teams_b_lenght = (len(soup.findAll('table')[0].findAll('td', class_='team team-b')))
        b = 0
        away_team = []
        while b >= 0 and b <= teams_b_lenght - 1:
            team2_elements = soup.findAll('table')[0].findAll('td', class_='team team-b')[b].text.replace('\n','').replace(' ', '')
            b += 1
            away_team.append(team2_elements)
        score_lenght = (len(soup.findAll('table')[0].findAll('td', class_='score-time score')))
        c = 0
        score = []
        while c >= 0 and c <= score_lenght - 1:
            score_elements = soup.findAll('table')[0].findAll('td', class_='score-time score')[c].text.replace('\n','').replace(' ', '')
            c += 1
            score.append(score_elements)
        label_home_team=Label(self.last_results,text='Home team',relief=RAISED,font=("Courier New", 10, "roman"))
        label_home_team.grid(row=0,column=2)
        home_team_listbox=Listbox(self.last_results,width=25,height=15,background='light blue')
        for m in home_team:
            home_team_listbox.insert(END,m)
        home_team_listbox.grid(row=1,column=2,sticky=NE)
        label_score=Label(self.last_results,text='Score',font=("Courier New", 7, "roman"))
        label_score.grid(row=0,column=3)
        score_listbox=Listbox(self.last_results,width=5,height=15,background='green')
        for n in score:
            score_listbox.insert(END,n)
        score_listbox.grid(row=1,column=3)
        label_away_team=Label(self.last_results,text='Away team',relief=RAISED,font=("Courier New", 10, "roman"))
        label_away_team.grid(row=0,column=4)
        away_team_listbox=Listbox(self.last_results,width=25,height=15,background='light blue')
        for o in away_team:
            away_team_listbox.insert(END,o)
        away_team_listbox.grid(row=1,column=4,sticky=NW)
    def match_configuration(self):
        '''A method for creating a match,where the user have to choose a home team,an away team
        and their tactics.This creates a small window with the options for the user'''
        self.match_config=Tk(self.init_window())
        self.match_config.title("Define match")
        label_1=Label(self.match_config,text='Choose home team',width=30,relief=RAISED,font=("Courier New", 10, "roman"))
        label_1.grid(row=0,column=0,sticky=W)
        file = open('teams//teams.txt', "r")
        line = file.readlines()
        self.teams_list = [i.replace('\n', '') for i in line]
        file.close()
        home_team = StringVar()
        self.selectie_1 = ttk.Combobox(self.match_config, textvariable=home_team)
        self.selectie_1.config(values=self.teams_list)
        self.selectie_1.grid(row=0, column=1,sticky=W)
        label_2=Label(self.match_config,text='Choose home tactics',width=30,relief=RAISED,font=("Courier New", 10, "roman"))
        label_2.grid(row=1,column=0,sticky=NW)
        choose_home_tactics=StringVar()
        self.selectie_2 = ttk.Combobox(self.match_config, textvariable=choose_home_tactics)
        self.selectie_2.config(values=self.tactics)
        self.selectie_2.grid(row=1,column=1,sticky=NW)
        label_3 = Label(self.match_config, text='Choose away team', width=30,relief=RAISED,font=("Courier New", 10, "roman"))
        label_3.grid(row=2, column=0,sticky=NW)
        away_team = StringVar()
        self.selectie_3 = ttk.Combobox(self.match_config, textvariable=away_team)
        self.selectie_3.config(values=self.teams_list)
        self.selectie_3.grid(row=2, column=1,sticky=NW)
        label_4 = Label(self.match_config, text='Choose away tactics', width=30,relief=RAISED,font=("Courier New", 10, "roman"))
        label_4.grid(row=3, column=0,sticky=NW)
        choose_away_tactics = StringVar()
        self.selectie_4 = ttk.Combobox(self.match_config, textvariable=choose_away_tactics)
        self.selectie_4.config(values=self.tactics)
        self.selectie_4.grid(row=3, column=1,sticky=NW)
        label_round = Label(self.match_config, text='Select round', width=30,relief=RAISED,font=("Courier New", 10, "roman"))
        label_round.grid(row=4, column=0,sticky=NW)
        round = StringVar()
        self.round = Spinbox(self.match_config, from_=1, to=50, textvariable=round,width=21)
        self.round.grid(row=4, column=1,sticky=NW)
        #the button 'confirm and save' have to be clicked after the fields above are completed and
        button_1=Button(self.match_config,text='Confirm and save',command=self.save_match,width=20,background='green',relief=SOLID)
        button_1.grid(row=5,column=0,sticky=W)
        #this button is responsible for taking the user to the window assign players to first 11 or to bench
        button_2=Button(self.match_config,text='Go to lineup',command=self.assign_players,width=15,background='light green',relief=SOLID)
        button_2.grid(row=5,column=0,sticky=E)
        button_exit = Button(self.match_config, text="Exit",background='red',width=27,command=self.match_config.destroy)
        button_exit.grid(row=0, column=3,sticky=E)
        self.match_config.geometry("600x200+200+200")
        self.match_config.configure(background="grey")
        self.match_config.mainloop()

    def save_match(self):
        '''This function saves a folder in the matches folder with the name of the home team-away team'''
        if self.selectie_1.get() and self.selectie_2.get() and self.selectie_3.get() and self.selectie_4.get() and self.round.get() !='':
            try:
                os.mkdir(f'matches\\{self.selectie_1.get()} - {self.selectie_3.get()}')

            except OSError:
                messagebox.showinfo('Warning','The match is already created')
            else:
                messagebox.showinfo('Done','Match created')
        else:
            messagebox.showinfo('Warning', 'Check the if you have correctly completed all the required fields')


    def assign_players(self):
        '''This method creates a new window for the user where he can pick for both teams the first 11 and the bench
        players after the go to lineup button is pressed'''
        self.player_assignation=Tk()
        self.player_assignation.title(f'{self.selectie_1.get()} - {self.selectie_3.get()}')
        label_1 = Label(self.player_assignation, text=f'{self.selectie_1.get()}', width=22,relief=RAISED,font=("Courier New", 10, "roman"))
        label_1.grid(row=1, column=0,sticky=W)
        label_2 = Label(self.player_assignation, text=f'{self.selectie_2.get()}', width=10,relief=RAISED,font=("Courier New", 10, "roman"))
        label_2.grid(row=1, column=1,sticky=W)
        label_3 = Label(self.player_assignation, text='Select player', width=20,relief=RAISED,font=("Courier New", 10, "roman"))
        label_3.grid(row=2, column=0,sticky=W)
        file_1 = open(f'teams\\{self.selectie_1.get()}\\{self.selectie_1.get()}.txt', "r")
        line_1 = file_1.readlines()
        self.players_list_h = [i.replace('\n', '') for i in line_1]
        file_1.close()
        first11_h = StringVar()
        self.first11_h = ttk.Combobox(self.player_assignation, textvariable=first11_h)
        self.first11_h.config(values=self.players_list_h)
        self.first11_h.grid(row=2, column=1,sticky=W)
        button_first11_h=Button(self.player_assignation,text="Add to first 11",command=self.create_first11_h,bg='green',relief=SOLID)
        button_first11_h.grid(row=5,column=0,sticky=W)
        button_bench_h =Button(self.player_assignation, text="Add to bench",command=self.create_bench_h,bg='light green',relief=SOLID)
        button_bench_h.grid(row=5, column=1,sticky=W)
        remove_button_h =Button(self.player_assignation, text='Remove', command=self.remove_home_players,bg='red',relief=SOLID)
        remove_button_h.grid(row=12, column=0,sticky=W)
        remove_button_h =Button(self.player_assignation, text='Remove',command=self.remove_home_bench,bg='red',relief=SOLID)
        remove_button_h.grid(row=12, column=1,sticky=W)
        label_5 = Label(self.player_assignation, text=f'{self.selectie_3.get()}', width=22,relief=RAISED,font=("Courier New", 10, "roman"))
        label_5.grid(row=1, column=2,sticky=W)
        label_6 = Label(self.player_assignation, text=f'{self.selectie_4.get()}', width=10,relief=RAISED,font=("Courier New", 10, "roman"))
        label_6.grid(row=1, column=3,sticky=W)
        label_7 = Label(self.player_assignation, text='Select player', width=20,relief=RAISED,font=("Courier New", 10, "roman"))
        label_7.grid(row=2, column=2,sticky=W)
        file_2 = open(f'teams\\{self.selectie_3.get()}\\{self.selectie_3.get()}.txt', "r")
        line_2 = file_2.readlines()
        self.players_list_a = [i.replace('\n', '') for i in line_2]
        file_2.close()
        first11_a = StringVar()
        self.home_players_list=Listbox(self.player_assignation,height=20,selectmode=SINGLE,background='green')
        self.home_players_list.grid(row=10,column=0,sticky=W)
        self.home_bench_list = Listbox(self.player_assignation,height=20,selectmode=SINGLE,background='light green')
        self.home_bench_list.grid(row=10, column=1,sticky=W)
        self.away_players_list = Listbox(self.player_assignation, height=20,selectmode=SINGLE,background='green')
        self.away_players_list.grid(row=10, column=2,sticky=W)
        self.away_bench_list = Listbox(self.player_assignation, height=20,selectmode=SINGLE,background='light green')
        self.away_bench_list.grid(row=10, column=3,sticky=W)
        self.first11_a = ttk.Combobox(self.player_assignation, textvariable=first11_a)
        self.first11_a.config(values=self.players_list_a)
        self.first11_a.grid(row=2, column=3,sticky=W)
        button_first11_h =Button(self.player_assignation, text="Add to first 11", command=self.create_first11_a,bg='green',relief=SOLID)
        button_first11_h.grid(row=5, column=2,sticky=W)
        button_bench_h =Button(self.player_assignation, text="Add to bench", command=self.create_bench_a,bg='light green',relief=SOLID)
        button_bench_h.grid(row=5, column=3,sticky=W)
        remove_button_a =Button(self.player_assignation, text='Remove',command=self.remove_away_players,bg='red',relief=SOLID)
        remove_button_a.grid(row=12, column=2,sticky=W)
        remove_button_a =Button(self.player_assignation, text='Remove',command=self.remove_away_bench,bg='red',relief=SOLID)
        remove_button_a.grid(row=12, column=3,sticky=W)
        submit_home_button=Button(self.player_assignation,text='Submit home team',command=self.home_players_submit,relief=SOLID,bg='light blue')
        submit_home_button.grid(row=14,column=0,sticky=E)
        submit_away_button=Button(self.player_assignation,text='Submit away team',command=self.away_players_submit,relief=SOLID,bg='light blue')
        submit_away_button.grid(row=14, column=2,sticky=E)
        button_finish =Button(self.player_assignation, text="Exit",command=self.player_assignation.destroy,bg='red',width=20,relief=SOLID)
        button_finish.grid(row=15,column=5)
        self.player_assignation.geometry("800x500+250+150")
        self.player_assignation.configure(background="grey")
        self.player_assignation.mainloop()
    def home_players_submit(self):
        '''This method confirms the home team lineup and bench and creates 2 .txt files with the players selected
        The files will be saved locally on the user computer in the match folder and will be used in the match start.
        Every player name is saved on a different line.The reason of creating the files is that you can close the app
        and still have the lineup and bench players to be used in the match start'''
        confirmation=messagebox.askyesno('Confirm','Are you sure you want to submit the home team?')
        if confirmation==True:
            self.home_first_11=self.home_players_list.get(0,END)
            if len(self.home_first_11) == 11:
                file_home_team=open(f'matches\\{self.selectie_1.get()} - {self.selectie_3.get()}\\A-{self.selectie_1.get()} lineup.txt', "a")
                for i in self.home_first_11:
                    file_home_team.write(f'{i}\n')
                file_home_team.close()
                self.home_bench = self.home_bench_list.get(0, END)
                file_home_team2=open(f'matches\\{self.selectie_1.get()} - {self.selectie_3.get()}\\A-{self.selectie_1.get()} substitutes.txt', "a")
                for j in self.home_bench:
                    file_home_team2.write(f'{j}\n')
                file_home_team2.close()
            else:
                messagebox.showinfo('Warning','You do not have 11 players in the lineup')
        else:
            messagebox.showinfo('Return','You are now returned to the player assigning process')


    def away_players_submit(self):
        '''Identical with the method above plus a creation of a Report file to be used for submitting a match report'''
        confirmation=messagebox.askyesno('Confirm','Are you sure you want to submit the away team?')
        if confirmation==True:
            self.away_first_11 = self.away_players_list.get(0, END)
            if len(self.away_first_11) == 11:
                file_away_team = open(f'matches\\{self.selectie_1.get()} - {self.selectie_3.get()}\\D-{self.selectie_3.get()} lineup.txt', "a")
                for i in self.away_first_11:
                    file_away_team.write(f'{i}\n')
                file_away_team.close()
                self.away_bench = self.away_bench_list.get(0, END)
                file_away_team2=open(f'matches\\{self.selectie_1.get()} - {self.selectie_3.get()}\\D-{self.selectie_3.get()} substitutes.txt', "a")
                for j in self.away_bench:
                    file_away_team2.write(f'{j}\n')
                file_away_team2.close()
                file = open(f'matches\\{self.selectie_1.get()} - {self.selectie_3.get()}\\Report.txt', "w")
                file.close()
            else:
                messagebox.showinfo('Warning', 'You do not have 11 players in the lineup')
        else:
            messagebox.showinfo('Return', 'You are now returned to the player assigning process')


    def create_first11_h(self):
        '''This method inserts user players selection in the home team first 11 listbox when pressing the add to first 11
        button'''
        if self.first11_h !='':
            self.home_players_list.insert(END, self.first11_h.get())
        else:
            messagebox.showinfo('Incorrect','Player not selected')


    def create_bench_h(self):
        '''This method inserts user players selection in the home team bench listbox when pressing the add to bench
        button'''
        if self.first11_h != '':
            self.home_bench_list.insert(END,self.first11_h.get())
        else:
            messagebox.showinfo('Incorrect', 'Player not selected')

    def create_first11_a(self):
        '''This method inserts user players selection in the away team first 11 listbox'''
        if self.first11_a !='':
            self.away_players_list.insert(END, self.first11_a.get())
        else:
            messagebox.showinfo('Incorrect','Player not selected')

    def create_bench_a(self):
        '''This method inserts user players selection in the away team bench listbox'''
        if self.first11_a != '':
            self.away_bench_list.insert(END,self.first11_a.get())
        else:
            messagebox.showinfo('Incorrect', 'Player not selected')

    def remove_home_players(self):
        '''The next methods are for removing players from the listboxes in case the user inserts wrong players'''
        return self.home_players_list.delete(ANCHOR)

    def remove_home_bench(self):
        return self.home_bench_list.delete(ANCHOR)

    def remove_away_players(self):
        return self.away_players_list.delete(ANCHOR)

    def remove_away_bench(self):
        return self.away_bench_list.delete(ANCHOR)

    def create_teams(self):
        '''This method opens a new window for a user team creation'''
        self.teams_creation=Tk()
        self.teams_creation.title('Create team')
        label_1=Label(self.teams_creation,text="Team's name",width=20,relief=RAISED,font=("Courier New", 10, "roman"))
        label_1.grid(row=0,column=0,sticky=W)
        self.team_entry=Entry(self.teams_creation,width=30)
        self.team_entry.grid(row=0,column=1,sticky=W)
        label_2=Label(self.teams_creation,text='Select league',width=20,relief=RAISED,font=("Courier New", 10, "roman"))
        label_2.grid(row=1,column=0,sticky=W)
        league_names=['Premier League','Liga 1','Bundesliga','Primera Division','Serie A','Ligue 1']
        self.league_selection=ttk.Combobox(self.teams_creation,values=league_names,width=27)
        self.league_selection.grid(row=1,column=1,sticky=W)
        button_1 =Button(self.teams_creation, text='Add this team',command=self.save_team,bg='green',relief=SOLID)
        button_1.grid(row=3,column=0,sticky=W)
        label_3 = Label(self.teams_creation, text="Stadium's name", width=20, relief=RAISED,
                        font=("Courier New", 10, "roman"))
        label_3.grid(row=2, column=0, sticky=W)
        self.field_entry = Entry(self.teams_creation, width=30)
        self.field_entry.grid(row=2, column=1, sticky=W)
        self.teams_creation.geometry("450x200+400+200")
        self.teams_creation.configure(background='grey')
        self.teams_creation.mainloop()
    def save_team(self):
        '''This method saves the user new created team as a folder in the teams folder and also as a new line in the
        teams.txt file'''
        if self.team_entry.get() != '' and self.field_entry.get() !='':
            try:
                os.mkdir(f'teams\\{self.team_entry.get()}')
                file = open(f'teams\\teams.txt', "a")
                file.write(f'{self.team_entry.get()}\n')
                file.close()
                file_2=open(f'teams\\{self.team_entry.get()}\\{self.team_entry.get()}.txt',"a")
                file_2.close()
                self.teams.append(self.team_entry.get())
                messagebox.showinfo('Added',f'{self.team_entry.get()} was added')
                self.team_entry.delete(0,'end')
            except OSError:
                messagebox.showinfo('Exists','The team is already created')
            else:
                messagebox.showinfo('Confirm','The team and its directory successfully created')
        else:
            messagebox.showinfo('Nope','Some fields incompleted')

    def create_players(self):
        '''This method opens a new window for a user player creation'''
        self.player_creation=Tk()
        self.player_creation.title("Create player")
        label_1=Label(self.player_creation,text='Select team',width=30,relief=RAISED,font=("Courier New", 10, "roman"))
        label_1.grid(row=0,column=0,sticky=W)
        file = open('teams//teams.txt', "r")
        line = file.readlines()
        self.teams_list = [i.replace('\n', '') for i in line]
        file.close()
        created_teams = StringVar()
        self.player_creation_team = ttk.Combobox(self.player_creation, textvariable=created_teams,width=30)
        self.player_creation_team.config(values=self.teams_list)
        self.player_creation_team.grid(row=0, column=1)
        label_2=Label(self.player_creation,text="Insert player name",width=30,relief=RAISED,font=("Courier New", 10, "roman"))
        label_2.grid(row=1,column=0,sticky=W)
        self.player_team_entry = Entry(self.player_creation, width=33)
        self.player_team_entry.grid(row=1, column=1,sticky=W)
        file2 = open('teams//nationalities.txt', "r")
        line2 = file2.readlines()
        self.nationalities_list = [j.replace('\n', '') for j in line2]
        file2.close()
        label_3=Label(self.player_creation,text='Select nationality',width=30,relief=RAISED,font=("Courier New", 10, "roman"))
        label_3.grid(row=2,column=0,sticky=W)
        nationalities = StringVar()
        self.nationality=ttk.Combobox(self.player_creation,values=self.nationalities_list,textvariable=nationalities,width=30)
        self.nationality.grid(row=2,column=1,sticky=W)
        button_1 = Button(self.player_creation, text='Add this player',command=self.save_player,bg='green',relief=SOLID)
        button_1.grid(row=3, column=0,sticky=W)
        self.player_creation.geometry("550x200+400+200")
        self.player_creation.configure(background='grey')
        self.player_creation.mainloop()

    def save_player(self):
        '''This method saves the user new created player in a text file which will be placed in the team's folder'''
        if self.player_team_entry.get() != '' and self.player_creation_team.get() !='' and self.nationality.get() != '':
            file = open(f'teams\\{self.player_creation_team.get()}\\{self.player_creation_team.get()}.txt', "a")
            file.write(f'{self.player_team_entry.get()}\n')
            file.close()
            messagebox.showinfo('Added', f'{self.player_team_entry.get()} was added')
            self.player_team_entry.delete(0, 'end')
        else:
            messagebox.showinfo('Warning', 'You have uncompleted fields')

    def start_match(self):
        '''This method is responsible for starting the match and adding the match events.
        This opens a new window from where the user can select the match created before with the players placed on the
        first 11 listbox and bench listbox.If the lineup hasn't been configured this functionality can't be used'''
        self.start=Tk()
        self.start.title('Match')
        label_1=Label(self.start,text='Choose a match',relief=SUNKEN)
        label_1.grid(row=0,column=0,sticky=W)
        self.buttonconf=Button(self.start,text='Confirm',command=self.confirm)
        self.buttonconf.grid(row=0,column=2,sticky=W)
        created_matches = StringVar()
        matches_list=os.listdir('matches')
        self.match_select = ttk.Combobox(self.start, textvariable=created_matches, width=40)
        self.match_select.configure(values=matches_list)
        self.match_select.grid(row=0, column=1,sticky=W)
        self.start.configure(background='grey')
        self.start.geometry('1400x700+0+0')
        self.start.mainloop()
    def confirm(self):
        '''This method creates the listboxes,the buttons and all the other functionalities to be used in the match adding
        events after the user confirms the match selection via Confirm button
        The listboxes are populated from the text files created before,the labels are automatically named after the match
        folder and the teams folders names '''
        self.match_select.configure(state=DISABLED,width=50)
        self.match_select.grid(row=0,column=0,columnspan=3)
        self.buttonconf.configure(state=DISABLED,text='',bg='grey')
        self.buttonconf.grid(row=0, column=3)
        teams=os.listdir(f'matches\\{self.match_select.get()}')
        teams2= [i.replace('.txt', '') for i in teams]
        self.label_team_f1 = Label(self.start, text=f'{teams2[0][2:5].upper()} FIRST 11',relief=RAISED,font=("Courier New", 10, "roman"))
        self.label_team_f1.grid(row=1,column=0,sticky=W)
        file1=open(f'matches\\{self.match_select.get()}\\{teams[0]}','r')
        line1 = file1.readlines()
        team1_line = [j.replace('\n', '') for j in line1]
        file1.close()
        self.start_list_f1 = Listbox(self.start, height=15,background='light green',exportselection=0,activestyle=NONE)
        for k in team1_line:
            self.start_list_f1.insert(0,k)
        self.start_list_f1.grid(row=2, column=0,sticky=W)

        self.label_team_s1 = Label(self.start, text=f'{teams2[1][2:5].upper()} BENCH',relief=RAISED,font=("Courier New", 10, "roman"))
        self.label_team_s1.grid(row=4, column=0,sticky=W)
        file2 = open(f'matches\\{self.match_select.get()}\\{teams[1]}', 'r')
        line2 = file2.readlines()
        team2_line = [j.replace('\n', '') for j in line2]
        file2.close()
        self.start_list_s1 = Listbox(self.start, height=15,background='light blue',exportselection=0,activestyle=NONE)
        for k in team2_line:
            self.start_list_s1.insert(0, k)
        self.start_list_s1.grid(row=5, column=0,sticky=W)

        self.match_events_label1 = Label(self.start, text='Team events',relief=RAISED,font=("Courier New", 10, "roman"))
        self.match_events_label1.grid(row=1, column=1,sticky=W)
        self.match_events_listbox1 = Listbox(self.start, height=15, exportselection=0, background='white',width=50)
        self.match_events_listbox1.grid(row=2, column=1,sticky=W)

        button1 = Button(self.start, text='Add event', bg='green',command=self.confirm_event_left,width=21,relief=SOLID)
        button1.grid(row=3, column=1,sticky=W)
        button1_remove=Button(self.start,text='Remove event',bg='red',command=self.remove_event_left,width=20,relief=SOLID)
        button1_remove.grid(row=3,column=1,sticky=E)

        events_list1=['GOAL','ASSIST','SHOT ON TARGET','SHOT OFF TARGET','YELLOW CARD','RED CARD','CORNER KICK']
        self.label_event1=Label(self.start,text='Pick an event',relief=RAISED,font=("Courier New", 10, "roman"))
        self.label_event1.grid(row=1,column=2,sticky=W)
        self.events_listbox1=Listbox(self.start,height=15,exportselection=0,activestyle=NONE,background='green')
        for m in events_list1:
            self.events_listbox1.insert(0,m)
        self.events_listbox1.grid(row=2,column=2,sticky=W)

        self.label_team_f2 = Label(self.start, text=f'{teams2[2][2:5].upper()} FIRST 11',relief=RAISED,font=("Courier New", 10, "roman"))
        self.label_team_f2.grid(row=1, column=3,sticky=W)
        file3 = open(f'matches\\{self.match_select.get()}\\{teams[2]}', 'r')
        line3 = file3.readlines()
        team3_line = [j.replace('\n', '') for j in line3]
        file3.close()
        self.start_list_f2 = Listbox(self.start, height=15, background='light green', exportselection=0,activestyle=NONE)
        for k in team3_line:
            self.start_list_f2.insert(0, k)
        self.start_list_f2.grid(row=2, column=3,sticky=W)

        self.label_team_s2 = Label(self.start, text=f'{teams2[3][2:5].upper()} BENCH',relief=RAISED,font=("Courier New", 10, "roman"))
        self.label_team_s2.grid(row=4, column=3,sticky=W)
        file4 = open(f'matches\\{self.match_select.get()}\\{teams[3]}', 'r')
        line4 = file4.readlines()
        team4_line = [j.replace('\n', '') for j in line4]
        file4.close()
        self.start_list_s2 = Listbox(self.start, height=15, background='light blue', exportselection=0)
        for k in team4_line:
            self.start_list_s2.insert(0, k)
        self.start_list_s2.grid(row=5, column=3,sticky=W)

        self.match_events_label2 = Label(self.start, text='Team events',relief=RAISED,font=("Courier New", 10, "roman"))
        self.match_events_label2.grid(row=1, column=4,sticky=W)
        self.match_events_listbox2 = Listbox(self.start, height=15, exportselection=0, background='white',width=50)
        self.match_events_listbox2.grid(row=2, column=4,sticky=W)

        button2 = Button(self.start, text='Add event', bg='green',command=self.confirm_event_right,width=21,relief=SOLID)
        button2.grid(row=3, column=4,sticky=W)
        button2_remove=Button(self.start,text='Remove event',bg='red',command=self.remove_event_right,width=20,relief=SOLID)
        button2_remove.grid(row=3,column=4,sticky=E)

        self.match_cronology_label=Label(self.start,text='Match cronology',relief=RAISED,font=("Courier New", 10, "roman"))
        self.match_cronology_label.grid(row=1,column=5,sticky=W)
        self.match_cronology_listbox=Listbox(self.start,height=15,width=60,background='white')
        self.match_cronology_listbox.grid(row=2,column=5,sticky=W)

        button_make_sub_left=Button(self.start,text='Make sub',bg='green',command=self.make_sub_left,width=16,relief=RAISED)
        button_make_sub_left.grid(row=6,column=0,sticky=W)

        button_make_sub_right=Button(self.start,text='Make sub',bg='green',command=self.make_sub_right,width=16,relief=RAISED)
        button_make_sub_right.grid(row=6,column=3,sticky=W)

        label_entry_time=Label(self.start,text='Insert event time',relief=SOLID,font=("Courier New", 9, "roman"),bg='green')
        label_entry_time.grid(row=3,column=2)
        self.entry_time=Entry(self.start,width=20,relief=SUNKEN,bg='green')
        self.entry_time.grid(row=4,column=2,sticky=N)
        self.score = os.listdir(f'matches\\{self.match_select.get()}')
        self.score2 = [i.replace('lineup.txt', '') for i in self.score]
        self.label_score_1 = Label(self.start, text=f'{self.match_select.get()} {self.score_counter_1} - {self.score_counter_2} ')
        self.label_score_1.configure(relief=RAISED,font=("Courier New", 10, "bold"),bg='green')
        self.label_score_1.grid(row=0, column=5,sticky = W)
        button_submit=Button(self.start,text='Submit report',command=self.submit_report,bg='blue',relief=SOLID)
        button_submit.grid(row=3,column=5,sticky=W)
    def update_score(self):
        '''This method updates the score in case the user adds a goal event'''
        self.label_score_up = Label(self.start, text=f'{self.match_select.get()} {self.score_counter_1} - {self.score_counter_2} ')
        self.label_score_up.configure(relief=RAISED, font=("Courier New", 10, "bold"),bg='green')
        self.label_score_up.grid(row=0, column=5,sticky = W)

    def confirm_event_left(self):
        '''This method inserts the home team event in the team event listbox and match cronology listbox when
        Add event button under the home team is clicked'''
        answer=messagebox.askyesno('Warning','Are you sure you want to add this event ?')
        if answer==True:
            if self.events_listbox1.get(ANCHOR) !='' and self.start_list_f1.get(ANCHOR) !='' and self.entry_time.get() !='':
                self.match_event1=self.events_listbox1.get(ANCHOR)+' '+self.start_list_f1.get(ANCHOR)+ ' ' +  ' MIN'+'->'+self.entry_time.get()
                self.match_events_listbox1.insert(0,self.match_event1)
                self.cronology_1 = ' MIN' + '->' + self.entry_time.get() + ' '+ self.events_listbox1.get(ANCHOR) + ' ' + self.start_list_f1.get(ANCHOR)
                self.match_cronology_listbox.insert(0, self.cronology_1)
                self.events_listbox1.selection_clear(0,END)
                self.start_list_f1.selection_clear(0,END)
                self.entry_time.delete(0, 'end')
                if self.match_event1[0:4] == 'GOAL':
                    self.score_counter_1 += 1
                    self.update_score()


            else:
                messagebox.showinfo('Warning','You did not select an event,a player and the time')
        else:
            messagebox.showinfo('Return','You are now returned to event selection')


    def confirm_event_right(self):
        '''This method inserts the away team event in the team event listbox and match cronology listbox when
        Add event button under the away team is clicked'''
        answer=messagebox.askyesno('Warning','Are you sure you want to add this event ?')
        if answer==True:
            if self.events_listbox1.get(ANCHOR) !='' and self.start_list_f2.get(ANCHOR) !='' and self.entry_time.get() !='':
                self.match_event2 = self.events_listbox1.get(ANCHOR) + ' '+self.start_list_f2.get(ANCHOR) + ' ' +  ' MIN'+'->'+self.entry_time.get()
                self.match_events_listbox2.insert(0,self.match_event2)
                self.cronology_2=' MIN'+'->'+self.entry_time.get() + ' '+self.events_listbox1.get(ANCHOR) + ' '+self.start_list_f2.get(ANCHOR)
                self.match_cronology_listbox.insert(0, self.cronology_2)
                self.events_listbox1.selection_clear(0,END)
                self.start_list_f2.selection_clear(0,END)
                self.entry_time.delete(0, 'end')
                if self.match_event2[0:4] == 'GOAL':
                    self.score_counter_2 += 1
                    self.update_score()

            else:
                messagebox.showinfo('Warning','You did not select an event,a player and the time')
        else:
            messagebox.showinfo('Return','You are now returned to event selection')

    def remove_event_left(self):
        '''This method removes a selected event from the home team events listbox and match cronology listbox when the remove
        button under the home team is clicked and updates the score in case the event is a goal event'''
        event_deleted = self.match_events_listbox1.get(ANCHOR)
        self.match_events_listbox1.delete(ANCHOR)
        self.match_cronology_listbox.delete(ANCHOR)
        if event_deleted[0:4]=='GOAL':
            self.score_counter_1 -=1
            self.update_score()
    def remove_event_right(self):
        '''This method removes a selected event from the away team events listbox and match cronology listbox when the remove
        button under the away team is clicked and updates the score in case the event is a goal event'''
        event_deleted = self.match_events_listbox2.get(ANCHOR)
        self.match_events_listbox2.delete(ANCHOR)
        self.match_cronology_listbox.delete(ANCHOR)
        if event_deleted[0:4]=='GOAL':
            self.score_counter_2 -=1
            self.update_score()
    def make_sub_left(self):
        '''This method creates a substitution event and adds it to the team events and match cronology listboxes
        and also replace selected players in the first 11 and bench listboxes when the button make sub is clicked'''
        if self.start_list_f1.get(ANCHOR) !='' and self.start_list_s1.get(ANCHOR) !='' and self.entry_time.get() !='':
            player_out=self.start_list_f1.get(ANCHOR)
            player_in=self.start_list_s1.get(ANCHOR)
            self.start_list_f1.insert(END,player_in)
            self.start_list_s1.insert(END,player_out)
            self.start_list_f1.delete(ANCHOR)
            self.start_list_s1.delete(ANCHOR)
            substitution='OUT' + ' '+f'{player_out}'+ '<->'+ 'IN'+' '+f'{player_in}'+ ' MIN'+'->'+self.entry_time.get()
            sub_cron=' MIN'+'->'+self.entry_time.get()+' '+'OUT' + ' '+f'{player_out}'+ '<->'+ 'IN'+' '+f'{player_in}'
            self.match_events_listbox1.insert(0,substitution)
            self.match_cronology_listbox.insert(0, sub_cron)
            self.entry_time.delete(0, 'end')
    def make_sub_right(self):
        '''The same functionality as the above method but for the away team'''
        if self.start_list_f2.get(ANCHOR) !='' and self.start_list_s2.get(ANCHOR) !='' and self.entry_time.get() !='':
            player_out=self.start_list_f2.get(ANCHOR)
            player_in=self.start_list_s2.get(ANCHOR)
            self.start_list_f2.insert(END,player_in)
            self.start_list_s2.insert(END,player_out)
            self.start_list_f2.delete(ANCHOR)
            self.start_list_s2.delete(ANCHOR)
            substitution='OUT' + ' '+f'{player_out}'+ '<->'+ 'IN'+' '+f'{player_in}'+ ' MIN'+'->'+self.entry_time.get()
            sub_cron = ' MIN' + '->' + self.entry_time.get() + ' ' + 'OUT' + ' ' + f'{player_out}' + '<->' + 'IN' + ' ' + f'{player_in}'
            self.match_events_listbox2.insert(0,substitution)
            self.match_cronology_listbox.insert(0, sub_cron)
            self.entry_time.delete(0, 'end')

    def submit_report(self):
        '''This method inserts the match score and the chronological order of the match events in the Report text file
        when the blue button Submit report is pressed'''
        answer=messagebox.askyesno('Submit report','Are you sure you want to submit the match report?')
        if answer==True:
            self.match_cronology=list(self.match_cronology_listbox.get(0,END))
            self.match_cronology.sort()
            file = open(f'matches\\{self.match_select.get()}\\Report.txt', "w")
            file.write(f'{self.match_select.get()} {self.score_counter_1} - {self.score_counter_2}\n\n')
            for i in self.match_cronology:
                file.write(f'{i}\n')
            file.close()
        else:
            messagebox.showinfo('Return','You are now returned to the match')

root = Tk()
root.geometry("1400x700+0+0")
app = Window(root)
root.mainloop()


