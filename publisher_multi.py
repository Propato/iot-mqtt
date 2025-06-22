import argparse
import random
import string
import time
import subprocess
import tempfile
import os
from multiprocessing import Process

MAX_MQTT_PAYLOAD = 268_435_455  # Limite real do MQTT 3.1.1 (~256MB)
# 268435400


def gerar_payload(tamanho):
    """Gera uma string aleatória com o tamanho especificado."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))


def publicador(intervalo, destino, tamanho, topico, id_pub):
    """Função que cada publicador executa."""
    print(f"[Publisher {id_pub}] Iniciando...")
    try:
            payload = gerar_payload(tamanho)
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
                temp.write(payload)
                temp_path = temp.name
                
    except Exception as e:
        print(f"[Publisher {id_pub}] Erro ao gerar o payload: {e}")
        return
                
    while True:
        try:
            comando = [
                "mosquitto_pub",
                "-h", destino,
                "-t", topico,
                "-f", temp_path
            ]
            subprocess.run(comando)
            print(f"[Publisher {id_pub}] Publicado ({tamanho} bytes)")
            time.sleep(intervalo)
        except subprocess.CalledProcessError as e:
            print(f"[Publisher {id_pub}] Erro ao publicar: {e}")
            os.remove(temp_path)
            break
            
    os.remove(temp_path)


def main():
    parser = argparse.ArgumentParser(description="Envia pacotes MQTT com dados aleatórios via mosquitto_pub.")
    parser.add_argument("intervalo", type=float, help="Tempo entre pacotes em segundos")
    parser.add_argument("destino", type=str, help="Endereço do broker Mosquitto (ex: localhost ou 192.168.0.10)")
    parser.add_argument("tamanho", type=int, help="Tamanho do payload em bytes")
    parser.add_argument("topico", type=str, help="Tópico MQTT para envio dos dados")
    parser.add_argument("-n", "--publicadores", type=int, default=1, help="Número de publishers simultâneos")

    args = parser.parse_args()

    if args.tamanho > MAX_MQTT_PAYLOAD:
        print(f"Erro: tamanho máximo permitido pelo MQTT é {MAX_MQTT_PAYLOAD} bytes (~256 MB).")
        return

    print(f"Iniciando {args.publicadores} publicador(es) para {args.destino} no tópico '{args.topico}'...")

    processos = []
    try:
        for i in range(args.publicadores):
            p = Process(target=publicador, args=(args.intervalo, args.destino, args.tamanho, args.topico, i + 1))
            p.start()
            processos.append(p)

        for p in processos:
            p.join()
    except KeyboardInterrupt:
        print("\nInterrompendo todos os publishers...")
        for p in processos:
            p.terminate()
        print("Finalizado.")

if __name__ == "__main__":
    main()

