#Code by Kh4ru
import os
import tkinter as gui
import requests,webbrowser as web
from bs4 import BeautifulSoup
class Jeu:
  def __init__(self,title,region,url):
    self.title = title
    self.region = region
    self.url = url
links = []
games = []
jeux = []
regions = ["china", "europe", "north-america", "taiwan","japan","korea"]
base_dir = os.path.dirname(os.path.realpath(__file__))
def Search(game):
  idr = 0
  target = "green bold nospace"
  reponse = requests.get(f"https://hshop.erista.me/search/results?e=videos.*%2Cthemes.*%2Cdlc.*%2Cupdates.*%2Cvirtual-console.*%2Cdsiware.*%2Cextras.*&q={game}")
  data = reponse.text
  html = BeautifulSoup(data, "html.parser")
  links_el = html.find_all(class_="list-entry block-link")
  games_el = html.find_all(class_=target)
  types_el = html.find_all("h4")
  for link in links_el:
    href = link["href"]
    links.append(href)
  for game in games_el:
    games.append(game.get_text(strip=True))
  for type in types_el:
    spans = type.find_all("span") 
    for span in spans:
      if span:
        span_text = span.get_text(strip=True).lower()
        region = spans[1].get_text(strip=True).lower()
        if(region in regions):
          if ("games" in span_text):
            if (idr < len(games) and idr < len(links)):
              new_game = Jeu(games[idr],region,"https://hshop.erista.me"+links[idr])
              jeux.append(new_game)
        idr += 1
    else:
      pass
def Search_gui():
    global games,jeux,links
    games = []
    jeux = []
    links = []
  
    for widget in window.winfo_children():
        if(isinstance(widget,gui.Frame) or isinstance(widget,gui.Label) and widget.cget("text") == "No results found :(" or widget.cget("text") == "Enter a game name to begin"):
            widget.destroy()
    Search(searchbar.get())
    for jeu in jeux:
        frame = gui.Frame(window,bg="grey")
        frame.pack(side="top",pady=5)
        download = gui.Button(frame,text="Download",command= lambda jeu=jeu:Download(jeu),bg="white")
        title = gui.Label(frame,text=jeu.title+" : "+jeu.region.upper(),bg="black",fg="white")
        title.pack(side="left")
        download.pack(side="right")
    if(jeux == []):
        message = gui.Label(window,text="No results found :(")
        message.pack(side="top")
def Download(jeu):
   download_page = requests.get(jeu.url)
   data = BeautifulSoup(download_page.text,"html.parser")
   button = data.find_all("a")
   for btn in button:
      if("btn-c3" in btn.get("class",[])):
         download_link = btn["href"]
         web.open(download_link) 
window = gui.Tk()
window.geometry("800x500")
window.configure(bg="black")
window.title("Crusoe Crawler for 3DS")
icon = gui.PhotoImage(file=base_dir+"/icon.png")
window.iconphoto(True,icon)
crusoe_icon = gui.PhotoImage(file=base_dir+"/icon_x64.png")
crusoe = gui.Label(window,image=crusoe_icon,bg="black")
crusoe.place(relx=0.5, rely=0.5, anchor="center")
searchbar = gui.Entry(window,fg="black",bg="white")
search_btn = gui.Button(window,command=Search_gui,text="Search",fg="black",bg="white")
powered = gui.Label(window,text="Powered by Hshop",bg="black",fg="white")
powered.place(relx=0.0, rely=1.0, anchor="sw")
credits = gui.Label(window,text="Developped by @Kh4ru",bg="black",fg="white")
version = gui.Label(window,text="Enter a game name to begin",bg="black",fg="white")
information = gui.Label(window,text="Version: 1.0",bg="black",fg="white")
information.place(relx=0.5, rely=0.59, anchor="center")
version.place(relx=0.5, rely=0.64, anchor="center")
credits.place(relx=1.0, rely=1.0, anchor="se")
search_btn.pack(side="bottom")
searchbar.pack(side="bottom")
window.mainloop()