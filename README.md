🎬 youTubeDownloader

# 🎬 YouTube Downloader

[![Download Latest Release](https://img.shields.io/github/v/release/TheLastEnvoy/youtubeDownloader?style=for-the-badge&logo=github&label=Download)](https://github.com/TheLastEnvoy/youtubeDownloader/releases/latest)

Clique no link acima para baixar o executável já compilado com o PyInstaller, pronto para uso!

✨ Funcionalidades

    🔍 Busca rápida de informações de vídeos por URL
    📋 Visualização detalhada do título e duração
    🎞️ Disponível em MP4 e WebM (com áudio)
    📂 Seleção personalizada do diretório de download
    🌙 Tema escuro integrado (Sun Valley)
    🧵 Processamento multithreading para uma experiência fluida

📋 Requisitos

    Python 3.6+
    Bibliotecas:
        tkinter (geralmente incluído com Python)
        yt-dlp
        sv_ttk (opcional, para o tema Sun Valley)

🚀 Instalação

    Clone este repositório:

Bash

git clone https://github.com/seu-usuario/youtube-downloader.git
cd youtube-downloader

Instale as dependências:
Bash

pip install yt-dlp sv_ttk

Execute o aplicativo:

    Bash

    python main.py

📖 Como usar

    Cole a URL do vídeo do YouTube no campo de entrada
    Clique em "Buscar Vídeo" para carregar as informações
    Selecione o formato desejado na lista
    Escolha o diretório de destino (padrão: ~/Downloads)
    Clique em "Baixar Vídeo" para iniciar o download
    Acompanhe o progresso pela barra e mensagens de status

🔧 Tecnologias utilizadas

    Python: Linguagem de programação principal
    Tkinter: Framework para interface gráfica
    yt-dlp: Biblioteca para download de conteúdo do YouTube
    sv_ttk: Tema moderno para a interface Tkinter
    Threading: Processamento assíncrono para melhor desempenho

🛠️ Estrutura do projeto

O aplicativo foi desenvolvido com uma arquitetura limpa e modular:

    Classe YouTubeDownloader: Gerencia toda a lógica da aplicação
    Interface responsiva: Adaptável a diferentes tamanhos de tela
    Tratamento de erros: Mensagens amigáveis para o usuário
    Multithreading: Impede o congelamento da interface durante downloads

🤝 Contribuição

Contribuições são bem-vindas! Siga estes passos:

    Faça um fork do projeto
    Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade)
    Faça commit das mudanças (git commit -m 'Adiciona nova funcionalidade')
    Envie para o GitHub (git push origin feature/nova-funcionalidade)
    Abra um Pull Request

📜 Licença

Está sob a licença "Unlicense", aproveite como quiser.

⭐ Desenvolvido por The Last Envoy
