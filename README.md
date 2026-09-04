Ocean Optics

Aplicações em Python para aquisição, visualização e registro de espectros utilizando espectrômetros Ocean Optics.

O projeto fornece interfaces gráficas para realizar medições espectrais, acompanhar o espectro em tempo real, executar aquisições contínuas e realizar séries temporais de espectros.

✨ Funcionalidades
Conexão com espectrômetros Ocean Optics compatíveis.
Configuração do tempo de integração.
Aquisição de espectros individuais.
Visualização do espectro em tempo real.
Modo Free Run para monitoramento contínuo.
Correção de dark counts durante a aquisição.
Visualização da intensidade em função do comprimento de onda.
Salvamento dos espectros adquiridos.
Aquisição de múltiplos espectros em intervalos de tempo definidos.
Suporte a séries temporais de medidas.
Interface gráfica baseada em Qt.
Aquisição em QThread na versão mais recente da aplicação dinâmica, mantendo a interface responsiva durante medições prolongadas.
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


O projeto está dividido principalmente em duas partes:

basics/ — aplicações para aquisição e visualização de espectros.
dynamics/ — aplicações para aquisição de múltiplos espectros ao longo do tempo.
🔬 Aplicação básica

A aplicação localizada em basics/ fornece uma interface para aquisição de espectros.

Principais controles:

Integration time (ms) — define o tempo de integração.
Measure — realiza uma aquisição.
Free run — realiza aquisições continuamente.
Save — salva os dados adquiridos.
Clear — limpa o gráfico.
Exit — encerra a aplicação.

Os dados adquiridos consistem em comprimento de onda e intensidade.

⏱️ Aquisição dinâmica

A pasta dynamics/ contém aplicações destinadas à aquisição de múltiplos espectros ao longo do tempo.

É possível configurar:

Integration time (ms) — tempo de integração de cada espectro.
Number of spectra — número de espectros a serem adquiridos.
Time step (seconds) — intervalo entre as aquisições.

A versão mais recente utiliza QThread para executar a aquisição separadamente da interface gráfica, evitando que a aplicação fique congelada durante experimentos mais longos.

🧰 Requisitos

O projeto utiliza Python e bibliotecas como:

NumPy
PyQt5
PyQtGraph
SeaBreeze
keyboard

Também é necessário possuir um espectrômetro compatível com o SeaBreeze.

🚀 Instalação

Clone o repositório:

git clone https://github.com/marcelomfaleiros/Ocean-Optics.git
cd Ocean-Optics


Recomenda-se utilizar um ambiente virtual:

python -m venv .venv

Linux / macOS
source .venv/bin/activate

Windows
.venv\Scripts\activate


Instale as dependências:

pip install numpy pyqt5 pyqtgraph seabreeze keyboard


A comunicação com o equipamento depende da compatibilidade do espectrômetro e da configuração do SeaBreeze no sistema operacional.

▶️ Executando a aplicação básica

Entre na pasta basics:

cd basics


Execute:

python ocean_optics_spectrometer.py


A aplicação tenta localizar automaticamente um espectrômetro disponível.

▶️ Executando a aplicação dinâmica

Entre na pasta dynamics:

cd dynamics


Para executar a versão 2:

python ocean_optics_spctrntr_dynamics_v2.py


Para executar a versão 3:

python ocean_optics_spctrntr_dynamics_v3.pyw

📊 Fluxo de aquisição
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
│            NumPy            │
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

🛑 Interrompendo uma aquisição

Durante o modo Free Run, a aquisição pode ser interrompida utilizando a tecla:

Esc

💾 Salvando os dados

Após realizar uma aquisição, utilize o botão Save para selecionar o arquivo de destino.

Os dados são salvos em formato de texto e podem ser posteriormente analisados utilizando Python, MATLAB, Origin ou outras ferramentas de análise científica.

🧪 Aplicações

O projeto pode ser utilizado como base para:

Espectroscopia óptica.
Caracterização de fontes luminosas.
Monitoramento temporal de espectros.
Experimentos de cinética.
Monitoramento de processos.
Aquisição de dados para análise científica.
Desenvolvimento de aplicações personalizadas para espectrômetros Ocean Optics.
🔧 Personalização

As interfaces gráficas são definidas nos arquivos .ui, que podem ser editados utilizando o Qt Designer.

Isso permite modificar a aparência da aplicação e adicionar ou remover componentes da interface.

⚠️ Observações

O funcionamento pode variar de acordo com:

Modelo do espectrômetro.
Sistema operacional.
Versão do Python.
Versões das bibliotecas utilizadas.
Drivers e configuração do equipamento.
Características específicas do espectrômetro.

Alguns modelos podem exigir configurações ou tratamentos específicos durante a aquisição.

🤝 Contribuindo

Contribuições são bem-vindas.

Para contribuir:

Faça um fork do projeto.
Crie uma nova branch:
git checkout -b feature/minha-alteracao

Faça suas alterações.
Teste a aplicação com um espectrômetro compatível.
Faça o commit:
git commit -m "Adiciona nova funcionalidade"

Envie a branch:
git push origin feature/minha-alteracao

Abra um Pull Request.
📄 Licença

Este projeto está distribuído sob a licença MIT.

Consulte o arquivo LICENSE para obter os detalhes completos da licença.

📚 Referência

Marcelo Meira Faleiros — Ocean-Optics

Repositório:

https://github.com/marcelomfaleiros/Ocean-Optics

Ocean Optics — aquisição e visualização de espectros em Python.
