import argparse
import subprocess
from multiprocessing import Process

def subscriber(destino, topico, id_sub):
    """Executa um mosquitto_sub com identificação."""
    comando = [
        "mosquitto_sub",
        "-h", destino,
        "-t", topico
    ]

    processo = subprocess.Popen(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    print(f"[Subscriber {id_sub}] Subscrito ao tópico '{topico}' em {destino}.")

    try:
        for linha in processo.stdout:
            print(f"[Subscriber {id_sub}] Recebeu: {linha.strip()}")
    except KeyboardInterrupt:
        processo.terminate()
        print(f"[Subscriber {id_sub}] Interrompido.")

def main():
    parser = argparse.ArgumentParser(description="Cria múltiplos subscribers via mosquitto_sub.")
    parser.add_argument("destino", type=str, help="Endereço do broker Mosquitto (ex: localhost)")
    parser.add_argument("topico", type=str, help="Tópico MQTT a ser subscrito")
    parser.add_argument("-n", "--subscribers", type=int, default=1, help="Número de subscribers a serem criados")

    args = parser.parse_args()

    print(f"Iniciando {args.subscribers} subscriber(s) para o tópico '{args.topico}' em {args.destino}...")

    processos = []
    try:
        for i in range(args.subscribers):
            p = Process(target=subscriber, args=(args.destino, args.topico, i + 1))
            p.start()
            processos.append(p)

        for p in processos:
            p.join()
    except KeyboardInterrupt:
        print("\nInterrompendo todos os subscribers...")
        for p in processos:
            p.terminate()
        print("Finalizado.")

if __name__ == "__main__":
    main()

