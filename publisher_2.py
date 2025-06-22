import argparse
import random
import string
import time
import subprocess
import tempfile
import os

def gerar_payload(tamanho):
    """Gera uma string aleatória com o tamanho especificado."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=tamanho))

def main():
    parser = argparse.ArgumentParser(description="Envia pacotes MQTT com dados aleatórios via mosquitto_pub.")
    parser.add_argument("intervalo", type=float, help="Tempo entre pacotes em segundos")
    parser.add_argument("destino", type=str, help="Endereço do broker Mosquitto (ex: localhost ou 192.168.0.10)")
    parser.add_argument("tamanho", type=int, help="Tamanho do payload em bytes")
    parser.add_argument("topico", type=str, help="Tópico MQTT para envio dos dados")

    args = parser.parse_args()
    
    MAX_MQTT_PAYLOAD = 268_435_455  # Limite real do MQTT 3.1.1 268435455

    if args.tamanho > MAX_MQTT_PAYLOAD:
        print(f"Erro: tamanho máximo permitido pelo MQTT é {MAX_MQTT_PAYLOAD} bytes (~256 MB).")
        return


    print(f"Iniciando envio para {args.destino} no tópico '{args.topico}' com pacotes de {args.tamanho} bytes a cada {args.intervalo}s...")

    try:
        while True:
            payload = gerar_payload(args.tamanho)
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
                temp.write(payload)
                temp_path = temp.name

            comando = [
                "mosquitto_pub",
                "-h", args.destino,
                "-t", args.topico,
                "-f", temp_path
            ]
            subprocess.run(comando)
            print(f"Publicado ({args.tamanho} bytes)")
            os.remove(temp_path)  # Remove o arquivo temporário
            time.sleep(args.intervalo)
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")

if __name__ == "__main__":
    main()

