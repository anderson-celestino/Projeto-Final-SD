# 🎧 Sistema de Música Distribuído

## 📄 Descrição do Projeto

Este projeto é uma implementação de um **Sistema de Música Distribuído** desenvolvido como trabalho final para a disciplina de Sistemas Distribuídos. Ele demonstra a utilização de diferentes padrões de comunicação, como **RPC (Remote Procedure Call)** para comunicação síncrona entre serviços e **Message Queues (RabbitMQ)** para comunicação assíncrona e registro de eventos.

O sistema simula um serviço de música básico, permitindo que um cliente liste músicas, crie playlists e solicite recomendações.

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia | Uso |
| :--- | :--- | :--- |
| Linguagem | Python 3 | Linguagem principal de desenvolvimento. |
| Comunicação Síncrona | XML-RPC | Utilizado pelo Gateway para invocar métodos nos serviços de Catálogo, Playlist e Recomendação. |
| Comunicação Assíncrona | RabbitMQ (via `pika`) | Utilizado para registro de eventos e desacoplamento entre o Gateway e o Serviço de Usuário. |

## 🏗️ Arquitetura do Sistema

A arquitetura é composta por um **Gateway** central que atua como fachada para o **Cliente**, e um conjunto de **Microsserviços** que realizam as funcionalidades específicas.

### Componentes

1.  **Cliente (`client.py`):**
    *   Interface de linha de comando para interação do usuário.
    *   Comunica-se diretamente com o **Gateway**.

2.  **Gateway (`gateway.py`):**
    *   Ponto de entrada para todas as requisições do cliente.
    *   **Síncrono (XML-RPC):** Invoca os serviços de Catálogo, Playlist e Recomendação.
    *   **Assíncrono (RabbitMQ):** Publica eventos de usuário para o `user_service.py`.

3.  **Serviços (XML-RPC):**
    *   `catalogo_service.py` (Porta 8001): Lista as músicas disponíveis.
    *   `playlists_service.py` (Porta 8002): Gerencia a criação de playlists.
    *   `recomendacao_service.py` (Porta 8003): Fornece recomendações de músicas.

4.  **Serviço de Usuário (`user_service.py`):**
    *   Consumidor de eventos do RabbitMQ.
    *   Simula o registro de logs ou processamento secundário de eventos de usuário.

### Fluxo de Comunicação

| Ação do Cliente | Comunicação Síncrona (XML-RPC) | Comunicação Assíncrona (RabbitMQ) |
| :--- | :--- | :--- |
| **Listar Músicas** | `Gateway` -> `catalogo_service` | `Gateway` publica `usuario:listou_musicas` |
| **Criar Playlist** | `Gateway` -> `playlists_service` | `Gateway` publica `playlist_criada:{nome}` |
| **Ver Recomendações** | `Gateway` -> `recomendacao_service` | `Gateway` publica `usuario:recomendacao:{musica}` |

## ⚙️ Pré-requisitos

Para executar este projeto, você precisará ter instalado:

*   **Python 3.x**
*   **RabbitMQ Server:** O servidor de mensagens deve estar rodando localmente (padrão `localhost`).

### Instalação do RabbitMQ

Se você estiver usando Docker, pode iniciar o servidor rapidamente:

```bash
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

## 🚀 Instalação e Execução

Siga os passos abaixo para configurar e rodar o projeto.

### 1. Clonar o Repositório

```bash
git clone https://github.com/anderson-celestino/Projeto-Final-SD.git
cd Projeto-Final-SD
```

### 2. Instalar Dependências

O projeto requer a biblioteca `pika` para comunicação com o RabbitMQ.

```bash
pip install -r requirements.txt
```

### 3. Iniciar os Serviços

Todos os serviços devem ser iniciados em terminais separados, pois eles rodam em *loop* infinito (`server.serve_forever()`).

**Terminal 1: Serviço de Catálogo (Porta 8001)**
```bash
python3 services/catalogo_service.py
```

**Terminal 2: Serviço de Playlists (Porta 8002)**
```bash
python3 services/playlists_service.py
```

**Terminal 3: Serviço de Recomendações (Porta 8003)**
```bash
python3 services/recomendacao_service.py
```

**Terminal 4: Serviço de Usuário (Consumidor de Eventos)**
```bash
python3 services/user_service.py
```

**Terminal 5: Gateway**
```bash
python3 gateway.py
```

### 4. Iniciar o Cliente

Com todos os serviços e o Gateway rodando, inicie o cliente em um novo terminal:

**Terminal 6: Cliente**
```bash
python3 client.py
```

## ✨ Funcionalidades

O cliente apresenta o seguinte menu de opções:

| Opção | Funcionalidade | Detalhes |
| :--- | :--- | :--- |
| **1** | Listar músicas | O `gateway` solicita a lista ao `catalogo_service` e publica o evento `usuario:listou_musicas`. |
| **2** | Criar playlist | O `gateway` solicita a criação ao `playlists_service` e publica o evento `playlist_criada:{nome}`. |
| **3** | Ver recomendações | O `gateway` solicita a recomendação ao `recomendacao_service` e publica o evento `usuario:recomendacao:{musica}`. |
| **0** | Sair | Encerra a aplicação cliente. |

## 📢 Eventos do RabbitMQ

O sistema utiliza uma fila de eventos (padrão `events`) para registro de atividades. O `user_service.py` consome os seguintes eventos:

*   `usuario:listou_musicas`
*   `playlist_criada:{nome_da_playlist}`
*   `usuario:recomendacao:{musica_solicitada}`

## 🧑‍💻 Autor

Este projeto foi desenvolvido por **Anderson Celestino** e **Yngrid Coelho** como parte dos requisitos para a disciplina de Sistemas Distribuídos.
