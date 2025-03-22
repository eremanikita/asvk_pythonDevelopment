import asyncio
import cowsay
import shlex

clients = {}


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)

    username = None
    queue = asyncio.Queue()

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue.get())
    while True:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                text = q.result().decode()
                print(text)
                match shlex.split(text):
                    case [code, "who"]:
                        await queue.put(f"{code} " + ", ".join(clients.keys()))
                    case [code, "cows"]:
                        await queue.put(f"{code} " + ", ".join(cowsay.list_cows() - clients.keys()))
                    case [code, "login", name] if not username:
                        if name in cowsay.list_cows() - clients.keys():
                            username = name
                            clients[name] = queue
                    case [code, "say", name, message] if username:
                        await clients[name].put(f"{code} {cowsay.cowsay(message, cow=username)}")
                    case [code, "yield", message] if username:
                        for out in clients.values():
                            if out is not clients[username]:
                                await out.put(f"{code} {cowsay.cowsay(message, cow=username)}")
                    case [code, "quit"]:
                        send.cancel()
                        receive.cancel()
                        print(me, "DONE")
                        del clients[username]
                        writer.close()
                        await writer.wait_closed()
                        return
            elif q is receive:
                receive = asyncio.create_task(queue.get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
