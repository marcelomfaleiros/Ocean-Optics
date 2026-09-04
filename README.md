Ocean Optics

Aplicações em Python para aquisição, visualização e registro de espectros utilizando espectrômetros Ocean Optics.
O projeto fornece interfaces gráficas para realizar medições espectrais, acompanhar o espectro em tempo real, executar aquisições contínuas e realizar séries temporais de espectros. A comunicação com o espectrômetro é feita por meio da biblioteca SeaBreeze, enquanto a interface gráfica e a visualização dos dados utilizam PyQt/PyQtGraph. GGitHub+1

✨ Funcionalidades
    • Conexão automática com o primeiro espectrômetro Ocean Optics disponível.
    • Configuração do tempo de integração em milissegundos.
    • Aquisição de espectros individuais.
    • Visualização do espectro em tempo real.
    • Modo Free Run para monitoramento contínuo.
    • Correção de dark counts durante a aquisição.
    • Visualização de intensidade em função do comprimento de onda.
    • Salvamento dos espectros adquiridos em arquivos de texto.
    • Aquisição de múltiplos espectros em intervalos de tempo definidos.
    • Suporte a séries temporais de medidas.
    • Interface gráfica baseada em Qt.
    • Na versão mais recente da aplicação de dinâmica, as aquisições são executadas em uma QThread, evitando bloquear a interface durante medições prolongadas. GGitHub+2
    
📁 Estrutura do projeto
Ocean-Optics/
│
├── basics/
│   ├── ocean_optics_interface.py
│   ├── ocean_optics_spectrometer.py
│   └── ocean_optics_spectrometer.pyw
│
├── dynamics/
│   ├── ocean_optics_intrfc_dynamics.py
│   ├── ocean_optics_spctrntr_dynamics_v2.py
│   └── ocean_optics_spctrntr_dynamics_v3.pyw
│
├── ocean_optics_interface.ui
├── ocean_optics_intrfc_dynamics.ui
├── LICENSE
└── README.md
As aplicações estão organizadas em dois grupos principais: basics, destinado às medições espectrais básicas, e dynamics, voltado para aquisições de espectros ao longo do tempo. GGitHub+2

🔬 Aplicação básica
A aplicação localizada em basics/ fornece uma interface simples para aquisição de espectros.
A interface disponibiliza:
    • Integration time (ms) — tempo de integração;
    • Measure — realiza uma aquisição;
    • Free run — atualiza continuamente o espectro;
    • Save — salva os dados adquiridos;
    • Clear — limpa o gráfico;
    • Exit — encerra a aplicação. GGitHub+1
Durante a aquisição, o programa obtém os comprimentos de onda através de wavelengths() e as intensidades através de intensities(), utilizando correção de dark counts. Os dados são então apresentados graficamente através do PyQtGraph. GGitHub
Dados salvos
Os dados de uma medição são organizados em duas colunas:
wavelength    intensity
onde:
    • wavelength corresponde ao comprimento de onda em nanômetros (nm);
    • intensity corresponde à intensidade medida pelo espectrômetro.
    
⏱️ Aplicação para medidas dinâmicas
A pasta dynamics/ contém aplicações destinadas à aquisição de múltiplos espectros ao longo do tempo.
O usuário pode configurar:
    • Integration time (ms) — tempo de integração de cada espectro;
    • Number of spectra — número de espectros;
    • Time step (seconds) — intervalo entre aquisições.
A versão v2 implementa a aquisição sequencial diretamente no fluxo da aplicação. A versão v3, por sua vez, introduz uma QThread e sinais Qt para executar a aquisição separadamente da interface gráfica, proporcionando uma experiência mais responsiva durante experimentos de maior duração. GGitHub+1
Os valores padrão da aplicação dinâmica são:
Integration time: 10 ms
Number of spectra: 5
Time step: 1 s
Esses valores podem ser alterados diretamente na interface. GGitHub+1

🧰 Requisitos
O projeto utiliza Python e as seguintes bibliotecas:
    • NumPy — manipulação dos dados numéricos;
    • PyQt5 / Qt — interface gráfica;
    • PyQtGraph — visualização dos espectros;
    • SeaBreeze — comunicação com o espectrômetro;
    • keyboard — detecção da tecla Esc para interromper aquisições contínuas. GGitHub+2
Também é necessário possuir um espectrômetro compatível com a biblioteca SeaBreeze conectado ao computador.

🚀 Instalação
Clone o repositório:
git clone https://github.com/marcelomfaleiros/Ocean-Optics.git
cd Ocean-Optics
Recomenda-se utilizar um ambiente virtual:
python -m venv .venv
Ative o ambiente virtual.

Linux/macOS
source .venv/bin/activate

Windows
.venv\Scripts\activate

Instale as dependências:
pip install numpy pyqt5 pyqtgraph seabreeze keyboard

Observação: a comunicação com o equipamento depende do suporte fornecido pelo SeaBreeze e da compatibilidade do espectrômetro utilizado.

▶️ Executando a aplicação básica
Entre na pasta basics:
cd basics
Execute:
python ocean_optics_spectrometer.py
A aplicação inicializa a interface gráfica e tenta localizar automaticamente o primeiro espectrômetro disponível através de:
Spectrometer.from_first_available()
GGitHub

▶️ Executando a aplicação dinâmica
Entre na pasta dynamics:
cd dynamics
Para utilizar a versão 2:
python ocean_optics_spctrntr_dynamics_v2.py
Para utilizar a versão 3:
python ocean_optics_spctrntr_dynamics_v3.pyw
A versão 3 utiliza uma thread dedicada para a aquisição dos dados, emitindo os espectros para a interface gráfica através de sinais Qt. GGitHub

📊 Fluxo de aquisição
O fluxo básico da aplicação é:
┌─────────────────────────────┐
│ Espectrômetro Ocean Optics  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          SeaBreeze          │
│ Comunicação com equipamento │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Aquisição Python      │
│ wavelength + intensity      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Processamento        │
│  NumPy + correções básicas  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       PyQtGraph / Qt        │
│    Visualização do espectro │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Arquivo de dados      │
└─────────────────────────────┘

🛑 Interrompendo uma aquisição contínua
O modo Free Run pode ser interrompido pressionando a tecla:
Esc
O código verifica continuamente o estado dessa tecla durante a aquisição. GGitHub+2

💾 Salvando os dados
Após uma aquisição, utilize o botão Save para escolher o arquivo de destino.
Os dados são gravados utilizando numpy.savetxt(). Na aplicação dinâmica, os espectros são organizados de forma que os diferentes instantes da aquisição possam ser posteriormente analisados como uma série temporal. GGitHub+2

🧪 Aplicações
O projeto pode ser utilizado como base para experimentos que envolvam:
    • espectroscopia óptica;
    • caracterização de fontes luminosas;
    • acompanhamento temporal de espectros;
    • experimentos de cinética;
    • monitoramento de processos;
    • aquisição de dados para posterior análise científica;
    • desenvolvimento de aplicações personalizadas para espectrômetros Ocean Optics.
    
🔧 Personalização
As interfaces gráficas são definidas em arquivos .ui, permitindo que a aparência e os componentes da aplicação sejam modificados utilizando o Qt Designer.
Os arquivos Python gerados a partir das interfaces devem ser tratados com cuidado, pois alterações manuais em arquivos gerados pelo pyuic5 podem ser sobrescritas quando a interface for regenerada. GGitHub

⚠️ Observações
O projeto é voltado principalmente para uso experimental e pode exigir adaptações de acordo com:
    • modelo do espectrômetro;
    • sistema operacional;
    • versão do Python;
    • versão das bibliotecas;
    • configuração dos drivers;
    • características específicas do equipamento.
Alguns modelos de espectrômetros podem apresentar comportamentos diferentes durante a aquisição. O código atual também contém tratamentos específicos para determinados dispositivos, como o USB2000PLUS. GGitHub

🤝 Contribuindo
Contribuições são bem-vindas.
Para contribuir:
    1. Faça um fork do projeto.
    2. Crie uma branch para sua alteração:
git checkout -b feature/minha-alteracao
    3. Faça as modificações.
    4. Teste a aplicação com um espectrômetro compatível.
    5. Faça commit das alterações:
git commit -m "Adiciona nova funcionalidade"
    6. Envie a branch:
git push origin feature/minha-alteracao
    7. Abra um Pull Request.
    
📄 Licença
Este projeto está distribuído sob a licença MIT.
Copyright © 2023 Marcelo Meira Faleiros. GGitHub
A licença permite usar, copiar, modificar, distribuir e sublicenciar o software, respeitando as condições estabelecidas no arquivo LICENSE.

📚 Referência
Se este software for utilizado em um trabalho acadêmico ou científico, recomenda-se citar o repositório original:
Faleiros, Marcelo Meira. Ocean-Optics. GitHub.
Repositório: github.com/marcelomfaleiros/Ocean-Optics
