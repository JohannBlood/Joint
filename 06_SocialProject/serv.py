import asyncio
import shlex
import cowsay

clients = {}

async def chat(reader, writer):
    temp = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(temp.get())
    fl = True
    # Registration
    while not reader.at_eof() and fl:
        requests, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for request in requests:
            if request is send:
                send = asyncio.create_task(reader.readline())
                # print(request.result().decode().strip())
                if request.result().decode().startswith('login'):
                    name = shlex.split(request.result().decode())[1]
                    if name not in clients.keys() and name in cowsay.list_cows():
                        clients[name] = temp
                        print(f'{name} has joined the chat')
                        await temp.put('Registration successful')
                        me = name
                        fl = False
                        fl1 = True
                    elif name in clients.keys() and name in cowsay.list_cows():
                        await temp.put(f'{name} is already in the chat')
                    else:
                        await temp.put(f'{name} is not a cow')
                elif request.result().decode().strip() == 'who':
                    await temp.put(' '.join(clients.keys()))
                elif request.result().decode().strip() == '#who':
                    await temp.put('\\' + ' '.join(clients.keys()))
                elif request.result().decode().strip() == '#cows':
                    await temp.put('#' + ' '.join(set(cowsay.list_cows()) - set(clients.keys())))
                elif request.result().decode().strip() == 'cows':
                    await temp.put(' '.join(set(cowsay.list_cows()) - set(clients.keys())))
                elif request.result().decode().strip() == 'quit':
                    fl1 = False
                    fl = False
                    me = None
                else:
                    await temp.put('Complete registration first')
            elif request is receive:
                receive = asyncio.create_task(temp.get())
                writer.write(f"{request.result()}\n".encode())
                await writer.drain()
    # Chatting
    while not reader.at_eof() and fl1:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                if q.result().decode().startswith('say'):
                    _, name, message = shlex.split(q.result().decode())
                    if name in clients.keys():
                        await clients[name].put(f'Private:\n {cowsay.cowsay(message, cow=me)}')
                    else:
                        await clients[me].put('No such user')
                elif q.result().decode().startswith('yield'):
                    _, message = shlex.split(q.result().decode())
                    for out in clients.values():
                        if out is not clients[me]:
                            await out.put(f"{cowsay.cowsay(message, cow=me)}")
                elif q.result().decode().strip() == 'who':
                    await clients[me].put(' '.join(clients.keys()))
                elif q.result().decode().strip() == '#who':
                    await clients[me].put('\\' + ' '.join(clients.keys()))
                elif q.result().decode().strip() == '#cows':
                    await clients[me].put('#' + ' '.join(set(cowsay.list_cows()) - set(clients.keys())))
                elif q.result().decode().strip() == 'cows':
                    await clients[me].put(' '.join(set(cowsay.list_cows()) - set(clients.keys())))
                elif q.result().decode().strip() == 'quit':
                    fl1 = False
                    break
                else:
                    await clients[me].put('No such command')
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    if me:
        print(me, "DONE")
        del clients[me]
    writer.write('Leaving the chat'.encode())
    await writer.drain()
    send.cancel()
    receive.cancel()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())