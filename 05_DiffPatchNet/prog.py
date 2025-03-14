import asyncio
import cowsay
import shlex

clients = {}
clients_names = {}


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)

    username = None
    clients[me] = asyncio.Queue()

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while True:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                text = q.result().decode()

                match shlex.split(text):
                    case ["who"]:
                        await clients[me].put(", ".join(clients_names.keys()))
                    case ["cows"]:
                        await clients[me].put(", ".join(cowsay.list_cows() - clients.keys()))
                    case ["login", name] if not username:
                        if name in cowsay.list_cows() - clients.keys():
                            clients_names[name] = me
                            username = name
                    case ["say", name, message] if username:
                        await clients[clients_names[name]].put(f"{username}>\n{cowsay.cowsay(message, cow=username)}")
                    case ["yield", message] if username:
                        for out in map(lambda x: clients[clients_names[x]], clients_names.keys()):
                            if out is not clients[me]:
                                await out.put(f"{username}>\n{cowsay.cowsay(message, cow=username)}")
                    case ["quit"]:
                        clients.pop(me)
                        clients_names.pop(username)
                        send.cancel()
                        receive.cancel()
                        print(me, "DONE")
                        del clients[me]
                        writer.close()
                        await writer.wait_closed()
                        return
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
