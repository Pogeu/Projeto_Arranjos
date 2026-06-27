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
- Experimento de transmissão direcional com ULA transmissora e receptora.
- Seção de aplicações em radar, sonar, comunicações sem fio, sistemas
  acústicos e Massive MIMO, com imagens externas creditadas e licenciadas.
- Figuras e tabelas usadas no artigo.
- Artigo tecnico em `article/paper.pdf`.

## Estrutura

```text
Projeto_Arranjos/
|-- article/
|   |-- paper.tex
|   |-- paper.pdf
|   |-- generated_results.tex
|-- data/
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
```

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
