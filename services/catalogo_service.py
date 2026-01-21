from xmlrpc.server import SimpleXMLRPCServer

musicas = [
    "Arabian Nights",
    "Desert Wind",
    "Ali Baba Theme",
    "Cave of Wonders"
]

def listar_musicas():
    print("📀 Listagem solicitada pelo gateway")
    return musicas

server = SimpleXMLRPCServer(("localhost", 8001), allow_none=True)
server.register_function(listar_musicas, "listar_musicas")

print("🎼 Serviço de Catálogo ativo (8001)")
server.serve_forever()
