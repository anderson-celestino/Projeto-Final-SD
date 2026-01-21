import sys
import os

# Adiciona o diretório pai (..) ao caminho para importar messaging.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from messaging import RabbitMQService

# --- Banco de Dados Mockado (Na memória) ---
# Estrutura: [{'id': 1, 'nome': 'Rock 80s', 'dono': 'usuario1', 'musicas': []}]
PLAYLISTS = []


def logica_playlists(request):
    """
    Processa pedidos da fila 'playlist_queue'
    """
    acao = request.get('action')
    print(f" [.] Processando ação: {acao}")

    if acao == 'criar':
        nova_playlist = {
            'id': len(PLAYLISTS) + 1,
            'nome': request.get('nome'),
            'dono': request.get('dono', 'anonimo'),
            'musicas': []  # Lista de IDs de músicas
        }
        PLAYLISTS.append(nova_playlist)
        return {"status": "success", "message": f"Playlist '{nova_playlist['nome']}' criada!"}

    elif acao == 'listar':
        # Retorna todas (em um sistema real, filtraria pelo usuário)
        return {"status": "success", "data": PLAYLISTS}

    elif acao == 'adicionar_musica':
        # Busca a playlist pelo ID
        pl_id = int(request.get('playlist_id'))
        musica_id = int(request.get('musica_id'))

        for pl in PLAYLISTS:
            if pl['id'] == pl_id:
                pl['musicas'].append(musica_id)
                return {"status": "success", "message": "Música adicionada com sucesso!"}

        return {"status": "error", "message": "Playlist não encontrada."}

    else:
        return {"status": "error", "message": "Ação desconhecida"}


if __name__ == "__main__":
    # Note que o nome da fila é diferente: 'playlist_queue'
    servico = RabbitMQService(service_queue='playlist_queue', business_logic_callback=logica_playlists)

    try:
        servico.start()
    except KeyboardInterrupt:
        print("Serviço de Playlists encerrado.")