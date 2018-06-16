from flask import Flask
from flask import render_template
from flask import request
import urllib.request 
import json
import os

token = ''
#'bbb5f50ce78e38e84d5420cbcfbf6a51d6820d6c065079b7b72f2f844a5fb362ab7ecc8a71d4c2761b332'

def get_data_from_url(url):
    req = urllib.request.Request(url) 
    response = urllib.request.urlopen(req) 
    result = response.read().decode('utf-8')
    return (result)

def get_friends(user_id, token):
    result = get_data_from_url('https://api.vk.com/method/friends.get?user_id='+str(user_id)+'&v=5.74&access_token='+str(token))
    raw_data = json.loads(result)
    data = raw_data['response']['items']
    friends_list = [str(i) for i in data]
    users = ','.join(friends_list)
    u_result = json.loads(get_data_from_url('https://api.vk.com/method/users.get?user_ids='+users+'&fields=deactivated&v=5.74&access_token='+str(token)))['response']
    for user in u_result:
        if 'deactivated' in user:
            data.remove(user['id'])
    data.append(int(user_id))
    return data

def nodes(data, dict_to_graph, user_id):
    for user in data:
        if user == user_id:
            dict_edge = {"name": user, "group":0}
        else:
            dict_edge = {"name": user, "group":1}
        dict_to_graph ['nodes'].append(dict_edge)
    return dict_to_graph

def create_links(friends_list, user_id, dict_to_graph, done, data):
    target_uids = ','.join(friends_list)
    mutual_friends = get_data_from_url('https://api.vk.com/method/friends.getMutual?source_uid='+str(user_id)+'&target_uids='+str(target_uids)+'&v=5.74&access_token='+str(token))
    friends = json.loads(mutual_friends)['response']
    dict_link = {}
    for user in data:
        for friend in friends:
            if user in friend['common_friends']:
                dict_link = {"source":data.index(user), "target":data.index(friend['id']), "value":1}
                dict_to_graph['links'].append(dict_link)
        done.append(user)
    return dict_to_graph

def links_by_lists(data, dict_to_graph, user_id, done):
    raw_friends_list = [str(fr_id) for fr_id in data]
    for i in range(len(raw_friends_list)//100):
        friends_list = raw_friends_list[i:i+100]
        create_links(friends_list, user_id, dict_to_graph, done, data)
    friends_list = raw_friends_list[len(raw_friends_list)-len(raw_friends_list)%100:len(raw_friends_list)]
    create_links(friends_list, user_id, dict_to_graph, done, data)
    return

def get_user_info(user_id):
    result = get_data_from_url('https://api.vk.com/method/users.get?user_ids='+str(user_id)+'&fields=first_name,last_name,sex,bdate,city,country&v=5.74&access_token='+str(token))
    user_info = json.loads(result)
    return user_info

def dict_uinfo (user_id):
    user_info = get_user_info(user_id)['response'][0]
    infos = {'name' : 'first_name', 'surname' :'last_name', 'sex' : 'sex', 'city':'city', 'country':'country', 'bd':'bdate'}
    infodata = {}
    for item in infos:
        if infos[item] in list(user_info.keys()):
            if infos[item] == 'city' or infos[item] == 'country':
                infodata[infos[item]] = user_info[infos[item]]['title']
            else:
                infodata[infos[item]] = user_info[infos[item]]
        else:
            infodata[infos[item]] = "Не указано"
        if user_info ['sex'] == 1:
            infodata ['sex'] = "Женский"
        else:
            infodata ['sex'] = "Мужской"
    return infodata

app = Flask(__name__)

@app.route('/')
def auth():
    return render_template('auth_page.html')

@app.route('/ok/')
def ok():
    global token
    token = request.args['token']
    return render_template('write_token.html')

@app.route('/gettoken/')
def get_token():
    link = 'https://oauth.vk.com/access_token?client_id=6603537&client_secret=lqTve329nImo4NVEnzhV&redirect_uri=https://project-friends-network.herokuapp.com/gettoken/&code='+request.args['code']
    return render_template('token_page.html', link=link)

@app.route('/initial/')
def index():
    global token
    return render_template('index_page.html')

@app.route('/graph/')
def graph():
    done = []
    user_id = request.args['user_id']
    infodata = dict_uinfo (user_id)
    uuuu  = get_user_info(user_id)
    dict_to_graph = { "nodes": [],
                      "links": []}
    data = get_friends(user_id, token)
    dict_to_graph = nodes(data, dict_to_graph, user_id)
    links_by_lists(data, dict_to_graph, user_id, done)
    json_data = json.dumps(dict_to_graph)
    result = get_data_from_url('https://api.vk.com/method/friends.get?user_id='+str(user_id)+'&v=5.74&access_token='+str(token))
    return render_template('graph_html_text.html', json_data = dict_to_graph, name = infodata['first_name'], surname = infodata['last_name'], bd = infodata['bdate'], sex = infodata['sex'], city = infodata['city'], country = infodata['country'])


if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
