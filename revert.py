import os
import subprocess
import sys

def run(cmd):
    print(f"> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    # checa se está no root
    if os.geteuid() != 0:
        print("Este script precisa ser executado como root.")
        sys.exit(1)

    # comandos de reversão
    try:
        run("iptables -F")
        run("iptables -X")
        run("iptables -P INPUT ACCEPT")
        run("iptables -P OUTPUT ACCEPT")
        run("iptables -P FORWARD ACCEPT")
        print("Reversão concluída.")
        print("Você pode usar 'sudo iptables -L -v -n' para verificar o estado atual")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comando iptables: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
