import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
import time

# Importar sv_ttk com tratamento de erros
try:
    import sv_ttk
    has_sv_ttk = True
except ImportError:
    has_sv_ttk = False
    print("Aviso: sv_ttk não encontrado. O tema Sun Valley não será aplicado.")

# Importar yt-dlp com tratamento de erros
try:
    import yt_dlp
except ImportError:
    messagebox.showerror("Erro de Dependência", "A biblioteca yt-dlp não está instalada. Por favor, instale usando 'pip install yt-dlp'")
    sys.exit(1)

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # Aplicar tema Sun Valley se disponível
        if has_sv_ttk:
            sv_ttk.set_theme("dark")

        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # URL input
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=10)

        ttk.Label(url_frame, text="URL do YouTube:").pack(side=tk.LEFT, padx=(0, 10))
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Botão para buscar informações do vídeo
        ttk.Button(url_frame, text="Buscar Vídeo", command=self.get_video_info).pack(side=tk.LEFT, padx=(10, 0))

        # Informações do vídeo
        info_frame = ttk.LabelFrame(main_frame, text="Informações do Vídeo", padding=10)
        info_frame.pack(fill=tk.X, pady=10)

        ttk.Label(info_frame, text="Título:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.title_label = ttk.Label(info_frame, text="")
        self.title_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(info_frame, text="Duração:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.duration_label = ttk.Label(info_frame, text="")
        self.duration_label.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Seleção de formato/resolução
        resolution_frame = ttk.LabelFrame(main_frame, text="Formato e Resolução", padding=10)
        resolution_frame.pack(fill=tk.X, pady=10)

        self.format_listbox = tk.Listbox(resolution_frame, height=5)
        self.format_listbox.pack(fill=tk.X, padx=5, pady=5)

        # Seleção de diretório para download
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=10)

        ttk.Label(path_frame, text="Local de download:").pack(side=tk.LEFT, padx=(0, 10))
        self.path_entry = ttk.Entry(path_frame, width=40)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.path_entry.insert(0, os.path.expanduser("~/Downloads"))

        ttk.Button(path_frame, text="Procurar", command=self.select_directory).pack(side=tk.LEFT, padx=(10, 0))

        # Botão de download (MOVIDO PARA CIMA)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        self.download_button = ttk.Button(button_frame, text="Baixar Vídeo", command=self.download_video, state=tk.DISABLED)
        self.download_button.pack(padx=5, pady=5, ipadx=10, ipady=5)

        # Barra de progresso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)

        self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)

        self.status_label = ttk.Label(progress_frame, text="")
        self.status_label.pack(pady=5)

        # Armazenar informações do vídeo
        self.video_info = None
        self.formats = None
        self.format_ids = []

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)

    def get_video_info(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL do YouTube.")
            return

        self.status_label.config(text="Buscando informações do vídeo...")
        self.download_button.config(state=tk.DISABLED)
        self.format_listbox.delete(0, tk.END)

        # Executar em uma thread separada para não travar a interface
        threading.Thread(target=self._fetch_video_info, args=(url,), daemon=True).start()

    # Funções auxiliares para atualizar UI (substituindo lambdas com atribuições)
    def _update_title(self, title):
        self.title_label.config(text=title)

    def _update_duration(self, duration):
        self.duration_label.config(text=duration)

    def _add_format_to_listbox(self, fmt):
        self.format_listbox.insert(tk.END, fmt)

    def _select_first_format(self):
        self.format_listbox.selection_set(0)

    def _enable_download_button(self):
        self.download_button.config(state=tk.NORMAL)

    def _update_status(self, text):
        self.status_label.config(text=text)

    def _show_error(self, message):
        messagebox.showerror("Erro", message)

    def _update_progress(self, percentage):
        self.progress_bar["value"] = percentage

    def _fetch_video_info(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.video_info = ydl.extract_info(url, download=False)

            # Atualizar informações na interface principal
            self.root.after(0, lambda: self._update_title(self.video_info.get('title', 'Desconhecido')))

            # Calcular duração formatada
            duration_seconds = self.video_info.get('duration', 0)
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            duration_str = f"{minutes}:{seconds:02}"

            self.root.after(0, lambda: self._update_duration(duration_str))

            # Obter formatos disponíveis
            self.formats = []
            self.format_ids = []

            # Adicionar formatos com vídeo e áudio (mp4, webm)
            video_formats = []
            for f in self.video_info.get('formats', []):
                if f.get('vcodec', 'none') != 'none' and f.get('acodec', 'none') != 'none':
                    format_str = f"{f.get('format_note', '')} - {f.get('ext', '')} - {f.get('resolution', '')}"
                    if format_str not in video_formats:
                        video_formats.append(format_str)
                        self.formats.append(format_str)
                        self.format_ids.append(f.get('format_id', ''))

            # Adicionar formato áudio apenas (mp3)
            for f in self.video_info.get('formats', []):
                if f.get('vcodec', 'none') == 'none' and f.get('acodec', 'none') != 'none':
                    format_str = f"Áudio - {f.get('ext', '')} - {f.get('abr', '')}kbps"
                    if format_str not in video_formats:  # Evitar duplicatas
                        self.formats.append(format_str)
                        self.format_ids.append(f.get('format_id', ''))
                    break  # Apenas adicionar o melhor áudio

            # Atualizar listbox
            for fmt in self.formats:
                self.root.after(0, lambda f=fmt: self._add_format_to_listbox(f))

            if self.formats:
                self.root.after(0, self._select_first_format)
                self.root.after(0, self._enable_download_button)

            self.root.after(0, lambda: self._update_status("Pronto para download."))

        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Não foi possível obter informações do vídeo: {str(e)}"))
            self.root.after(0, lambda: self._update_status("Erro ao buscar informações."))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            # Calcular progresso
            total_bytes = d.get('total_bytes')
            if total_bytes is None:
                total_bytes = d.get('total_bytes_estimate', 0)

            if total_bytes > 0:
                downloaded_bytes = d.get('downloaded_bytes', 0)
                percentage = (downloaded_bytes / total_bytes) * 100

                # Atualizar barra de progresso
                self.root.after(0, lambda p=percentage: self._update_progress(p))
                self.root.after(0, lambda p=percentage: self._update_status(f"Baixando... {p:.1f}%"))
                self.root.update_idletasks()

        elif d['status'] == 'finished':
            self.root.after(0, lambda: self._update_status("Download concluído. Convertendo..."))

    def download_video(self):
        if not self.video_info or not self.formats:
            messagebox.showerror("Erro", "Nenhum vídeo foi selecionado.")
            return

        selected_indices = self.format_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Erro", "Selecione um formato.")
            return

        selected_index = selected_indices[0]
        selected_format_id = self.format_ids[selected_index]

        download_path = self.path_entry.get()
        if not download_path or not os.path.exists(download_path):
            messagebox.showerror("Erro", "Diretório de download inválido.")
            return

        # Desativar botão durante o download
        self.download_button.config(state=tk.DISABLED)
        self.status_label.config(text="Iniciando download...")

        # Resetar barra de progresso
        self.progress_bar['value'] = 0

        # Iniciar download em uma thread separada
        threading.Thread(target=self._download_video, args=(selected_format_id, download_path), daemon=True).start()

    def _download_video(self, format_id, download_path):
        try:
            # Verificar se é formato de áudio
            is_audio_only = "Áudio" in self.formats[self.format_ids.index(format_id)]

            ydl_opts = {
                'format': format_id,
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
            }

            # Se for somente áudio, converter para mp3
            if is_audio_only:
                ydl_opts.update({
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.video_info['webpage_url']])

            # Atualizar interface ao terminar
            self.root.after(0, lambda: self._update_status("Download concluído com sucesso!"))
            self.root.after(0, self._enable_download_button)
            self.root.after(0, lambda: messagebox.showinfo("Sucesso", "Download concluído com sucesso!"))

        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Erro ao baixar o vídeo: {str(e)}"))
            self.root.after(0, lambda: self._update_status("Erro durante o download."))
            self.root.after(0, self._enable_download_button)

# Função para encontrar recursos quando compilado com pyinstaller
def resource_path(relative_path):
    """ Obter caminho absoluto para recursos, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria um diretório temporário e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
