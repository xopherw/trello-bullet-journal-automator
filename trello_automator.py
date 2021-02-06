import datetime as dt
from trello_func import *

while(True):
    try:
        # get Bullet Journal team board and id information for quick processing
        bullet_journal = [{'name': i.get('name'), 'board' : i.get('id'), 'list' : viewLists(i.get('id'))} for i in viewBoards() if(i.get('idOrganization') == '600062e4ff8dbe380e403bbe')]
        
        date = dt.datetime.now()  

        if(datex.year == int(bullet_journal[-1].get('name'))):

            if(switchMonth(date.month) != bullet_journal[-1].get('list')[-1].get('name')): 
                newList(date)   
            else: 
                if(date.day != int(viewCards(bullet_journal[-1].get('list')[-1].get('id'))[-1].get('name').strip('Day '))): 
                    newCard(date) 
        else:
            newBoard(date)

        time.sleep(5)
    
    except Exception:
        print("Attempt to reconncet, please hold...")
        time.sleep(5)
