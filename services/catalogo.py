import sys
import os

# Adiciona o diretório pai (..) ao caminho do sistema para importar messaging.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from messaging import RabbitMQService

# --- Banco de Dados Mockado (Na memória) ---
MUSICAS = [
    {"id": 1, "titulo": "Bohemian Rhapsody", "artista": "Queen", "genero": "Rock"},
    {"id": 2, "titulo": "Shape of You", "artista": "Ed Sheeran", "genero": "Pop"},
    {"id": 3, "titulo": "Billie Jean", "artista": "Michael Jackson", "genero": "Pop"},
    {"id": 4, "titulo": "Smells Like Teen Spirit", "artista": "Nirvana", "genero": "Rock"},
    {"id": 5, "titulo": "Hotel California", "artista": "Eagles", "genero": "Rock"},
    {"id": 6, "titulo": "Blinding Lights", "artista": "The Weeknd", "genero": "Pop"},
]


def logica_catalogo(request):
    """
    Função de Callback que processa os pedidos que chegam na fila 'catalogo_queue'
    Espera receber um dicionário: {'action': '...', ...}
    """
    acao = request.get('action')

    print(f" [.] Processando ação: {acao}")

    if acao == 'listar_todas':
        return {"status": "success", "data": MUSICAS}

    elif acao == 'buscar':
        termo = request.get('query', '').lower()
        # Filtra músicas onde o termo aparece no título ou artista
        resultado = [
            m for m in MUSICAS
            if termo in m['titulo'].lower() or termo in m['artista'].lower()
        ]
        return {"status": "success", "data": resultado}

    elif acao == 'detalhes':
        music_id = request.get('id')
        for m in MUSICAS:
            if m['id'] == music_id:
                return {"status": "success", "data": m}
        return {"status": "error", "message": "Música não encontrada"}

    else:
        return {"status": "error", "message": "Ação desconhecida"}


if __name__ == "__main__":
    # Inicia o serviço ouvindo na fila 'catalogo_queue'
    # O RabbitMQService (do messaging.py) cuida de toda a conexão e RPC
    servico = RabbitMQService(service_queue='catalogo_queue', business_logic_callback=logica_catalogo)

    try:
        servico.start()
    except KeyboardInterrupt:
        print("Serviço de Catálogo encerrado.")