from aiohttp import web
import socketio
import asyncio
import subprocess
import json

socketio = socketio.AsyncServer()
app = web.Application()
socketio.attach(app)

loop = asyncio.get_event_loop()

ipRange = '192.168.0.*'
ipStart = '192'

Users = {}
with open('Users.json') as file:
    Users = json.load(file)


async def index(request):
    return web.FileResponse('./main/templates/index.html')


@socketio.on('getTable', namespace='/main')
async def whoshome(sid):
    await socketio.emit('table', Users, namespace='/main', room=sid)


@socketio.on('addUser', namespace='/main')
async def addUser(sid, data):
    ##Error checking of the user web inputs
    ##update users list 
    with open('Users.json', 'w') as file:
        json.dump(Users, file)
    return 0


async def updateNmap():
    while True: 
        ##get nmap data
        cmd = 'sudo nmap -sn ' + ipRange
        y = subprocess.run(['sudo', 'nmap', '-sn', ipRange], stdout=subprocess.PIPE)
        output = str(y.stdout)
        ##process nmap data
        vals = output.split('\\n')

        i = 0
        while 'Starting' not in vals[i]:
            i = i+1

        while i+3 < len(vals):
            i = i+1
            ip = vals[i][21:]
            i = i+2
            mac = vals[i][13:30]


        ##put data into Online dict
        ##put last seen data in the users file
        await asyncio.sleep(300)


#loop.create_task(updateNmap())

app.router.add_get('/', index)
app.router.add_static('/static/', path=str('./main/static'), name='static')
web.run_app(app, port=8080)





