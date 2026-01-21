from xmlrpc.server import SimpleXMLRPCServer

playlists = {}

def criar_playlist(nome, musica):
    if nome not in playlists:
        playlists[nome] = []
    playlists[nome].append(musica)
    print(f"📂 Playlist '{nome}' atualizada com '{musica}'")
    return True

server = SimpleXMLRPCServer(("localhost", 8002), allow_none=True)
server.register_function(criar_playlist, "criar_playlist")

print("📂 Serviço de Playlists ativo (8002)")
server.serve_forever()
