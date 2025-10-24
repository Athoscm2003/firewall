# Firewall Didático (iptables) — Projeto de Segurança Computacional

## Objetivo
Implementar e testar um firewall simples em um roteador Linux (Roteador 1) usando `iptables`, com as seguintes políticas:
- Permitir conexões HTTP de saída e suas respostas.
- Bloquear solicitações ICMP externas (ping/traceroute), mas permitir ICMP interno.
- Bloquear acesso a duas redes sociais. (Foram escolhidos Facebook e Instagram)

## Como usar
1. Rodar o script como root:
   ```bash
   sudo python3 firewall.py
2. Agora o firewall está configurado e rodando

3. Para reverter às configurações padrão, basta rodar o script de reversão como root:
   ```bash
   sudo python3 revert.py