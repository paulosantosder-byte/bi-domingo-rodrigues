# -*- coding: utf-8 -*-
import json, os

DATA = "2026-06-30"
HORA = "14:35"
TIPO = "analise_completa_tarde"

report = {
  "data": DATA,
  "hora_execucao": HORA,
  "tipo_analise": TIPO,
  "observacao_geral": (
    "DR4 (152352) ACESSIVEL. DR2 (175001) NAO verificado nesta analise (a pedido da diretoria) - "
    "ultimo status conhecido em 26/06 = plano expirado (13o dia fora do ar). "
    "Censo DR4: 40 linhas HH:MM (06:14-14:25); excluidos 2 feeds 'Chegou um lead' (Yan Sobral, 558781463639) "
    "e 1 'Paulo Junior -Ignorar' = 37 conversas reais. Substantivas/inbound/respondentes lidas a fundo via "
    "extracao DOM (clique por nome + leitura no-scroll). Yan Francisco domina (24 conversas, 12 disparos puros "
    "de template + 12 leads ativos); Alan Oliveira sem conversa solo (co-atende visitas com Yan). "
    "Keanny Brandao 11 + Lucas 2 (SDRs). NOVIDADE: Yan adotou template de URGENCIA FALSA "
    "('diretor liberou desconto para os 3 proximos projetos fechados hoje')."
  ),
  "metricas": {
    "total_conversas": 37,
    "total_conversas_dr4": 37,
    "total_conversas_dr2": 0,
    "total_ligacoes": 4,
    "sem_resposta": 3,
    "criticas": 1,
    "sem_vendedor": 0,
    "nota_media_sdr": 4.8,
    "nota_media_vendedor": 4.8,
    "aderencia_geral": 42
  },
  "sdrs": [
    {
      "nome": "Keanny Brandão (Keane)", "cor": "#f59e0b", "papel": "SDR",
      "total_conversas": 11, "ligacoes_dia": 0, "visitas_agendadas": 1,
      "taxa_conversao": 9, "mediana_resposta_min": 60, "media_resposta_min": 240,
      "qualidade": {
        "nota_media": 6.0, "aderencia_script": 60,
        "etapas_cumpridas": {"SDR-1_abertura": 11, "SDR-2_qualificacao": 6, "SDR-3_quebra_objecao": 1, "SDR-4_agendamento": 1},
        "pontos_fortes": [
          {"categoria": "Oferta de visita tecnica (SDR-4)", "descricao": "Oferece visita tecnica presencial com horario concreto",
           "exemplos": [
             "Cliente Rafael (Petrolina): ofereceu ligacao OU visita tecnica as 16h ('garantimos que nao haja intercorrencia no projeto')",
             "Cliente Adalberto (Petrolina): follow-up apos cliente pedir para falar no dia seguinte"]},
          {"categoria": "Qualificacao de inbound (SDR-2)", "descricao": "Responde inbounds e coleta dados",
           "exemplos": [
             "Cliente Italo Alves: inbound R$350/mes + CPF para analise de financiamento, retornou 'vejo agora mesmo'",
             "Cliente Sheila: inbound 'quero economizar com energia solar', perguntou regiao"]}
        ],
        "pontos_fracos": [
          {"categoria": "Orcamento prometido nao entregue", "descricao": "Promete preparar orcamento e some por dias",
           "impacto": "Cliente quente esfria e passa a cobrar", "conversas_afetadas": 1,
           "exemplos_clientes": ["Cliente Andre Martins (Cupira-PE, usina 300-350kW/mes): Keanny disse 'vou preparar e entro em contato logo em seguida' em 25/06; 5 dias depois (30/06 14:17) o cliente cobra 'Conseguiu fechar o orcamento?'"],
           "acao_corretiva": "Entregar orcamento no SLA prometido (mesmo dia); se atrasar, avisar o cliente proativamente"},
          {"categoria": "Tempo de resposta de inbound", "descricao": "Inbounds noturnos respondidos so na tarde seguinte",
           "impacto": "Lead pode esfriar", "conversas_afetadas": 2,
           "exemplos_clientes": ["Cliente Italo Alves: deu CPF 29/06 21:38, resposta humana so 30/06 14:16 (~17h)"],
           "acao_corretiva": "Priorizar retorno de inbounds com dados (conta/CPF) no inicio do expediente"}
        ],
        "erros_cometidos": [
          {"codigo": "SDR-X3", "descricao": "Orcamento prometido sem prazo cumprido (Andre Martins)", "ocorrencias": 1}
        ]
      }
    },
    {
      "nome": "Lucas", "cor": "#10b981", "papel": "SDR",
      "total_conversas": 2, "ligacoes_dia": 0, "visitas_agendadas": 0,
      "taxa_conversao": 0, "mediana_resposta_min": 0, "media_resposta_min": 0,
      "qualidade": {
        "nota_media": 3.5, "aderencia_script": 35,
        "etapas_cumpridas": {"SDR-1_abertura": 2, "SDR-2_qualificacao": 1, "SDR-3_quebra_objecao": 0, "SDR-4_agendamento": 0},
        "pontos_fortes": [
          {"categoria": "Tentativa de avanco para visita", "descricao": "Tenta marcar visita tecnica",
           "exemplos": ["Cliente Clea: ofereceu marcar visita para avaliar e passar orcamento"]}
        ],
        "pontos_fracos": [
          {"categoria": "Ignora pergunta direta do cliente", "descricao": "Nao responde a duvida do cliente e empurra script generico",
           "impacto": "Quebra de confianca; lead interessado fica sem resposta", "conversas_afetadas": 1,
           "exemplos_clientes": ["Cliente Clea: perguntou 'Qual condicao exclusiva?' (29/06 21:05) e Lucas respondeu so 'bom dia / poderia marcar uma visita?' (30/06 10:42), sem explicar a condicao"],
           "acao_corretiva": "Responder a pergunta do cliente ANTES de avancar o script"}
        ],
        "erros_cometidos": [
          {"codigo": "SDR-X5", "descricao": "Nao respondeu a pergunta direta do cliente", "ocorrencias": 1}
        ]
      }
    }
  ],
  "vendedores": [
    {
      "nome": "Yan Francisco", "cor": "#ef4444", "papel": "VENDEDOR",
      "total_conversas": 24, "ligacoes_dia": 0, "visitas_realizadas": 0, "propostas_enviadas": 0,
      "sem_resposta": 2, "mediana_resposta_min": 30, "media_resposta_min": 90, "total_respostas": 22,
      "qualidade": {
        "nota_media": 4.8, "aderencia_script": 40,
        "argumentos_usados": {"A1":2,"A2":2,"A3":4,"A4":2,"B1":0,"B2":0,"B3":0,"B4":4,"C1":0,"C2":0,"C3":0,"C4":0,"C5":0,
          "D1":0,"D2":1,"D3":1,"D4":1,"D5":0,"D6":0,"E1":0,"E2":0,"E3":0,"E4":0,"E5":0,"F1":0,"F2":0,"F3":0,"F4":0},
        "argumentos_nao_usados": [
          {"id":"D1","nome":"Laboratorio proprio + troca 24h","categoria":"Diferenciacao","importancia":"Critica","vezes_perdidas":24},
          {"id":"F4","nome":"Plantar duvida sobre concorrente","categoria":"Tecnica avancada","importancia":"Alta","vezes_perdidas":24}
        ],
        "pontos_fortes": [
          {"categoria":"Agendamento de visita com diferenciais (B4 + D2/D4)","descricao":"Em alguns leads agendou visita HOJE e usou diferenciais",
           "exemplos":[
             "Cliente Leandro Telez: AGENDOU visita HOJE 16h (cliente enviou localizacao) e usou D2 (17 anos), D3 (6 mil projetos) e D4 (orfaos solares) - raro uso de diferenciais",
             "Cliente Jadson Rosendo: ofereceu visita HOJE 16h apos cliente sinalizar visita 'nessa semana'"]}
        ],
        "pontos_fracos": [
          {"categoria":"Pergunta direta do cliente ignorada por dias","descricao":"Cliente pede valores e recebe so templates/urgencia",
           "impacto":"Perda de lead por falta de resposta objetiva", "conversas_afetadas":1,
           "exemplos_clientes":["Cliente Rafael Borges: pediu 'Os valores' em 23/06; Yan nunca enviou valores, so 'usina de quanto?' + templates de reativacao + urgencia falsa (30/06 14:21)"],
           "acao_corretiva":"Responder o que o cliente pediu (faixa de valores) e so entao qualificar"},
          {"categoria":"Recuperacao pos-visita generica","descricao":"Lead de alto valor visitado some e recebe so 'o que impede de avancar'",
           "impacto":"Recuperacao de lead a vista em risco", "conversas_afetadas":1,
           "exemplos_clientes":["Cliente Maria Vanilma (900kW A VISTA): visitada 26/06 17h, sumiu; Yan so 'Fizemos uma visita mas nao tivemos retorno. O que impede de avancar?' (30/06 10:40), sem reforcar diferenciais nem proposta concreta"],
           "acao_corretiva":"Pos-visita: enviar proposta/recap com D1-D4 e proxima acao clara, nao pergunta aberta"},
          {"categoria":"Disparo em massa generico + urgencia falsa","descricao":"12 reativacoes template identico, zero D1-D4; novo gatilho de escassez artificial",
           "impacto":"Queima de base e baixa conversao", "conversas_afetadas":12,
           "exemplos_clientes":[
             "Cliente Mateus Luiz: 'diretor liberou desconto para os 3 proximos projetos fechados hoje' (X7 - simulacao bancaria sem visita tecnica)",
             "Cliente Jair Araujo (1000kW): lead perdido por distancia recuperado so com escassez artificial"],
           "acao_corretiva":"Segmentar lista; substituir urgencia falsa por D1-D4 e oferta de visita tecnica"}
        ],
        "erros_cometidos": [
          {"codigo":"X4","descricao":"Mensagem generica copy-paste (disparo)","ocorrencias":12},
          {"codigo":"X6","descricao":"Nao mencionou diferenciais D1-D4 na maioria","ocorrencias":21},
          {"codigo":"X7","descricao":"Conduziu a simulacao bancaria sem oferecer visita tecnica","ocorrencias":2}
        ]
      }
    },
    {
      "nome": "Alan Oliveira", "cor": "#f97316", "papel": "VENDEDOR",
      "total_conversas": 0, "ligacoes_dia": 0, "visitas_realizadas": 0, "propostas_enviadas": 0,
      "sem_resposta": 0, "mediana_resposta_min": 0, "media_resposta_min": 0, "total_respostas": 0,
      "qualidade": {
        "nota_media": 0, "aderencia_script": 0,
        "argumentos_usados": {"A1":0,"A2":0,"A3":0,"A4":0,"B1":0,"B2":0,"B3":0,"B4":0,"C1":0,"C2":0,"C3":0,"C4":0,"C5":0,
          "D1":0,"D2":0,"D3":0,"D4":0,"D5":0,"D6":0,"E1":0,"E2":0,"E3":0,"E4":0,"E5":0,"F1":0,"F2":0,"F3":0,"F4":0},
        "argumentos_nao_usados": [],
        "pontos_fortes": [
          {"categoria":"Co-atendimento de visitas","descricao":"Sem conversa solo no chat hoje; aparece como assessor que vai as visitas com Yan",
           "exemplos":["Cliente Mariana: visita marcada 10h com 'Alan e Yan' (remarcada pela cliente)"]}
        ],
        "pontos_fracos": [
          {"categoria":"Sem atuacao no chat","descricao":"Nenhuma conversa solo registrada no periodo","impacto":"Baixa cobertura de chat","conversas_afetadas":0,
           "exemplos_clientes":[], "acao_corretiva":"Registrar tratativas no chat para rastreabilidade"}
        ],
        "erros_cometidos": []
      }
    }
  ],
  "insights": {
    "destaques_positivos": [
      {"pessoa":"Yan Francisco","papel":"VENDEDOR","cliente":"Leandro Telez","acao":"Agendou visita HOJE 16h (cliente enviou localizacao) usando D2/D3/D4 (17 anos, 6 mil projetos, orfaos solares)","resultado":"Visita confirmada para hoje + uso raro de diferenciais"},
      {"pessoa":"Keanny Brandão","papel":"SDR","cliente":"Rafael","acao":"Ofereceu visita tecnica as 16h com script de qualificacao","resultado":"Lead encaminhado para visita"},
      {"pessoa":"Yan Francisco","papel":"VENDEDOR","cliente":"Jadson Rosendo","acao":"Ofereceu visita HOJE 16h apos cliente sinalizar visita na semana","resultado":"Visita em fechamento"}
    ],
    "alertas": [
      {"pessoa":"Keanny Brandão","papel":"SDR","cliente":"André Martins","problema":"Orcamento de usina 300-350kW prometido em 25/06 e nao entregue; cliente cobrou 'Conseguiu fechar o orcamento?' 5 dias depois (30/06 14:17)","impacto":"Lead quente esfriando por gargalo de entrega","acao_corretiva":"Entregar orcamento HOJE; cumprir SLA de mesmo dia"},
      {"pessoa":"Yan Francisco","papel":"VENDEDOR","cliente":"Maria Vanilma","problema":"900kW A VISTA visitada 26/06 sumiu; recebeu so follow-up generico 'o que impede de avancar?'","impacto":"Recuperacao de lead a vista em risco","acao_corretiva":"Enviar proposta/recap com D1-D4 e proxima acao concreta"},
      {"pessoa":"Yan Francisco","papel":"VENDEDOR","cliente":"Rafael Borges","problema":"Pediu 'Os valores' em 23/06 e nunca recebeu; so templates + urgencia falsa","impacto":"Lead perdido por falta de resposta objetiva","acao_corretiva":"Enviar faixa de valores solicitada"},
      {"pessoa":"Lucas","papel":"SDR","cliente":"Clea","problema":"Cliente perguntou 'Qual condicao exclusiva?' e foi ignorada (empurrou visita generica)","impacto":"Quebra de confianca com lead interessado","acao_corretiva":"Responder a duvida antes de avancar o script"}
    ],
    "oportunidades": [
      {"tipo":"Processo","cliente":"Multiplos","descricao":"Yan adotou template de URGENCIA FALSA ('diretor liberou desconto para 3 projetos hoje') em vez de qualificar/usar diferenciais","acao_sugerida":"Substituir escassez artificial por D1-D4 + oferta de visita tecnica"},
      {"tipo":"Diferenciacao","cliente":"Geral","descricao":"D1-D4 quase ausentes (excecao: Leandro Telez com D2/D3/D4); maioria dos leads sem diferenciacao","acao_sugerida":"Padronizar D1 (laboratorio/troca 24h) e D4 (orfaos solares) no script de vendedor"}
    ]
  },
  "ranking_sdrs": [
    {"posicao":1,"nome":"Keanny Brandão","nota_media":6.0,"aderencia":60,"visitas_agendadas":1,"badge":"\U0001F3C6 Ouro"},
    {"posicao":2,"nome":"Lucas","nota_media":3.5,"aderencia":35,"visitas_agendadas":0,"badge":"\U0001F948 Prata"}
  ],
  "ranking_vendedores": [
    {"posicao":1,"nome":"Yan Francisco","nota_media":4.8,"aderencia":40,"badge":"\U0001F3C6 Ouro"},
    {"posicao":2,"nome":"Alan Oliveira","nota_media":0,"aderencia":0,"badge":"\U0001F4CA Sem atuacao solo"}
  ],
  "oportunidades_prioritarias": [
    {"cliente":"André Martins","pessoa":"Keanny Brandão","papel":"SDR","conta":"DR4","categoria":"⚠️ FOLLOW-UP URGENTE","motivo":"Usina 300-350kW/mes (Cupira-PE); orcamento prometido em 25/06 e nao entregue, cliente cobrando hoje 14:17","recomendacao":"Entregar o orcamento HOJE e agendar visita/ligacao","urgencia":"HOJE","argumentos_recomendados":["A3 - qualificacao","B4 - vender a visita","D3 - 6 mil projetos"]},
    {"cliente":"Leandro Telez","pessoa":"Yan Francisco","papel":"VENDEDOR","conta":"DR4","categoria":"\U0001F525 QUENTE","motivo":"Visita confirmada HOJE 16h, localizacao enviada; Yan ja usou D2/D3/D4","recomendacao":"Executar visita e fechar com proposta no local","urgencia":"HOJE","argumentos_recomendados":["B4 - vender a visita","D1 - laboratorio","D4 - orfaos solares"]},
    {"cliente":"Maria Vanilma","pessoa":"Yan Francisco","papel":"VENDEDOR","conta":"DR4","categoria":"\U0001F6A8 RECUPERAÇÃO","motivo":"900kW A VISTA visitada 26/06 e sumiu; so follow-up generico","recomendacao":"Enviar proposta/recap com diferenciais e proxima acao concreta","urgencia":"HOJE","argumentos_recomendados":["D1 - laboratorio","D2 - 17 anos","C1 - troca conta por parcela"]},
    {"cliente":"Mariana","pessoa":"Yan Francisco / Alan Oliveira","papel":"VENDEDOR","conta":"DR4","categoria":"\U0001F525 QUENTE","motivo":"R$1.000/mes (Cond. Buona Vita); visita HOJE 10h remarcada pela cliente (bebe)","recomendacao":"Confirmar novo horario ativamente HOJE, nao deixar em aberto","urgencia":"HOJE","argumentos_recomendados":["B4 - vender a visita","A2 - personalizacao"]},
    {"cliente":"Jadson Rosendo","pessoa":"Yan Francisco","papel":"VENDEDOR","conta":"DR4","categoria":"\U0001F525 QUENTE","motivo":"Quer visita 'nessa semana'; Yan ofereceu HOJE 16h","recomendacao":"Confirmar a visita e preparar orcamento","urgencia":"HOJE","argumentos_recomendados":["B4 - vender a visita","D2 - 17 anos"]},
    {"cliente":"Márcio Bittencourt","pessoa":"Yan Francisco","papel":"VENDEDOR","conta":"DR4","categoria":"\U0001F48E ALTO CONSUMO","motivo":"Usina ~10kWp (~R$15mil), negociando visita para fechar valor","recomendacao":"Agendar visita tecnica e ancorar diferenciais","urgencia":"HOJE","argumentos_recomendados":["B4 - vender a visita","D1 - laboratorio","D3 - 6 mil projetos"]},
    {"cliente":"Rafael Borges","pessoa":"Yan Francisco","papel":"VENDEDOR","conta":"DR4","categoria":"\U0001F6A8 RECUPERAÇÃO","motivo":"Pediu 'Os valores' em 23/06 e nunca recebeu; so templates","recomendacao":"Enviar a faixa de valores solicitada e retomar","urgencia":"HOJE","argumentos_recomendados":["A3 - qualificacao","C1 - parcela"]},
    {"cliente":"Italo Alves","pessoa":"Keanny Brandão","papel":"SDR","conta":"DR4","categoria":"\U0001F525 QUENTE","motivo":"Inbound R$350/mes + CPF para analise de financiamento","recomendacao":"Rodar a analise e retornar com proposta","urgencia":"HOJE","argumentos_recomendados":["SDR-2 - qualificacao","C1 - parcela"]},
    {"cliente":"Mateus Luiz","pessoa":"Yan Francisco","papel":"VENDEDOR","conta":"DR4","categoria":"\U0001F48E ALTO CONSUMO","motivo":"Engajado em simulacao bancaria, mas conduzido SEM visita tecnica (X7)","recomendacao":"Inserir visita tecnica antes de fechar a simulacao","urgencia":"ESTA SEMANA","argumentos_recomendados":["B4 - vender a visita","D1 - laboratorio"]},
    {"cliente":"Rafael","pessoa":"Keanny Brandão","papel":"SDR","conta":"DR4","categoria":"\U0001F525 QUENTE","motivo":"Petrolina; aceitou trilha de visita tecnica 16h","recomendacao":"Confirmar visita e encaminhar ao vendedor","urgencia":"HOJE","argumentos_recomendados":["SDR-4 - agendamento","B4 - vender a visita"]}
  ],
  "conversas": []
}

conversas = [
 {"id":1,"conta":"DR4","cliente":"André Martins","pessoa":"Keanny Brandão","papel":"SDR","hora_lista":"14:17","ultima_msg":"14:17","total_msgs":18,"status":"sem_resposta","nota":4,"argumentos_usados":["SDR-1","SDR-2"],"argumentos_perdidos":["SDR-4"],"erros":["SDR-X3"],"observacao":"Cliente Andre Martins (Cupira-PE, usina 300-350kW/mes): orcamento prometido 25/06 e nao entregue; cliente cobrou 'Conseguiu fechar o orcamento?' 30/06 14:17 (GARGALO de entrega)"},
 {"id":2,"conta":"DR4","cliente":"Leandro Telez","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"14:26","ultima_msg":"14:26","total_msgs":20,"status":"ok","nota":7,"argumentos_usados":["B4","D2","D3","D4"],"argumentos_perdidos":["D1"],"erros":[],"observacao":"Cliente Leandro Telez: Yan AGENDOU visita HOJE 16h (localizacao enviada) usando D2/D3/D4 (17 anos, 6 mil projetos, orfaos solares) - destaque do dia"},
 {"id":3,"conta":"DR4","cliente":"Mariana","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"09:48","ultima_msg":"09:48","total_msgs":20,"status":"ok","nota":5,"argumentos_usados":["A2"],"argumentos_perdidos":["B4"],"erros":[],"observacao":"Cliente Mariana (R$1.000/mes, Cond. Buona Vita): visita HOJE 10h com Alan e Yan REMARCADA pela cliente ('caos com a bebe'); Yan deixou em aberto 'ver qual horario'"},
 {"id":4,"conta":"DR4","cliente":"Maria Vanilma","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"10:40","ultima_msg":"10:40","total_msgs":20,"status":"ok","nota":3,"argumentos_usados":["D2"],"argumentos_perdidos":["D1","D4"],"erros":["X6"],"observacao":"Cliente Maria Vanilma (900kW A VISTA): visitada 26/06 17h pelo assessor Diego, sumiu; Yan so follow-up generico 'o que impede de avancar?' (recuperacao em risco)"},
 {"id":5,"conta":"DR4","cliente":"Jadson Rosendo","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"10:36","ultima_msg":"10:36","total_msgs":20,"status":"ok","nota":6,"argumentos_usados":["B4"],"argumentos_perdidos":["D1","D2"],"erros":["X6"],"observacao":"Cliente Jadson Rosendo: sinalizou visita 'nessa semana' (29/06), Yan ofereceu HOJE 16h (assessor Alan em tratativas)"},
 {"id":6,"conta":"DR4","cliente":"Mateus Luiz","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"11:51","ultima_msg":"11:51","total_msgs":20,"status":"ok","nota":4,"argumentos_usados":["A3"],"argumentos_perdidos":["B4","D1"],"erros":["X7"],"observacao":"Cliente Mateus Luiz: engajou em simulacao parceria Banco do Nordeste; Yan conduz SEM visita tecnica (X7) e usa urgencia falsa 'diretor liberou desconto p/ 3 projetos hoje'"},
 {"id":7,"conta":"DR4","cliente":"Márcio Bittencourt","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"12:07","ultima_msg":"12:07","total_msgs":20,"status":"ok","nota":5,"argumentos_usados":["A3","B4"],"argumentos_perdidos":["D1","D2"],"erros":["X6"],"observacao":"Cliente Marcio Bittencourt: usina ~10kWp (~R$15mil), Yan tentando marcar visita p/ negociar valor; cliente passivo ('Ok')"},
 {"id":8,"conta":"DR4","cliente":"Rafael Borges","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"14:21","ultima_msg":"14:21","total_msgs":20,"status":"ok","nota":2,"argumentos_usados":[],"argumentos_perdidos":["A3","C1"],"erros":["X4","X6"],"observacao":"Cliente Rafael Borges: pediu 'Os valores' 23/06 e NUNCA recebeu; Yan so 'usina de quanto?' + templates + urgencia falsa 30/06"},
 {"id":9,"conta":"DR4","cliente":"Jair Araujo","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"14:14","ultima_msg":"14:14","total_msgs":20,"status":"ok","nota":3,"argumentos_usados":[],"argumentos_perdidos":["D1","D2"],"erros":["X4","X6"],"observacao":"Cliente Jair Araujo (1000kW): nao quis seguir por distancia (25/06); Yan tenta recuperar so com escassez artificial 'desconto p/ 3 projetos'"},
 {"id":10,"conta":"DR4","cliente":"Robério Allan","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"11:29","ultima_msg":"11:29","total_msgs":20,"status":"ok","nota":5,"argumentos_usados":["B4"],"argumentos_perdidos":["D1"],"erros":["X6"],"observacao":"Cliente Roberio Allan: telhado de ceramica, quer ver valores; so disponivel sabado (trabalha ate 18h); Yan ofereceu sabado"},
 {"id":11,"conta":"DR4","cliente":"Camila P","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"11:42","ultima_msg":"11:42","total_msgs":20,"status":"ok","nota":4,"argumentos_usados":["A3"],"argumentos_perdidos":["D1"],"erros":["X6"],"observacao":"Cliente Camila P: telhado ceramica, quer saber valor do projeto antes da forma de pagamento; Yan respondendo por audio"},
 {"id":12,"conta":"DR4","cliente":"Prof. Vieira","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"14:05","ultima_msg":"14:05","total_msgs":20,"status":"ok","nota":5,"argumentos_usados":["A3","B4"],"argumentos_perdidos":["D1"],"erros":["X6"],"observacao":"Cliente Prof. Vieira: R$250/mes (residencia), Yan ofereceu visita p/ negociar valor"},
 {"id":13,"conta":"DR4","cliente":"Pablo Jaasiel","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"11:13","ultima_msg":"11:13","total_msgs":17,"status":"ok","nota":4,"argumentos_usados":[],"argumentos_perdidos":["D1","D2"],"erros":["X4"],"observacao":"Cliente Pablo Jaasiel: reativacao com urgencia falsa; cliente respondeu por audio, troca de audios em andamento"},
 {"id":14,"conta":"DR4","cliente":"Rafael","pessoa":"Keanny Brandão","papel":"SDR","hora_lista":"14:10","ultima_msg":"14:10","total_msgs":13,"status":"ok","nota":7,"argumentos_usados":["SDR-1","SDR-2","SDR-4"],"argumentos_perdidos":[],"erros":[],"observacao":"Cliente Rafael (Petrolina): Keanny ofereceu ligacao OU visita tecnica as 16h com bom script"},
 {"id":15,"conta":"DR4","cliente":"Italo Alves","pessoa":"Keanny Brandão","papel":"SDR","hora_lista":"14:18","ultima_msg":"14:18","total_msgs":9,"status":"ok","nota":6,"argumentos_usados":["SDR-1","SDR-2"],"argumentos_perdidos":["SDR-4"],"erros":[],"observacao":"Cliente Italo Alves: inbound R$350/mes + CPF p/ analise de financiamento (29/06 21:38); Keanny retornou 30/06 14:16 'vejo agora mesmo' (~17h)"},
 {"id":16,"conta":"DR4","cliente":"Sheila","pessoa":"Keanny Brandão","papel":"SDR","hora_lista":"14:20","ultima_msg":"14:20","total_msgs":8,"status":"ok","nota":6,"argumentos_usados":["SDR-1","SDR-2"],"argumentos_perdidos":["SDR-4"],"erros":[],"observacao":"Cliente Sheila: inbound 13:09 'quero economizar com energia solar'; Keanny respondeu 14:19 perguntando regiao"},
 {"id":17,"conta":"DR4","cliente":"Adalberto","pessoa":"Keanny Brandão","papel":"SDR","hora_lista":"14:15","ultima_msg":"14:15","total_msgs":15,"status":"ok","nota":6,"argumentos_usados":["SDR-1","SDR-2"],"argumentos_perdidos":["SDR-4"],"erros":[],"observacao":"Cliente Adalberto (Petrolina): pediu p/ falar no dia seguinte (29/06 20:52), Keanny fez follow-up 30/06 14:15"},
 {"id":18,"conta":"DR4","cliente":"Maria Souza Araujo","pessoa":"Keanny Brandão","papel":"SDR","hora_lista":"14:23","ultima_msg":"14:23","total_msgs":6,"status":"ok","nota":6,"argumentos_usados":["SDR-1","SDR-2"],"argumentos_perdidos":["SDR-4"],"erros":[],"observacao":"Cliente Maria Souza Araujo: inbound fresco 14:05 'posso ter mais informacoes?'; Keane abriu e respondeu por audio 14:23"},
 {"id":19,"conta":"DR4","cliente":"Clea","pessoa":"Lucas","papel":"SDR","hora_lista":"10:44","ultima_msg":"10:44","total_msgs":20,"status":"ok","nota":3,"argumentos_usados":["SDR-1"],"argumentos_perdidos":["SDR-2","SDR-4"],"erros":["SDR-X5"],"observacao":"Cliente Clea: interessada ('aguardando passar alta temporada'), perguntou 'Qual condicao exclusiva?'; Lucas ignorou e empurrou visita generica"},
 {"id":20,"conta":"DR4","cliente":"Lucas (cliente)","pessoa":"Lucas/Gabriel","papel":"SDR","hora_lista":"09:06","ultima_msg":"09:06","total_msgs":7,"status":"ok","nota":4,"argumentos_usados":["SDR-1","SDR-2"],"argumentos_perdidos":["SDR-4"],"erros":[],"observacao":"Cliente Lucas: inbound noturno, opener bot Gabriel; qualificacao de cidade em andamento"},
 {"id":21,"conta":"DR4","cliente":"Patrícia Lima","pessoa":"Keanny Brandão","papel":"SDR","hora_lista":"09:03","ultima_msg":"09:03","total_msgs":5,"status":"ok","nota":0,"argumentos_usados":[],"argumentos_perdidos":[],"erros":[],"observacao":"NAO-LEAD: cliente informou que 'a neta enviou mensagem errada'"},
 {"id":22,"conta":"DR4","cliente":"Mainaldo","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"11:28","ultima_msg":"11:28","total_msgs":20,"status":"ok","nota":0,"argumentos_usados":[],"argumentos_perdidos":[],"erros":[],"observacao":"NAO-LEAD: contato por engano (cliente informou na ligacao)"},
 {"id":23,"conta":"DR4","cliente":"[Disparo em massa - Yan Francisco]","pessoa":"Yan Francisco","papel":"VENDEDOR","hora_lista":"--","ultima_msg":"--","total_msgs":0,"status":"ok","nota":4,"argumentos_usados":[],"argumentos_perdidos":["D1","D2","D3","D4"],"erros":["X4","X6","X7"],"observacao":"Agregado: ~12 reativacoes template identico (banco/urgencia), NOS ultima msg aguardando cliente (classificacao por preview): keilacassia66, ZE NILTON LIMA, 3151 LEO, Claudemy, fabioluiz..., cicero, blessed, Perpetua Castro, valdemir..., Nilton L C, Emanuel, JaironKelver"}
]
report["conversas"] = conversas

out_dir = r"C:\BotConversa\dados"
out_path = os.path.join(out_dir, DATA + ".json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

# Update index.json (current schema)
index_path = os.path.join(out_dir, "index.json")
with open(index_path, "r", encoding="utf-8") as f:
    index = json.load(f)

entry = {
    "data": DATA,
    "hora_execucao": HORA,
    "tipo_analise": TIPO,
    "total_conversas": report["metricas"]["total_conversas"],
    "total_conversas_dr4": report["metricas"]["total_conversas_dr4"],
    "total_conversas_dr2": report["metricas"]["total_conversas_dr2"],
    "sem_resposta": report["metricas"]["sem_resposta"],
    "criticas": report["metricas"]["criticas"],
    "nota_media_sdr": report["metricas"]["nota_media_sdr"],
    "nota_media_vendedor": report["metricas"]["nota_media_vendedor"],
    "cobertura": report["observacao_geral"],
    "alerta_critico": (
        "DR4 dominado pelo Yan Francisco (24 conv: 12 disparos puros + 12 leads ativos) com NOVO template de "
        "URGENCIA FALSA ('diretor liberou desconto p/ 3 projetos hoje'). DESTAQUE: Yan AGENDOU visita HOJE 16h do "
        "Leandro Telez usando D2/D3/D4 (raro uso de diferenciais) + ofereceu visita 16h ao Jadson. GARGALO CRITICO: "
        "Keanny prometeu orcamento 300-350kW ao Andre Martins em 25/06, 5 dias sem entregar e cliente cobrando hoje. "
        "RECUPERACAO EM RISCO: Maria Vanilma (900kW a vista) visitada 26/06 e sumiu, so follow-up generico; Rafael "
        "Borges pediu valores em 23/06 e nunca recebeu. Mariana (R$1.000/mes) remarcou visita de hoje. SDR Lucas "
        "ignorou pergunta direta da Clea. Nota SDR 4.8 (Keanny 6.0/Lucas 3.5) / Vendedor 4.8 (Yan 4.8; Alan sem chat solo)."
    ),
    "sdrs": ["Keanny Brandão", "Lucas"],
    "vendedores": ["Yan Francisco", "Alan Oliveira"]
}
rel = [r for r in index.get("relatorios", []) if r.get("data") != DATA]
rel.append(entry)
rel.sort(key=lambda r: r.get("data", ""))
index["relatorios"] = rel
index["ultima_atualizacao"] = DATA + "T" + HORA

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

# Validate
with open(out_path, "r", encoding="utf-8") as f:
    json.load(f)
with open(index_path, "r", encoding="utf-8") as f:
    json.load(f)

print("OK", out_path)
print("conversas:", len(report["conversas"]))
print("index relatorios:", len(index["relatorios"]))
