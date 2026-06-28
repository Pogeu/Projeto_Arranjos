# Roteiro da apresentação oral

Duração total: 20 minutos. Todos os integrantes participam e devem conseguir
explicar o código, a modelagem matemática e os resultados.

## 0 a 6 minutos - Gabriel

- Objetivo do trabalho e aplicações de processamento espacial.
- Geometrias ULA, UCA, UPA e arranjo cilíndrico.
- Vetor diretor, DoA, fator de arranjo e beampattern.
- Significado físico de lóbulo principal, HPBW e lóbulos secundários.

## 6 a 14 minutos - Pedro

- Funções de geração das geometrias e canal LOS.
- Implementação do beamformer Delay-and-Sum.
- Comparação dos beampatterns e das métricas HPBW/SLL.
- Demonstração: executar `python main.py` e mostrar os arquivos gerados.

## 14 a 20 minutos - Ricardo

- Experimento de transmissão e recepção direcionais.
- Efeito do desalinhamento sobre potência, ganho e correlação.
- Separação de duas fontes e influência do número de sensores.
- Vantagens, limitações e conclusões.

## Comandos para a demonstração

```powershell
.\.venv\Scripts\python -m unittest discover -s tests
.\.venv\Scripts\python main.py --compile-paper
.\.venv\Scripts\python examples\run_transmission_sweep.py
```

Antes da apresentação, cada integrante deve revisar as equações e executar os
exemplos sem consultar o roteiro.
