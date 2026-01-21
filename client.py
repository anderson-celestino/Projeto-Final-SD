import gateway

def menu():
    print("\n🎧 Sistema de Música Distribuído")
    print("1 - Listar músicas")
    print("2 - Criar playlist")
    print("3 - Ver recomendações")
    print("0 - Sair")

while True:
    menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        musicas = gateway.buscar_musicas()
        print("\n🎶 Músicas disponíveis:")
        for m in musicas:
            print("-", m)

    elif opcao == "2":
        nome = input("Nome da playlist: ")
        musica = input("Adicionar qual música? ")
        gateway.criar_playlist(nome, musica)
        print("✅ Playlist criada!")

    elif opcao == "3":
        musica = input("Digite o nome da música: ")
        recs = gateway.recomendar_musicas(musica)
        print("\n🎯 Recomendações:")
        for r in recs:
            print("-", r)

    elif opcao == "0":
        print("👋 Encerrando sistema.")
        break

    else:
        print("❌ Opção inválida.")
