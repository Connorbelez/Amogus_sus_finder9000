
from pprint import pprint

colours = ['red','blue','green','orange','yellow','brown','pink']

def load_map(file_path): 
    mp_loaded = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip().split(':')
            key = line[0]
            val = line[1]
            val_list = val.strip().split(',')
            for i in range(len(val_list)): #this strips spaces from each list element
                val_list[i] = val_list[i].strip()
            mp_loaded[key] = val_list
    return mp_loaded

def simplify_testimony(chat,rooms):
    #case 1: has word 'voted'
    #case 2: refrences room, no colour = self declaration
    #case 3: refrecnes room and colour, accusation
    #case 4: no room or colour = null
    #check for 'voted'
    if 'voted' in chat:
        x = chat.strip()
        return x
    #check if a room is refrenced
    else:    # i hate this code but it works... must be a better way.
        for room in rooms:
            x = chat.find(room)
            if x != -1:
                y = chat.split()
                check = " ".join(y[1:])
                #check for colours   
                #all of this code is prbaby unecessary
                for colour in colours:
                    if check.find(colour) != -1:
                        self_report = False
                        break
                    else:
                        self_report = True
                        
                if self_report == False:
                    report = f'{y[0]} {colour} in {room}'
                    return report
                else:
                    col = y[0].strip(':')
                    report = f'{col}: {col} in {room}'
                    return report
    return ''


def load_chat_log(filename,rooms):
    chatter =[]
    with open(filename,"r") as f:
        for line in f:
            x = simplify_testimony(line,rooms)
            if x != '':
                chatter.append(x)
    return chatter

def tally_votes(chat_log):
    votes = {
        "red" : 0,
        "blue" : 0,
        "green" : 0,
        "orange" : 0,
        "pink" : 0,
        "yellow" : 0,
        "brown" : 0,
        "purple" : 0,
        "skip": 0
    }
    for chat in chat_log:
        if "vote" in chat:
            if "skip" in chat:
                votes['skip'] = votes['skip'] + 1
            else:
                voted = chat.split()[2]
                votes[voted] = votes[voted] + 1
    return votes


def get_paths(chat_log):
    find_path = {
        "red" : [],
        "blue" : [],
        "green" : [],
        "orange" : [],
        "pink" : [],
        "yellow" : [],
        "brown" : [],
    }
    for chat in chat_log:
        check = chat.split()
        if check[1] == check[0].strip(":"):
            find_path[check[1]].append(check[3])
    return find_path


def get_sus_paths(path_dict,rooms):
    susstring = []
    for color in path_dict:
        path = path_dict[color]
        if path == []:
            break
        for i in range(0,len(path)-1):
            current_room = path[i] #note these variables arent necessary, just for ease of reading
            next_room = path[i+1]
            valid_path = rooms.get(current_room)
            if next_room not in valid_path:
                susstring.append(color)
                break
    return susstring
    #the below code is how we could accomplish the above in 9 lines but the above code is clearer imo!:
    # susstring = []
    # for color in path_dict:
    #     if path_dict[color] == []:
    #         break
    #     for i in range(0,len(path_dict[color])-1):
    #         if path_dict[color][i+1] not in rooms.get(path_dict[color][i]):
    #             susstring.append(color)
    #             break
    # return susstring


def main():
    mapy = load_map("skeld.txt")
    c_log = load_chat_log("chatlog.txt",mapy)
    tallied_votes = tally_votes(c_log) #should I leave as variable?
    pathy = get_paths(c_log)
    sus_colours = get_sus_paths(pathy,mapy) #returns a string of sus colours
    #testing:
    print('MAP DICT')
    pprint(mapy)
    print('CHAT LOG')
    pprint(c_log)
    print('VOTES DICT')
    pprint(tallied_votes)
    print('SELF DECLARED PATHWAYS')
    pprint(pathy)
    print('SUS COLOURS')
    pprint(sus_colours)


if __name__ == "__main__":
    main()