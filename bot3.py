import websocket,threading,json,time,requests,random,urllib.parse,bs4,string
from backend import check_pings
s = requests.session()
s.verify = False
ids=str(int(time.time()))+str(random.randint(0,900))

def parser(step,text):
    if step == 0:

        soup = bs4.BeautifulSoup(text,'lxml')
        return soup.findAll('a')
    elif step == 1:
        'get tags'
        soup = bs4.BeautifulSoup(text,'lxml')
        alltags = soup.find('span',{'id':'tags_value'}).text
        first_tag = alltags.lstrip().rstrip().split(',')[0]
        return first_tag
    elif step == 2:
        soup = bs4.BeautifulSoup(text,'lxml')
        profile_id = soup.find('img',{'id':'profile_avatar'})['src'].split('/')[5]
        return '1'+profile_id
def get_model_idv2(username):
    url2 = s.get('https://profiles.myfreecams.com/{}'.format(username), headers={
        'Host': 'profiles.myfreecams.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://m.myfreecams.com/profiles/{}'.format(username),
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    })
    ftag = parser(2, url2.text)
    return ftag
def generaterandomstring(num):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=num))
def connect_room(model_username,ROOMID,proxy_to_use):

    msent = 0
    nid = 0
    userid = 0
    websocket_id_room = ''
    websocket_lentype = ''
    websocket_cxid = ''
    arg1 = ''
    arg2 = ''
    respkey = ''

    def on_message(ws, message):
        global msent, websocket_id_room, websocket_lentype, websocket_cxid, arg1, arg2, respkey
        try:
            message1 = json.loads(urllib.parse.unquote_plus(message.split(' ')[-1]))

            if '_err' in message1.keys():
                websocket_id_room = message1['ctx'][0]
                websocket_lentype = message1['ctx'][-1]
                websocket_cxid = message1['cxid']
            if 'msg' in message1.keys():
                arg1 = message1['msg']['arg1']
                if arg1 > 10000:
                    print('AJA HACKING')
                    arg2 = message1['msg']['arg2']
                    respkey = message1['respkey']
                    serv = message1['serv']
                    # print([arg1,arg2])

                    str1 = 'https://www.myfreecams.com/php/FcwExtResp.php?respkey={}&type=14&opts=256&serv={}&arg1={}&arg2={}&owner=38012424&nc={}'.format(
                        respkey, serv, str(2000), arg2, websocket_cxid)
                    str2 = 'https://www.myfreecams.com/php/FcwExtResp.php?respkey={}&type=14&opts=256&serv={}&nc=0.6544192043797341&_={}'.format(
                        respkey, serv, str(int(time.time())))

                    # input(json.loads(requests.get(str2).text))
                    all_models = json.loads(requests.get(str1).text)

                    for ele in all_models['rdata'][1:]:
                        print([ele[0], ele[1], ele[2]])
            if 'sid' in message1.keys():
                if message1['sid'] == websocket_id_room:
                    print('LOGGED IN AS > {}'.format(message1['nm']))
                    # jroom()

            # print(message1)
            def jroom():
                if proxy_to_use == '1':
                    ws.send('51 {} 0 {} 9\n\0'.format(websocket_id_room, ROOMID))
                else:
                    allinf2 = json.loads(requests.get('http://localhost:5000/api?action=get_models&web=mfc').text)
                    for ele in allinf2['success']:
                        if ele[0] == model_username:
                            if ele[1] == 'run':
                                ws.send('51 {} 0 {} 9\n\0'.format(websocket_id_room, ROOMID))
                            elif ele[1] == 'stop':
                                ws.close()
                                exit()
                                break
            jroom()
            #apisend()
        except:
            pass
    def on_error(ws, error):
        print('ERROR')
        print(error)
        ws.close()
    def on_close(ws):
        print('CLOSED')
        print("### closed ###")
        # ws.close()
    def on_open(ws):
        def wssend():
            while True:
                ws.send('0 0 0 0 0\n\0')
                time.sleep(30)

        def apisend():
            bid = 'botctb_{}'.format(str(generaterandomstring(8)))

            url = requests.get(
                'http://localhost:5000/api?action=newbot&model_username={}&ping={}&botid={}'.format(model_username, str(
                    int(time.time())), bid))
            while True:
                'check by server'
                allinfo = json.loads(requests.get('http://localhost:5000/api?action=get_models&web=mfc').text)
                for ele in allinfo['success']:
                    if ele[0] == model_username:
                        if ele[1] == 'stop':
                            ws.close()
                            exit()

                'check by server max live time'
                res2 = check_pings(direct_result=bid)
                if res2 == False:
                    ws.close()
                    exit()
                time.sleep(5)

        ws.send('fcsws_20180422\n\0')
        ws.send('1 0 0 20071025 0 1/guest:guest\n\0')
        time.sleep(3)

        threading.Thread(target=wssend).start()
        threading.Thread(target=apisend).start()

    websocket.enableTrace(False)
    chat_servers = [76,111,107,108,61,94,109,37,38,47,48,49,50,51,52,53,54,57,26,95,112,113,114,115,116,118,119,41,42,43,44,58,27,45,46,39,59,120,121,122,123,124,125,126,67,66,62,63,64,65,69,70,71,72,73,74,75,77,40,60,80,28,29,30,31,32,33,34,35,36,90,91,92,93,81,82,83,79,68,78,84,85,86,87,88,89,96,97,98,99,100,101,102,103,104,105,106,110,127,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    ws = websocket.WebSocketApp('wss://xchat{}.myfreecams.com/fcsl'.format(str(random.choice(chat_servers))),
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    if proxy_to_use == '1':
        ws.run_forever()
    else:
        total_info = proxy_to_use.split(':')
        if len(total_info) == 4:
            ws.run_forever(http_proxy_host=total_info[2],http_proxy_port=int(total_info[3]),http_proxy_auth=(total_info[0],total_info[1]))
        elif len(total_info) == 2:
            ws.run_forever(http_proxy_host=total_info[0], http_proxy_port=int(total_info[1]))

def start_bot(model_username, MAX_PER_CONNECTION,direct=False):
    if direct == True:
        ROOMID = get_model_idv2(model_username)
        roomtotal = json.loads(requests.get('http://localhost:5000/api?action=get_models&web=mfc'))['cgc']
        for i in range(int(roomtotal)):
            threading.Thread(target=connect_room, args=(model_username, ROOMID, '1')).start()
            print('STARTED > {}'.format(str(i)))
            time.sleep(1)
    else:
        for ele in json.loads(requests.get('http://localhost:5000/api?action=get_models&web=mfc').text)['success']:
            if ele[0] == model_username:
                if ele[1] == 'run':
                    ROOMID = get_model_idv2(model_username)
                    for proxy in ele[2].split(','):
                        for i in range(int(MAX_PER_CONNECTION)):
                            threading.Thread(target=connect_room, args=(ele[0], ROOMID, proxy)).start()
                            print('STARTED > {}'.format(str(i)))
                            #time.sleep(1)