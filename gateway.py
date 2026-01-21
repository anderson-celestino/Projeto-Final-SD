import xmlrpc.client
from messaging import RabbitMQService

catalogo = xmlrpc.client.ServerProxy("http://localhost:8001")
playlist = xmlrpc.client.ServerProxy("http://localhost:8002")
recomendacao = xmlrpc.client.ServerProxy("http://localhost:8003")

rabbit = RabbitMQService()

def buscar_musicas():
    rabbit.publish("usuario:listou_musicas")
    return catalogo.listar_musicas()

def criar_playlist(nome, musica):
    playlist.criar_playlist(nome, musica)
    rabbit.publish(f"playlist_criada:{nome}")

def recomendar_musicas(musica):
    rabbit.publish(f"usuario:recomendacao:{musica}")
    return recomendacao.recomendar(musica)
