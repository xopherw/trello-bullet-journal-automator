import requests, json

constant = json.loads(open('trello_params.config', 'r').read())

##--------CLASSES--------##

class trelloURLS:        

    def view_boards_url(self = ''):  return 'https://api.trello.com/1/members/me/boards'

    def view_lists_url(self): return f"https://api.trello.com/1/boards/{self}/lists"

    def view_cards_url(self): return f"https://api.trello.com/1/lists/{self}/cards"

    def create_checklist_url(self):   return f'https://api.trello.com/1/cards/{self}/checklists'

    def create_card_url(self = ''):  return 'https://api.trello.com/1/cards'

    def create_board_url(self = ''): return "https://api.trello.com/1/boards/"

    def create_list_url(self): return f"https://api.trello.com/1/boards/{self}/lists"


##--------FUNCTIONS--------##

# view all existing boards
def viewBoards():
    params = {
    'key': constant['key'],
    'token': constant['token'],
}
    return json.loads(requests.get(trelloURLS.view_boards_url(), params=params).text)

# view all existing lists from a board
def viewLists(idBoard):
    params = {
    'key': constant['key'],
    'token': constant['token'],
}
    return json.loads(requests.get(trelloURLS.view_lists_url(idBoard), params=params).text)

def viewCards(idList):
    params = {
    'key': constant['key'],
    'token': constant['token'],
}
    return json.loads(requests.get(trelloURLS.view_cards_url(idList), params=params).text)

# create board from Trello organization ID, also add name. NOTE: only for Bullter Journal team
def createBoard(name):
    params = {
        'key' : constant['key'],
        'token' : constant['token'],    
        'name' :name,
        'defaultLists' : 'false',
        'idOrganization' : '600062e4ff8dbe380e403bbe',
    }
    requests.post(trelloURLS.create_board_url(), params=params)


# create list from Trello board ID, also add name
def createList(idBoard, name):
    params = {
        'key' : constant['key'],
        'token' : constant['token'],    
        'name' :name,
        'pos' : 'bottom'
    }
    requests.post(trelloURLS.create_list_url(idBoard), params=params)


# create card from Trello list ID, also add name
def createCard(idList, name):
    params = {
        'key' : constant['key'],
        'token' : constant['token'],    
        'idList' : idList,
        'desc' : constant['desc'],
        'name' :name
    }
    requests.post(trelloURLS.create_card_url(), params=params)

# create checklist to a card with card ID, and copy checlist from other checklist ID
def createCheckList(idCard, idChecklistSource):
    params = {
        'key' : constant['key'],
        'token' : constant['token'],    
        'idChecklistSource' : idChecklistSource
    }
    requests.post(trelloURLS.create_checklist_url(idCard), params=params)

# convert month int to month text
def switchMonth(monthNum):
    if(monthNum == 1): return "January"
    elif(monthNum == 2): return "February"
    elif(monthNum == 3): return "March"
    elif(monthNum == 4): return "April"
    elif(monthNum == 5): return "May"
    elif(monthNum == 6): return "June"
    elif(monthNum == 7): return "July"
    elif(monthNum == 8): return "August"
    elif(monthNum == 9): return "September"
    elif(monthNum == 10): return "October"
    elif(monthNum == 11): return "November"
    elif(monthNum == 12): return "December"
    else: return "Error Month number"

def newBoard(date):
    # create new board according to the updated year
    createBoard(str(date.year)) 

    # update board to get board ID, then create list
    idBoard = [i for i in viewBoards() if(i.get('idOrganization') == '600062e4ff8dbe380e403bbe') ][-1].get('id')
    createList(idBoard, switchMonth(date.month))


    # update board to get board ID, then create card
    idList = viewLists(idBoard)[-1].get('id')
    createCard(idList, f"Day {date.day}")

    # update board to get card ID and previous checklist ID in the next line, then create checklist from previous board
    idCard = viewCards(idList)[-1].get('id')
    idChecklist = viewCards(viewLists([i for i in viewBoards() if(i.get('idOrganization') == '600062e4ff8dbe380e403bbe')][-2].get('id'))[-1].get('id'))[-1].get('idChecklists')[-1]
    createCheckList(idCard, idChecklist)

def newList(date):
    idBoard = [i for i in viewBoards() if(i.get('idOrganization') == '600062e4ff8dbe380e403bbe') ][-1].get('id')
    createList(idBoard, switchMonth(date.month))    # create new list of the month

    # update value
    bullet_journal = [{'name': i.get('name'), 'board' : i.get('id'), 'list' : viewLists(i.get('id'))} for i in viewBoards() if(i.get('idOrganization') == '600062e4ff8dbe380e403bbe')]
    
    createCard(bullet_journal[-1].get('list')[1].get('id'), f'Day {date.day}')   # create new Card
    
    #create new list
    createCheckList(viewCards(bullet_journal[-1].get('list')[-1].get('id'))[-1].get('id')  , viewCards(bullet_journal[-1].get('list')[-2].get('id'))[-1].get('idChecklists')[-1])
        
def newCard(date):
    idBoard = [i for i in viewBoards() if(i.get('idOrganization') == '600062e4ff8dbe380e403bbe') ][-1].get('id')
    idList = viewLists(idBoard)[-1].get('id')
    createCard(idList, f"Day {date.day}")

    idCard = viewCards(idList)[-1].get('id')
    idChecklist = viewCards(viewLists([i for i in viewBoards() if(i.get('idOrganization') == '600062e4ff8dbe380e403bbe')][-1].get('id'))[-1].get('id'))[-2].get('idChecklists')[-1]
    createCheckList(idCard, idChecklist)
