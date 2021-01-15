import time, datetime as dt
from trello_func import *

while(True):
    
    # get Bullet Journal team board and id information for quick processing
    bullet_journal = [{'name': i.get('name'), 'board' : i.get('id'), 'list' : viewLists(i.get('id'))} for i in viewBoards() if(i.get('idOrganization') == 'YOUR_TRELLO_TEAM_ID_FROM_TRELLO_API')]
    
    date = dt.datetime.now()  

    if(date.year == int(bullet_journal[-1].get('name'))):

        if(switchMonth(date.month) != bullet_journal[-1].get('list')[-1].get('name')): 
            newList(date)
            newCard(date)
        else: 
            if(date.day != int(viewCards(bullet_journal[-1].get('list')[-1].get('id'))[-1].get('name').strip('Day '))): 
                newCard(date)

    else:
        newBoard(date)

    time.sleep(10) #NOTE: YOU CAN SET ANY TIME INTERVAL YOU WANT
