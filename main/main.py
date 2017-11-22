from aiohttp import web
import socketio
import asyncio

socketio = socketio.AsyncServer()
app = web.Application()
socketio.attach(app)

loop = asyncio.get_event_loop()

Users = {}

async def loadFile():
    return 0


async def saveFile():
    return 0 


async def index(request):
    return web.FileResponse('./main/templates/index.html')


@socketio.on('getTable', namespace='/main')
async def whoshome(sid):
    return 0


@socketio.on('addUser', namespace='/main')
async def addUser(sid, data):
    return 0


app.router.add_get('/', index)
app.router.add_static('/static/', path=str('./main/static'), name='static')
web.run_app(app, port=8080)





