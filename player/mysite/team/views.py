from django.http.response import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def get_html_content(team):
    import requests
    USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    team = team.replace(' ', '+')
    html_content = session.get(f'https://www.google.com/search?q=nba+standing+{team}').text
    return html_content


def home(request):
    nba_team= None
    if 'team' in request.GET:
        team = request.GET.get('team')
        html_content=get_html_content(team)
        print(html_content)
        from bs4 import BeautifulSoup
        soup =BeautifulSoup(html_content, 'html.parser')
        if(team == 'warriors' or team =='suns' or team =='bulls' or team =='nets'):
            nba_team= dict()
            nba_team['name'] = soup.find("div" ,class_= "N0LMJe ellipsisize" ).text
            nba_team['rank'] = soup.find("div", class_= "gDo0uc tgaaSb xL0E7c snctkc").text
            win_lose = soup.find_all("td", class_="e9fBA xkW0Cc snctkc xL0E7c")
            #print(win_lose) # To see which number is the correct one u want to use

        
      
        else:
            #print('2')
            nba_team= dict()
            nba_team['name'] = soup.find("div" ,class_= "N0LMJe ellipsisize" ).text
            rank_list = soup.find_all("div", class_= "gDo0uc tgaaSb snctkc")
            counter=0
            for rank in rank_list:
                counter += 1
                if(counter == 2):
                    nba_team['rank'] = rank.text
            
            win_lose = soup.find_all("td", class_= "e9fBA xkW0Cc snctkc")
            #print(win_list)
           
        #nba_team['rank'] = soup.find("div", class_= "iU5t0d").text
        #nba_team['name'] = soup.find("div" ,class_= "N0LMJe ellipsisize" ).text        
        #nba_team['win'] = soup.find("td", class_="e9fBA xkW0Cc snctkc xL0E7c").text
        print(nba_team)
    return render(request, 'team/home.html', {'nba_team': nba_team})