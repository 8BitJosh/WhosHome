from aiohttp import web
import socketio
import asyncio
import subprocess
import json
import time
import os

socketio = socketio.AsyncServer()
app = web.Application()
socketio.attach(app)

loop = asyncio.get_event_loop()

#ipRange = '192.168.0.*'
ipRange = '10.9.162.*'

Users = {}

if not os.path.isfile('Users.json'):
    with open('Users.json', 'w') as file:
        json.dump({}, file)
        Users = json.load(file)

async def index(request):
    return web.FileResponse('./main/templates/index.html')


@socketio.on('getTable', namespace='/main')
async def whoshome(sid):
    global Users
    await socketio.emit('table', Users, namespace='/main', room=sid)


@socketio.on('addUser', namespace='/main')
async def addUser(sid, data):
    if data['mac'] not in Users:
        return 0
    
    Users[data['mac']]['name'] = data['name']
    print(data)

    with open('Users.json', 'w') as file:
        json.dump(Users, file)

    await socketio.emit('table', Users, namespace='/main')


def saveFile():
    with open('Users.json', 'w') as file:
        json.dump(Users, file)


async def updateNmap():
    global Users

    while True: 
        tempUsers = Users
        # get nmap data
        cmd = 'sudo nmap -sn ' + ipRange
        y = subprocess.run(['sudo', 'nmap', '-sn', ipRange], stdout=subprocess.PIPE)
        output = str(y.stdout)
        timeNow = time.ctime().format()
        print('Scan Run at ' + timeNow)
        # process nmap data
        vals = output.split('\\n')

        for user in tempUsers:
            user['Online'] = 0

        i = 0
        while 'Starting' not in vals[i]:
            i = i+1

        while i+3 < len(vals):
            i = i+1
            ip = vals[i][21:]
            i = i+2
            mac = vals[i][13:30]

            if mac not in tempUsers:
                tempUsers[mac] = {}

            tempUsers[mac]['ip'] = ip
            tempUsers[mac]['last'] = timeNow
            tempUsers[mac]['online'] = 1

        Users = tempUsers
        await socketio.emit('table', Users, namespace='/main')
        saveFile()
        await asyncio.sleep(300)


loop.create_task(updateNmap())

app.router.add_get('/', index)
app.router.add_static('/static/', path=str('./main/static'), name='static')
web.run_app(app, port=8080)





