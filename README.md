# Projeto Arranjos de Sensores

Repositorio do trabalho de Processamento de Sinais I sobre modelagem e
analise de arranjos de sensores, vetor diretor, beampattern, beamforming e
transmissao direcional.

## Integrantes

- [Gabriel Florencio da Fonseca](https://github.com/florencio300)
- [Pedro Nicollas Pereira Azevedo Della Torre Bastos](https://github.com/Pogeu)
- [Ricardo Alexandre Vieira da Silva](https://github.com/RicardoV1e1r4)

## O que o projeto gera

- Geometrias 3D para ULA, UCA, UPA e arranjo cilindrico.
- Vetor diretor usando a formulação do enunciado.
- Beampatterns normalizados em dB.
- Beamformer convencional Delay-and-Sum.
- Canal de propagação LOS em espaço livre.
- Experimento de transmissão direcional com ULA transmissora e receptora.
- Painel reprodutível de aplicações em radar, sonar, comunicações sem fio,
  sistemas acústicos e Massive MIMO, montado com imagens externas creditadas.
- Figuras e tabelas usadas no artigo.
- Artigo técnico no padrão IEEE Conference, em duas colunas e com 4 páginas.

## Estrutura

```text
Projeto_Arranjos/
|-- article/
|   |-- paper.tex
|   |-- paper.pdf
|   |-- generated_results.tex
|-- data/
|-- docs/
|   |-- roteiro_apresentacao.md
|-- examples/
|-- figures/
|   |-- applications/
|-- src/
|   |-- generate_ula.py
|   |-- generate_uca.py
|   |-- generate_upa.py
|   |-- generate_ucya.py
|   |-- steering_vector.py
|   |-- beampattern.py
|   |-- beamformer.py
|   |-- channel.py
|   |-- application_figures.py
|-- tests/
|-- main.py
|-- requirements.txt
|-- README.md
```

## Dependências

- Python 3.11 ou superior.
- `numpy`
- `matplotlib`
- MiKTeX ou outra distribuicao LaTeX com `pdflatex` e `IEEEtran`.

Instalação recomendada:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

## Como reproduzir os resultados

Gerar figuras, arquivos de dados e tabelas do artigo:

```powershell
.\.venv\Scripts\python main.py
```

Gerar tudo e compilar o artigo:

```powershell
.\.venv\Scripts\python main.py --compile-paper
```

Se `latexmk` não estiver disponível, compile diretamente com:

```powershell
cd article
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

Executar testes basicos:

```powershell
.\.venv\Scripts\python -m unittest discover -s tests
```

Exemplos independentes:

```powershell
.\.venv\Scripts\python examples\run_single_beampattern.py
.\.venv\Scripts\python examples\run_transmission_sweep.py
.\.venv\Scripts\python examples\run_los_channel.py
```

As imagens externas usadas no painel estão versionadas em
`figures/applications/`. Para baixá-las novamente a partir das fontes e
licenças documentadas:

```powershell
.\.venv\Scripts\python examples\download_application_images.py
```

O `main.py` usa esses arquivos para gerar automaticamente
`figures/applications_overview.png`, que é a única figura de aplicações
incluída no artigo.

## Observações de modelagem

A ULA foi posicionada por padrão no eixo `z`. Com a convencao do enunciado
`u = [cos(theta)cos(phi), cos(theta)sin(phi), sin(theta)]`, isso faz com que
`theta = 0` represente o apontamento broadside no corte de elevação usado nos
gráficos ULA e na transmissão com `theta_T = 20 graus`.

A UPA foi posicionada no plano `xz`, usando `x` como eixo horizontal e `z`
como eixo vertical.

Para UCA, UPA e arranjo cilíndrico, os gráficos direcionais usam pesos
Delay-and-Sum apontados para uma direção de referência. Essa escolha permite
identificar lobulo principal, lobulos secundarios e largura de feixe nos cortes
solicitados.

O módulo `src/channel.py` implementa o canal estreito de espaço livre entre
cada par transmissor-receptor, incluindo atenuação de Friis e fase de
propagação. O experimento angular utiliza ganho normalizado para isolar o efeito
do apontamento.

## Apresentação oral

O roteiro de 20 minutos, a divisão entre os integrantes e os comandos da
demonstração estão em `docs/roteiro_apresentacao.md`.
