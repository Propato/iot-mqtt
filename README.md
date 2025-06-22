# Internet Of Things

Este é o projeto do seminário sobre MQTT da disciplina de IoT (Internet Of Things). Desenvolvido por David Propato (<a href="https://github.com/Propato">@Propato</a>), Klarine Mendonça (<a href="https://github.com/Klarinemend">@Klarinemend</a>), Pedro (<a href="https://github.com/Pedro2um">@Pedro2um</a>) e Rhuan (<a href="https://github.com/gnizamaaa">@gnizamaaa</a>).

## MQTT - Message Queuing Telemetry Transport

A Internet das Coisas (IoT) tem revolucionado a forma como interagimos com o mundo digital, conectando uma miríade de dispositivos que coletam, processam e trocam dados. Nesse ecossistema, o protocolo MQTT (Message Queuing Telemetry Transport) emergiu como um padrão de fato para a comunicação entre dispositivos e aplicações, principalmente devido à sua leveza, eficiência e modelo de publicação/assinatura, que é ideal para ambientes com restrições de rede e de recursos.

A implantação tradicional, via execução nativa, vincula o processo do broker diretamente ao sistema operacional do host. Embora minimize teoricamente a sobrecarga, essa abordagem é frágil. Ela sofre de uma falta de portabilidade e reprodutibilidade, criando um acoplamento rígido. Para mitigar esses riscos, a estratégia proposta é a conteinerização via Docker.

### Objetivos

O objetivo principal deste trabalho é analisar e caracterizar a escalabilidade do broker MQTT Mosquitto quando executado em uma instalação conteinerizada com Docker.

Para alcançar este objetivo principal, foram definidos os seguintes objetivos específicos:

- Avaliar o limite de payload da mensagem
- Analisar a escalabilidade com aumento de publishers
- Investigar a escalabilidade com carga combinada de publishers e subscribers
- Identificar gargalos de desempenho
- Observar o impacto da conteinerização

## Pré-requisitos

> Neste projeto o Broker foi executado dentro de uma Raspberry, para melhor simular um ambiente IoT.

### Broker Mosquitto em Contêiner Docker

|      Tool      | Version |
| :------------: | :-----: |
|     Docker     | 28.2.2  |
| Docker Compose | 2.34.0  |

### Broker Mosquitto em Execução Nativa

|     Tool      | Version |
| :-----------: | :-----: |
| libmosquitto  | 2.0.11  |
| mosquitto_pub | 2.0.11  |
| mosquitto_sub | 2.0.11  |

### Client (Publishers/Subscribers)

|     Tool      | Version |
| :-----------: | :-----: |
|    Python     | 3.12.3  |
| libmosquitto  | 2.0.11  |
| mosquitto_pub | 2.0.11  |
| mosquitto_sub | 2.0.11  |

### Gráficos

|  Tool   | Version |
| :-----: | :-----: |
| gnuplot |   6.0   |

Requisitos de bibliotecas do Python podem ser vistas no <a href="./requirements.txt">requirements.txt</a>.

## Executando

### Broker Mosquitto em Contêiner Docker

#### Start

```bash
cd docker
docker compose up -d
```

#### Stop

```bash
cd docker
docker compose down
```

### Broker Mosquitto em Execução Nativa

#### Start

```bash
mosquitto -c ./docker/config/mosquitto.conf -v
```

#### Stop

```bash
Ctrl + C
```

### Clients

#### Subscribers

##### Start

```bash
python3 subscribers.py <host> <tópico> -n <número de subscribers>
```

##### Stop

```bash
Ctrl + C
```

#### Publishers

##### Start

Para fazer uma publicação a cada X períodos de tempo:

```bash
python3 publisher_2.py <intervalo> <host> <tamanho> <tópico>
```

Para enviar múltiplas publicações simultâneas:

```bash
python3 publisher_multi.py <intervalo> <host> <tamanho> <tópico> -n <número de publishers>
```

##### Stop

```bash
Ctrl + C
```

## Resultados

### Logs

Com o broker ativo, é executado os arquivos de publishers e subscribers e é monitorado o uso da CPU e memória através do <a href="./loglog.py">loglog.py</a>, que gera um CSV com diversas informações.

#### Start

```bash
python3 loglog.py --pid <pid> --container <container> -i <interval>
```

Passando o PId ou o nome do container que roda o broker e o intervalo de tempo das amostras.

##### Stop

```bash
Ctrl + C
```

### Gráficos

Com o arquivo CSV criado, basta inserir o nome do arquivo no <a href="./plot.ipynb">plot.ipynb</a> e executa-lo dentro do próprio notebook. Há diversos comentários descrevendo sobre as funcionalidades dentro do código.
