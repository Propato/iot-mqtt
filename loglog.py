import psutil
import time
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

def get_pid_from_container(container_name):
    try:
        result = subprocess.run(["docker", "top", container_name, "-eo", "pid,comm"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        if len(lines) < 2:
            raise Exception("Nenhum processo encontrado no container.")
        pid_line = lines[1].strip()
        pid = int(pid_line.split()[0])
        return pid
    except Exception as e:
        print(f"Erro ao obter PID do container: {e}")
        return None

def monitor_process(pid, interval=1):
    try:
        process = psutil.Process(pid)
        print(f"Monitorando processo PID={pid} ({process.name()}) a cada {interval}s...\n")
        print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
            "Tempo(s)", "CPU(%)", "Mem(MB)", "Threads", "UserCPU", "SysCPU"
        ))

        start_time = time.time()
        data = []

        while process.is_running():
            try:
                cpu = process.cpu_percent(interval=interval)
                mem = process.memory_info().rss / (1024 * 1024)
                threads = process.num_threads()
                cpu_times = process.cpu_times()
                user_time = cpu_times.user
                system_time = cpu_times.system
                elapsed = int(time.time() - start_time)

                print("{:<10} {:<10.2f} {:<10.2f} {:<10} {:<10.2f} {:<10.2f}".format(
                    elapsed, cpu, mem, threads, user_time, system_time
                ))

                data.append({
                    "tempo": elapsed,
                    "cpu": cpu,
                    "memoria": mem,
                    "threads": threads,
                    "user_time": user_time,
                    "system_time": system_time
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print("\n[!] O processo terminou ou acesso negado.")
                break

        return data

    except psutil.NoSuchProcess:
        print(f"Nenhum processo com PID {pid} encontrado.")
        return []

def salvar_csv_e_graficos(data, pid):
    if not data:
        print("Nenhum dado para salvar.")
        return

    df = pd.DataFrame(data)
    nome_base = f"monitor_pid_{pid}"
    csv_path = f"{nome_base}.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n✅ Dados salvos em: {csv_path}")

    # Gráficos
    plt.figure(figsize=(15, 6))

    plt.subplot(1, 3, 1)
    plt.plot(df["tempo"], df["cpu"], label="CPU (%)", color="blue")
    plt.title("Uso de CPU (%)")
    plt.xlabel("Tempo (s)")
    plt.ylabel("CPU (%)")

    plt.subplot(1, 3, 2)
    plt.plot(df["tempo"], df["memoria"], label="Memória (MB)", color="green")
    plt.title("Uso de Memória")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Memória (MB)")

    plt.subplot(1, 3, 3)
    plt.plot(df["tempo"], df["threads"], label="Threads", color="purple")
    plt.title("Número de Threads")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Threads")

    plt.tight_layout()
    img_path = f"{nome_base}_graficos.png"
    plt.savefig(img_path)
    print(f"✅ Gráficos salvos em: {img_path}")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitorar uso de CPU e memória de um processo ou container.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pid", type=int, help="PID do processo a ser monitorado")
    group.add_argument("--container", type=str, help="Nome do container Docker")

    parser.add_argument("-i", "--interval", type=float, default=1.0, help="Intervalo de atualização em segundos (padrão: 1s)")
    args = parser.parse_args()

    pid = args.pid
    if args.container:
        pid = get_pid_from_container(args.container)
        if pid is None:
            exit(1)

    dados = []
    try:
        dados = monitor_process(pid, args.interval)
    except KeyboardInterrupt:
        print("\n\n⛔ Monitoramento interrompido com Ctrl+C.")
    finally:
        salvar_csv_e_graficos(dados, pid)
