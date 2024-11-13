import os
import logging
import socket
import re

def resolver_ipv4(dominio):
    """Resolve um domínio para um endereço IPv4."""
    try:
        # Forçando a resolução para IPv4
        ip = socket.gethostbyname(dominio)
        logging.info(f"{dominio} resolvido para {ip}.")
        return ip
    except Exception as e:
        logging.error(f"Falha ao resolver {dominio} para IPv4: {e}")
        return None

def bloquear_no_firewall(dominio):
    try:
        # Obter o IP do domínio
        output = resolver_ipv4(dominio)
        
        # Verifica se o IP é válido
        if not output:
            logging.error(f"Domínio não encontrado ou IP inválido: {dominio}.")
            return False  # Indica que o bloqueio falhou
        
        # Criar a regra de bloqueio no firewall
        regra = f'netsh advfirewall firewall add rule name="Bloqueio de {dominio}" protocol=TCP dir=OUT remoteip={output} action=block profile=any'
        os.system(regra)
        logging.info(f"Regra de bloqueio adicionada para {dominio}.")
        return True  # Indica que o bloqueio foi bem-sucedido
    except Exception as e:
        logging.error(f"Falha ao adicionar regra de bloqueio para {dominio}: {e}")
        return False  # Indica que o bloqueio falhou
