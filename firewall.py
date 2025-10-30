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
    run("iptables -t nat -A POSTROUTING -o ens18 -j MASQUERADE")

    # Política padrão: bloquear tudo
    run("iptables -P INPUT DROP")
    run("iptables -P OUTPUT ACCEPT")
    run("iptables -P FORWARD DROP")

    # Permitir todo o tráfego da interface de loopback (importante)
    run("iptables -A INPUT -i lo -j ACCEPT")

    # Permitir tráfego ESTABELECIDO E RELACIONADO (respostas do roteador)
    run("iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT")

    # Permitir tráfego da sua LAN interna (ens19) para o roteador
    # Isso permite SSH e PING da sua rede interna
    run("iptables -A INPUT -i ens19 -j ACCEPT")
    # === FIM DAS REGRAS DE INPUT ===

    # Permitir DNS (UDP porta 53)
    run("iptables -A FORWARD -p udp --dport 53 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT")
    run("iptables -A FORWARD -p udp --sport 53 -m state --state ESTABLISHED,RELATED -j ACCEPT")

    # Permitir DNS (TCP porta 53, para fallback)
    run("iptables -A FORWARD -p tcp --dport 53 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT")
    run("iptables -A FORWARD -p tcp --sport 53 -m state --state ESTABLISHED,RELATED -j ACCEPT")


    # Permitir HTTP de saída e respostas
    run("iptables -A FORWARD -p tcp --dport 80 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT")

    # Permitir HTTP de saída e respostas
    run("iptables -A FORWARD -p tcp --dport 80 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT")
    run("iptables -A FORWARD -p tcp --sport 80 -m state --state ESTABLISHED,RELATED -j ACCEPT")

    # Permitir HTTPS (TLS) de saída e respostas (Porta 443)
    run("iptables -A FORWARD -p tcp --dport 443 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT")
    run("iptables -A FORWARD -p tcp --sport 443 -m state --state ESTABLISHED,RELATED -j ACCEPT")

    run("iptables -A FORWARD -p icmp -o ens18 -j DROP")  # Bloquear ICMP externo

    run("iptables -A FORWARD -p icmp -i ens19 -o ens19 -j ACCEPT")  # Permitindo ICMP interno

    run("iptables -A FORWARD -p tcp -d 157.240.0.0/16 -j REJECT")  # Bloqueando Facebook
    run("iptables -A FORWARD -p tcp -d 31.13.0.0/16 -j REJECT")    # Bloqueando Instagram

    print("=== Firewall configurado com sucesso ===")

if __name__ == "__main__":
    configurar_firewall()
