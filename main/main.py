from aiohttp import web
import socketio
import asyncio
import subprocess
import json
from datetime import datetime
import os

socketio = socketio.AsyncServer()
app = web.Application()
socketio.attach(app)

loop = asyncio.get_event_loop()

ipRange = '192.168.0.*'
#ipRange = '10.9.159.*'

Users = {}
if not os.path.isfile('Users.json'):
    with open('Users.json', 'w') as file:
        json.dump({}, file)

with open('Users.json', 'r') as file:
    Users = json.load(file)


async def index(request):
    return web.FileResponse('./main/templates/index.html')


@socketio.on('getTable', namespace='/main')
async def whoshome(sid):
    global Users
    await socketio.emit('table', Users, namespace='/main', room=sid)


@socketio.on('addUser', namespace='/main')
async def addUser(sid, data):
    global Users
    if data['mac'] not in Users:
        return 0

    Users[data['mac']]['name'] = data['name']
    print(data)

    saveFile()
    await socketio.emit('table', Users, namespace='/main')


def saveFile():
    global Users
    with open('Users.json', 'w') as file:
        print('Saving file - ' + datetime.now().strftime("[%d/%m/%y %H:%M:%S]"))
        json.dump(Users, file)


async def updateNmap():
    global Users
    await asyncio.sleep(20)

    while True:
        p = subprocess.Popen(['sudo','nmap','-oX','-','-sn','192.168.0.0/24'],
                            bufsize=10000,stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (temp_xml,temp_err) = p.communicate()
        temp_json=bf.data(fromstring(temp_xml))

        tempUsers = Users
        timeNow = datetime.now().strftime("[%d/%m/%y %H:%M:%S]")
        print('Scan run at {} in {} seconds, hosts up: {}'.format(timeNow,
                            temp_json['nmaprun']['runstats']['finished']['@elapsed'],
                            temp_json['nmaprun']['runstats']['hosts']['@up']))
        for key in tempUsers:
            tempUsers[key]['online'] = 0

        for y in range(0,temp_json['nmaprun']['runstats']['hosts']['@up']):
            mac = "none"
            ip = "none"
            ipv6 = "none"
            if len(temp_json['nmaprun']['host'][y]['hostnames']) > 0:
                hostname = temp_json['nmaprun']['host'][y]['hostnames']['hostname']['@name']
            else:
                hostname = "none"
            host_state = temp_json['nmaprun']['host'][y]['status']['@state']
            if type(temp_json['nmaprun']['host'][y]['address']) == list:
                for x in range(0,len(temp_json['nmaprun']['host'][y]['address'])):
                    temp_addr = temp_json['nmaprun']['host'][y]['address'][x]['@addr']
                    temp_addr_type = temp_json['nmaprun']['host'][y]['address'][x]['@addrtype']
                    if temp_addr_type == "ipv4":
                        ip = temp_addr
                    elif temp_addr_type == "ipv6":
                        ipv6 = temp_addr
                    elif temp_addr_type == "mac":
                        mac = temp_addr
            else:
                continue

            if mac not in tempUsers:
                tempUsers[mac] = {}

            if 'name' not in tempUsers[mac]:
                tempUsers[mac]['name'] = 'undefined'

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
