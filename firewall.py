import subprocess

def run(cmd):
    print(f"Executando: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def configurar_firewall():
    print("=== Configurando firewall ===")

    # Zerar regras anteriores
    run("iptables -F")
    run("iptables -X")
    run("iptables -t nat -F") # Limpa a tabela NAT também
    run("iptables -t nat -X") # Limpa a tabela NAT também
    run("iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")

    # Política padrão: bloquear tudo
    run("iptables -P INPUT DROP")
    run("iptables -P OUTPUT ACCEPT")
    run("iptables -P FORWARD DROP")

    # Permitir HTTP de saída e respostas
    run("iptables -A FORWARD -p tcp --dport 80 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT")
    run("iptables -A FORWARD -p tcp --sport 80 -m state --state ESTABLISHED,RELATED -j ACCEPT")

    run("iptables -A FORWARD -p icmp -o eth0 -j DROP")  # Bloquear ICMP externo

    run("iptables -A FORWARD -p icmp -i eth1 -o eth1 -j ACCEPT")  # Permitindo ICMP interno

    run("iptables -A FORWARD -p tcp -d 157.240.0.0/16 -j REJECT")  # Bloqueando Facebook
    run("iptables -A FORWARD -p tcp -d 31.13.0.0/16 -j REJECT")    # Bloqueando Instagram

    print("=== Firewall configurado com sucesso ===")

if __name__ == "__main__":
    configurar_firewall()
