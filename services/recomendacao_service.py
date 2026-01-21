from xmlrpc.server import SimpleXMLRPCServer

recomendacoes = {
    "Arabian Nights": ["Desert Wind", "Cave of Wonders"],
    "Desert Wind": ["Arabian Nights"],
    "Ali Baba Theme": ["Cave of Wonders"]
}

def recomendar(musica):
    print(f"🎯 Recomendação solicitada para '{musica}'")
    return recomendacoes.get(musica, ["Arabian Nights"])

server = SimpleXMLRPCServer(("localhost", 8003), allow_none=True)
server.register_function(recomendar, "recomendar")

print("🎯 Serviço de Recomendações ativo (8003)")
server.serve_forever()
