import logging
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import BooleanVar
from tkinter import ttk  # Importando o módulo ttk
import socket

from functions.firewall import bloquear_no_firewall


caminho_pasta = os.path.dirname(os.path.abspath(__file__))
caminho_pasta_anterior = os.path.dirname(caminho_pasta)

sites_file = os.path.join(caminho_pasta_anterior, "blacklist.txt")

print(caminho_pasta_anterior)  # Para verificar o caminho resultante

print("Caminho da pasta: ", caminho_pasta)

def bloquear_sites(checkbox_var, lista, progresso,janela):
        
    """Bloqueia os sites listados na blacklist se o usuário concordar em participar da rede de apoio."""
    if not checkbox_var.get():
        messagebox.showwarning("Aviso", "Você precisa concordar em participar da rede de apoio.")
        return

    try:
        

        with open(sites_file, "r") as file:
            sites = file.readlines()
            if not sites:
                messagebox.showwarning("Aviso", "A lista de sites a serem bloqueados está vazia.")
                return
            
            total_sites = len(sites)
            for index, site in enumerate(sites):
                site = site.strip()  # Remove espaços em branco
                if site:  # Ignorar linhas vazias
                    if bloquear_no_firewall(site):
                        lista.delete(lista.get(0, tk.END).index(site))  # Remove o site da lista
                    else:
                        # messagebox.showwarning("Aviso", f"Não foi possível bloquear o site: {site}")
                        logging.warning(f"Não foi possível bloquear o site: {site}")
                
                # Atualiza a barra de progresso
                progresso['value'] = (index + 1) / total_sites * 100
                janela.update_idletasks()  # Atualiza a interface para mostrar a mudança

        messagebox.showinfo("Informação", "Sites bloqueados com sucesso.")
        progresso['value'] = 100  # Certifique-se de que a barra de progresso vá até o final

    except Exception as e:
        logging.error(f"Erro ao bloquear os sites: {e}").showerror("Erro", f"Não foi possível bloquear os sites: {e}")
