import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime

# ================= CONFIG =================
CATEGORIAS = {
    "Imagens": [".png", ".jpg", ".jpeg", ".gif"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Documentos": [".pdf", ".txt", ".docx"],
    "Musicas": [".mp3", ".wav"],
    "Compactados": [".zip", ".rar", ".7z"],
    "Programas": [".exe", ".msi"]
}

# ================= FUNÇÕES =================

def log(msg):
    caixa_log.insert(tk.END, msg + "\n")
    caixa_log.see(tk.END)

def escolher_pasta():
    pasta = filedialog.askdirectory()
    entry_pasta.delete(0, tk.END)
    entry_pasta.insert(0, pasta)

def organizar():
    pasta = entry_pasta.get()

    if not os.path.exists(pasta):
        log("❌ Pasta inválida")
        return

    arquivos = os.listdir(pasta)
    total = len(arquivos)

    progresso["maximum"] = total
    progresso["value"] = 0

    movidos = 0

    for i, arquivo in enumerate(arquivos):
        caminho = os.path.join(pasta, arquivo)

        if os.path.isfile(caminho):
            for categoria, ext in CATEGORIAS.items():
                if any(arquivo.lower().endswith(e) for e in ext):
                    destino = os.path.join(pasta, categoria)
                    os.makedirs(destino, exist_ok=True)

                    try:
                        shutil.move(caminho, os.path.join(destino, arquivo))
                        log(f"✔ {arquivo} → {categoria}")
                        movidos += 1
                    except:
                        log(f"⚠ Erro ao mover {arquivo}")
                    break

        progresso["value"] = i + 1
        janela.update_idletasks()

    log(f"\n🔥 FINALIZADO: {movidos} arquivos organizados\n")
    salvar_log()

def limpar_temp():
    temp = os.getenv("TEMP")
    apagados = 0

    for arquivo in os.listdir(temp):
        caminho = os.path.join(temp, arquivo)
        try:
            if os.path.isfile(caminho):
                os.remove(caminho)
                apagados += 1
            else:
                shutil.rmtree(caminho)
                apagados += 1
        except:
            pass

    log(f"🧹 {apagados} arquivos temporários removidos")

def salvar_log():
    with open("historico.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- {datetime.now()} ---\n")
        f.write(caixa_log.get("1.0", tk.END))

# ================= INTERFACE =================

janela = tk.Tk()
janela.title("FileSmart PRO")
janela.geometry("650x500")
janela.configure(bg="#121212")

# Título
titulo = tk.Label(janela, text="📂 FileSmart PRO", font=("Arial", 18, "bold"), bg="#121212", fg="#00ffcc")
titulo.pack(pady=10)

# Entrada
frame_top = tk.Frame(janela, bg="#121212")
frame_top.pack()

entry_pasta = tk.Entry(frame_top, width=45, bg="#1e1e1e", fg="white", insertbackground="white")
entry_pasta.grid(row=0, column=0, padx=5)

btn_pasta = tk.Button(frame_top, text="Procurar", command=escolher_pasta, bg="#333", fg="white")
btn_pasta.grid(row=0, column=1)

# Botões
frame_btn = tk.Frame(janela, bg="#121212")
frame_btn.pack(pady=10)

btn_org = tk.Button(frame_btn, text="🚀 Organizar", command=organizar, bg="#00aa88", fg="white", width=15)
btn_org.grid(row=0, column=0, padx=5)

btn_temp = tk.Button(frame_btn, text="🧹 Limpar Temp", command=limpar_temp, bg="#aa3333", fg="white", width=15)
btn_temp.grid(row=0, column=1, padx=5)

# Barra progresso
progresso = ttk.Progressbar(janela, length=500)
progresso.pack(pady=10)

# Log
caixa_log = tk.Text(janela, height=15, bg="#1e1e1e", fg="#00ffcc")
caixa_log.pack(padx=10, pady=10, fill="both", expand=True)

janela.mainloop()