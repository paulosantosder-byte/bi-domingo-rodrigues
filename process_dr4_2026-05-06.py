"""
Processador da analise profunda do DR4 para 2026-05-06.
Le raw_dr4_2026-05-06_full.json (mensagens completas) e produz
2026-05-06.json no formato exigido.
"""
import json
import re
from datetime import datetime, time as dtime
from collections import defaultdict, Counter

DATA = "2026-05-06"
HORA_EXEC = datetime.now().strftime("%H:%M")

VENDEDORES = {
    "Luana": {"cor": "#7c3aed", "match": ["luana"]},
    "Maria Luiza": {"cor": "#ec4899", "match": ["maria luiza"]},
    "Keane": {"cor": "#f59e0b", "match": ["keane"]},
    "Claudio Rodrigues": {"cor": "#dc2626", "match": ["claudio"]},
    "Caio Roberto": {"cor": "#0ea5e9", "match": ["caio"]},
    "Guilherme": {"cor": "#10b981", "match": ["guilherme"]},
    "Kemily": {"cor": "#a855f7", "match": ["kemily"]},
}

def _load_ligacoes():
    base = {"Luana": 0, "Maria Luiza": 0, "Guilherme": 0, "Kemily": 0,
            "Keane": 0, "Claudio Rodrigues": 0, "Caio Roberto": 0}
    try:
        with open(r"C:/Botconversa/ligacoes_dia.txt", encoding="utf-8") as f:
            for line in f:
                if ":" not in line:
                    continue
                nome, val = line.split(":", 1)
                nome = nome.strip()
                try:
                    n = int(val.strip())
                except ValueError:
                    continue
                # normalizar Kemilly -> Kemily
                if nome.lower() == "kemilly":
                    nome = "Kemily"
                if nome in base:
                    base[nome] = n
    except FileNotFoundError:
        pass
    return base

LIGACOES = _load_ligacoes()

ARGUMENTOS = {
    "A1": {"nome": "Velocidade de resposta", "categoria": "Primeiro Contato", "importancia": "Alta"},
    "A2": {"nome": "Personalizacao com nome/saudacao", "categoria": "Primeiro Contato", "importancia": "Alta"},
    "A3": {"nome": "Pergunta de qualificacao", "categoria": "Primeiro Contato", "importancia": "Critica"},
    "A4": {"nome": "Nao enviar preco sem qualificacao", "categoria": "Primeiro Contato", "importancia": "Critica"},
    "B1": {"nome": "Gatilho de proximidade", "categoria": "Agendamento", "importancia": "Alta"},
    "B2": {"nome": "Quebra objecao 'manda Zap'", "categoria": "Agendamento", "importancia": "Critica"},
    "B3": {"nome": "Argumento de seguranca", "categoria": "Agendamento", "importancia": "Media"},
    "B4": {"nome": "Vender visita nao preco", "categoria": "Agendamento", "importancia": "Critica"},
    "C1": {"nome": "Financiamento sem entrada", "categoria": "Quebra Objecoes", "importancia": "Alta"},
    "C2": {"nome": "Prova social especifica", "categoria": "Quebra Objecoes", "importancia": "Alta"},
    "C3": {"nome": "Aversao a perda", "categoria": "Quebra Objecoes", "importancia": "Media"},
    "C4": {"nome": "Material educativo", "categoria": "Quebra Objecoes", "importancia": "Media"},
    "C5": {"nome": "Pergunta direta", "categoria": "Quebra Objecoes", "importancia": "Media"},
    "D1": {"nome": "Laboratorio proprio + troca 24h", "categoria": "Diferenciacao", "importancia": "Critica"},
    "D2": {"nome": "17 anos de mercado", "categoria": "Diferenciacao", "importancia": "Critica"},
    "D3": {"nome": "6 mil projetos", "categoria": "Diferenciacao", "importancia": "Critica"},
    "D4": {"nome": "Orfaos solares", "categoria": "Diferenciacao", "importancia": "Alta"},
    "D5": {"nome": "Checklist comparacao", "categoria": "Diferenciacao", "importancia": "Media"},
    "D6": {"nome": "Nao esta comprando placas", "categoria": "Diferenciacao", "importancia": "Media"},
    "E1": {"nome": "Follow-up Semana 1", "categoria": "Follow-up", "importancia": "Alta"},
    "E2": {"nome": "Follow-up Semana 2", "categoria": "Follow-up", "importancia": "Alta"},
    "E3": {"nome": "Follow-up Semana 3", "categoria": "Follow-up", "importancia": "Media"},
    "E4": {"nome": "Follow-up Semana 4 break-up", "categoria": "Follow-up", "importancia": "Media"},
    "E5": {"nome": "Audios curtos", "categoria": "Follow-up", "importancia": "Media"},
    "F1": {"nome": "Mensagem apagada (escassez)", "categoria": "Avancado", "importancia": "Baixa"},
    "F2": {"nome": "Gravacao de reuniao", "categoria": "Avancado", "importancia": "Baixa"},
    "F3": {"nome": "Programa de indicacoes", "categoria": "Avancado", "importancia": "Media"},
    "F4": {"nome": "Plantar duvida concorrente", "categoria": "Avancado", "importancia": "Media"},
}

ERROS_DESC = {
    "X1": "Enviou preco sem qualificacao",
    "X2": "Insistente sem agregar valor",
    "X3": "Ignorou perguntas/objecoes",
    "X4": "Mensagem genérica copy-paste",
    "X5": "Abandonou lead antes 7 dias",
    "X6": "Nunca mencionou diferenciais (D1-D4)",
    "X7": "Nao tentou agendar visita (B1-B4)",
    "X8": "Tempo resposta > 60min",
}

def normalize_vendedor(atribuido):
    if not atribuido:
        return None
    a = atribuido.lower()
    for nome, info in VENDEDORES.items():
        for m in info["match"]:
            if m in a:
                return nome
    return None


def msg_text_clean(text, vendor_name=None):
    """Remove vendor name prefix like 'Keane:' from message text."""
    if not text:
        return ""
    t = text.strip()
    # Remove leading vendor prefix
    t = re.sub(r"^(Keane|Caio|Luana|Claudio|Maria Luiza|Guilherme|Kemily|Kemilly)[^:\n]*:\s*\n?", "", t, flags=re.IGNORECASE)
    return t.strip()


def extract_time_hhmm(date_str):
    """From 'Qua, 06 Mai 2026, 12:51' extract '12:51'."""
    if not date_str:
        return None
    m = re.search(r"(\d{2}:\d{2})", date_str)
    return m.group(1) if m else None


def detectar_argumentos(vendor_text):
    """Detectar argumentos usados pelo vendedor com base no texto agregado."""
    t = vendor_text.lower()
    usados = set()
    # A2 - saudacao / personalizacao
    if re.search(r"(\bolá\b|\bola\b|\bbom dia\b|\bboa tarde\b|\bboa noite\b|\bsr\.|\bsra\.|\bsenhor\b|\bsenhora\b|\bme chamo\b)", t):
        usados.add("A2")
    # A3 - qualificacao
    if re.search(r"(valor.{0,20}conta|conta.{0,15}luz|consumo|qual.*conta|quanto.{0,20}conta|fatura|kwh|região|regiao|onde.{0,20}mora|qual.{0,20}bairro|cidade|qual.{0,5}cep|monofas|trifas|orçament|orcament)", t):
        usados.add("A3")
    # B1 - proximidade
    if re.search(r"(passar.{0,5}aí|passar.{0,5}ai|aí perto|seu bairro|sua região|sua regiao|próxim|proxim|estamos.{0,15}atend|cliente.{0,10}perto)", t):
        usados.add("B1")
    # B2 - quebra zap
    if re.search(r"(comprar.{0,15}carro|investir.{0,15}sem ver|ver antes|política.{0,15}empresa|so.{0,10}entreg.{0,10}projeto|visita.{0,5}técnica|visita.{0,5}tecnica|projeto.{0,15}após visita|antes de fechar)", t):
        usados.add("B2")
    # B3 - seguranca
    if re.search(r"(golpe|segurança|seguranca|empresa séria|empresa seria|legalizada|registrada)", t):
        usados.add("B3")
    # B4 - vender visita
    if re.search(r"(\bvisita\b|agendar|agendamento|\bvisitar\b|engenheiro|técnico|tecnico|avaliar|presencial|nos encontr|posso ir|posso passar)", t):
        usados.add("B4")
    # C1 - financ
    if re.search(r"(sem entrada|financia|parcela.{0,15}conta|trocar.{0,10}conta.{0,15}parcela|sem tirar.{0,15}bolso|parcelado|entrada zero)", t):
        usados.add("C1")
    # C2 - prova social
    if re.search(r"(instalamos|cliente.{0,15}economiza|conta caiu|taxa mínima|taxa minima|projeto recente|sr\..{0,30}economiz|sra\..{0,30}economiz)", t):
        usados.add("C2")
    # C3 - aversao
    if re.search(r"(já pagou|ja pagou|dinheiro.{0,5}não volta|dinheiro.{0,5}nao volta|perdendo|jogou.{0,5}fora|dinheiro perdido)", t):
        usados.add("C3")
    # C4 - material
    if re.search(r"(\bguia\b|5 mitos|mitos|simulação|simulacao|estudo|catálogo|catalogo)", t):
        usados.add("C4")
    # C5 - pergunta direta
    if re.search(r"(ainda.{0,15}prioridade|prefere que.{0,15}retome|ser inconveniente|fim do ano)", t):
        usados.add("C5")
    # D1 - laboratorio
    if re.search(r"(laboratório|laboratorio|troca.{0,5}24|24 ?h|inversor.{0,15}troca)", t):
        usados.add("D1")
    # D2 - 17 anos
    if re.search(r"(17 anos|dezessete anos|mercado há.{0,5}17|mercado ha.{0,5}17|17 ?\(dezessete\))", t):
        usados.add("D2")
    # D3 - 6 mil projetos
    if re.search(r"(6 ?mil.{0,15}projet|seis mil.{0,15}projet|6\.000.{0,15}projeto|6000.{0,15}projet|mais de.{0,5}\d.{0,5}mil.{0,15}projet)", t):
        usados.add("D3")
    # D4 - orfaos
    if re.search(r"(órfão|orfao|empresa.{0,15}fechando|setor específico|setor especifico|órfãos solares)", t):
        usados.add("D4")
    # D5 - checklist
    if re.search(r"(cnpj|capital social|comparação|comparacao|checklist)", t):
        usados.add("D5")
    # D6
    if re.search(r"(não.{0,5}comprando placas|nao.{0,5}comprando placas|comprando geração|geracao de energia|suporte.{0,5}garantia)", t):
        usados.add("D6")
    return usados


def msgs_to_text(msgs, sender):
    """Concatenate all texts of messages from given sender."""
    parts = []
    for m in msgs:
        if m.get("sender") == sender:
            parts.append(msg_text_clean(m.get("text", "")))
    return " \n".join(parts)


def calc_response_time_min(client_hhmm, vendor_hhmm):
    """Tempo dentro do horario comercial 08:00-18:00 (mesmo dia)."""
    if not client_hhmm or not vendor_hhmm:
        return None
    try:
        ch, cm = map(int, client_hhmm.split(":"))
        vh, vm = map(int, vendor_hhmm.split(":"))
    except Exception:
        return None
    cmin = ch * 60 + cm
    vmin = vh * 60 + vm
    if vmin < cmin:
        return None
    # Aplicar janela 08:00 (480) - 18:00 (1080)
    cmin_eff = max(cmin, 480) if cmin < 1080 else 480  # Se cliente fora horario noite, ate manha proxima (mas mesmo dia aqui)
    vmin_eff = min(vmin, 1080) if vmin > 480 else 480
    if vmin_eff <= cmin_eff:
        return 0
    return vmin_eff - cmin_eff


def main():
    with open(r"C:/Botconversa/dados/raw_dr4_2026-05-06_full.json", encoding="utf-8") as f:
        raw = json.load(f)

    completed = raw["completed"]
    conversas_proc = []
    por_vendedor = defaultdict(list)

    for i, c in enumerate(completed, 1):
        nome_cli = c["name"]
        if "Ignorar" in nome_cli or "ignorar" in nome_cli.lower():
            continue
        atrib = c.get("atribuido", "")
        vendedor = normalize_vendedor(atrib)
        msgs = c.get("msgs", [])
        # Filtra mensagens de hoje
        msgs_today = [m for m in msgs if m.get("date") and "06 Mai 2026" in m["date"]]

        # Vendedor / cliente split
        msgs_v = [m for m in msgs_today if m.get("sender") == "vendor"]
        msgs_c = [m for m in msgs_today if m.get("sender") == "client"]

        # Times
        last_client_t = extract_time_hhmm(msgs_c[-1]["date"]) if msgs_c else None
        first_vendor_response_t = None
        # Find first vendor msg AFTER last client msg
        if msgs_c:
            last_c_idx = max(j for j, m in enumerate(msgs_today) if m.get("sender") == "client")
            for j in range(last_c_idx + 1, len(msgs_today)):
                if msgs_today[j].get("sender") == "vendor":
                    first_vendor_response_t = extract_time_hhmm(msgs_today[j]["date"])
                    break

        last_v_t = extract_time_hhmm(msgs_v[-1]["date"]) if msgs_v else None
        ult_msg_time = (msgs_today[-1]["date"] if msgs_today else None)
        ult_msg_hhmm = extract_time_hhmm(ult_msg_time) if ult_msg_time else c["time"]
        ult_author = msgs_today[-1].get("sender") if msgs_today else None

        # Status
        respondeu = len(msgs_v) > 0
        if not respondeu and len(msgs_c) > 0:
            status = "critico"  # Cliente falou hoje, vendedor nao respondeu
        elif msgs_c and ult_author == "client":
            status = "sem_resposta"
        else:
            status = "ok"

        # Tempo de resposta
        tempo = calc_response_time_min(last_client_t, first_vendor_response_t) if first_vendor_response_t else None

        # Texto agregado
        txt_v = msgs_to_text(msgs_today, "vendor")
        txt_c = msgs_to_text(msgs_today, "client")

        # Argumentos
        usados = detectar_argumentos(txt_v)
        # A1 - velocidade (se tempo <=15min)
        if tempo is not None and tempo <= 15:
            usados.add("A1")
        # A4 - se vendor mandou preco SEM A3 antes (heuristica simples)
        # Evidencia preço: "R$" ou número valor + "mil"
        if re.search(r"R\$\s*\d|reais|valor.*\d{3,}|\d{3,}.*reais", txt_v.lower()) and "A3" not in usados:
            # Pode indicar X1 (ja avaliado abaixo)
            pass
        else:
            if re.search(r"R\$|reais", txt_v.lower()):
                # Verificar se A3 veio antes (heuristica - se tem A3 considera A4 ok)
                pass
        # E5 - audios usados (sender vendor com preview audio - heuristica simples)
        # Como nao temos preview de audio aqui, skip
        # F3 - indicacoes
        if re.search(r"indica|indicar|bonus.{0,10}indica|R\$ ?200", txt_v.lower()):
            usados.add("F3")

        # Erros
        erros = []
        if status == "critico" and msgs_c:
            erros.append("X3")
        if not any(d in usados for d in ["D1", "D2", "D3", "D4"]) and respondeu:
            erros.append("X6")
        if not any(b in usados for b in ["B1", "B2", "B3", "B4"]) and respondeu:
            erros.append("X7")
        if tempo is not None and tempo > 60:
            erros.append("X8")
        # X1 - precificou sem qualificar (heuristica: tem preco mas sem A3)
        if re.search(r"R\$|reais|valor.{0,10}\d{3,}", txt_v.lower()) and "A3" not in usados:
            erros.append("X1")

        # Nota
        nota = 5.0
        if respondeu:
            if any(a in usados for a in ["A1", "A2", "A3", "A4"]):
                nota += 1
            if any(b in usados for b in ["B1", "B2", "B3", "B4"]):
                nota += 1
            if any(co in usados for co in ["C1", "C2", "C3", "C4", "C5"]):
                nota += 0.5
            ds = sum(1 for d in ["D1", "D2", "D3", "D4"] if d in usados)
            nota += ds * 0.5
            if "A3" in usados:
                nota += 0.5
            if "B4" in usados:
                nota += 0.5
            for e in erros:
                if e == "X6": nota -= 1
                elif e == "X7": nota -= 0.5
                elif e == "X8": nota -= 0.5
                elif e == "X1": nota -= 1
                elif e == "X3": nota -= 0.5
        else:
            nota = 1 if msgs_c else 0  # Sem msgs hoje e sem vendor msg = 0
        nota = max(0, min(10, nota))
        nota = round(nota, 1)

        # Argumentos perdidos (criticos nao usados)
        perdidos = [k for k in ["D1", "D2", "D3", "D4", "B1", "B2", "B4", "A3", "C1"] if k not in usados]

        obs_parts = [f"{len(msgs_today)} msgs hoje"]
        if status == "critico":
            obs_parts.append("CRITICO: sem resposta vendedor!")
        elif tempo is not None:
            obs_parts.append(f"Resp {tempo}min")
        if not any(d in usados for d in ["D1","D2","D3","D4"]) and respondeu:
            obs_parts.append("Sem D1-D4")
        if respondeu and "A3" in usados:
            obs_parts.append("Qualificou (A3)")

        conv_data = {
            "id": i,
            "cliente": nome_cli,
            "vendedor": vendedor or "Sem atribuicao",
            "vendedor_botconversa": atrib,
            "hora_lista": c.get("time"),
            "ultima_msg": ult_msg_hhmm or c.get("time"),
            "total_msgs": len(msgs_today),
            "status": status,
            "nota": nota,
            "argumentos_usados": sorted(usados),
            "argumentos_perdidos": perdidos[:5],
            "erros": erros,
            "tempo_resposta_min": tempo,
            "observacao": " | ".join(obs_parts),
        }
        conversas_proc.append(conv_data)
        if vendedor:
            por_vendedor[vendedor].append(conv_data)

    # Aggregate per vendor
    vendedores_out = []
    for nome, info in VENDEDORES.items():
        convs = por_vendedor.get(nome, [])
        if not convs:
            continue
        tempos = [cv["tempo_resposta_min"] for cv in convs if cv["tempo_resposta_min"] is not None and cv["tempo_resposta_min"] >= 0]
        tempos_sorted = sorted(tempos)
        mediana = tempos_sorted[len(tempos_sorted)//2] if tempos_sorted else 0
        media = sum(tempos)//len(tempos) if tempos else 0
        notas = [cv["nota"] for cv in convs]
        nota_media = round(sum(notas)/len(notas), 1) if notas else 0
        # Argumentos contagem
        arg_count = {k: 0 for k in ARGUMENTOS.keys()}
        for cv in convs:
            for a in cv["argumentos_usados"]:
                if a in arg_count:
                    arg_count[a] += 1
        # Argumentos nao usados (criticos/altos)
        criticos_nao_usados = []
        for k, info_arg in ARGUMENTOS.items():
            if info_arg["importancia"] in ["Critica", "Alta"] and arg_count.get(k, 0) == 0:
                exemplos_clientes = [cv["cliente"] for cv in convs if k in cv["argumentos_perdidos"]][:3]
                if exemplos_clientes:
                    criticos_nao_usados.append({
                        "id": k,
                        "nome": info_arg["nome"],
                        "categoria": info_arg["categoria"],
                        "importancia": info_arg["importancia"],
                        "vezes_perdidas": len(convs),
                        "exemplo_aplicacao": f"Cliente {exemplos_clientes[0]}: aplicar {info_arg['nome']}"
                    })
        # Erros
        erros_count = defaultdict(int)
        for cv in convs:
            for e in cv["erros"]:
                erros_count[e] += 1
        erros_list = [{"codigo": k, "descricao": ERROS_DESC.get(k, k), "ocorrencias": v}
                      for k, v in sorted(erros_count.items())]

        # Pontos fortes/fracos
        pf, pfr = [], []
        if mediana > 0 and mediana <= 15:
            ex_rapidos = [f"Cliente {cv['cliente']}: respondeu em {cv['tempo_resposta_min']}min" for cv in convs if cv["tempo_resposta_min"] is not None and cv["tempo_resposta_min"] <= 15][:3]
            if ex_rapidos:
                pf.append({"categoria": "Velocidade", "descricao": f"Resposta rapida (mediana {mediana}min)", "exemplos": ex_rapidos})
        if arg_count.get("A3", 0) >= len(convs) * 0.4:
            ex_a3 = [f"Cliente {cv['cliente']}: vendedor pediu valor da conta" for cv in convs if "A3" in cv["argumentos_usados"]][:3]
            if ex_a3:
                pf.append({"categoria": "Qualificacao Inicial", "descricao": f"Frequente pergunta de qualificacao (A3 em {arg_count['A3']}/{len(convs)})", "exemplos": ex_a3})
        if arg_count.get("B4", 0) >= len(convs) * 0.3:
            ex_b4 = [f"Cliente {cv['cliente']}: vendedor ofereceu visita tecnica" for cv in convs if "B4" in cv["argumentos_usados"]][:3]
            if ex_b4:
                pf.append({"categoria": "Agendamento", "descricao": f"Oferece visita (B4 em {arg_count['B4']}/{len(convs)})", "exemplos": ex_b4})

        # Fracos
        if all(arg_count.get(d, 0) == 0 for d in ["D1", "D2", "D3", "D4"]):
            ex_d = [f"Cliente {cv['cliente']}: vendedor nao usou nenhum diferencial (D1-D4)" for cv in convs[:3]]
            pfr.append({
                "categoria": "Diferenciacao Competitiva",
                "descricao": "NUNCA mencionou laboratorio (D1), 17 anos (D2), 6mil projetos (D3) ou orfaos (D4)",
                "impacto": "Perde diferenciacao vs concorrentes",
                "conversas_afetadas": len(convs),
                "exemplos_clientes": ex_d,
                "acao_corretiva": "Incluir D1 (lab proprio + troca 24h) em todas conversas com objecao de preco/qualidade"
            })
        if arg_count.get("B4", 0) == 0 and arg_count.get("B1", 0) == 0:
            ex_v = [f"Cliente {cv['cliente']}: nao houve tentativa de visita" for cv in convs[:3]]
            pfr.append({
                "categoria": "Agendamento",
                "descricao": "Nao tentou agendar visita em nenhuma conversa hoje",
                "impacto": "Vende so pelo WhatsApp - alta perda de leads",
                "conversas_afetadas": len(convs),
                "exemplos_clientes": ex_v,
                "acao_corretiva": "Apos qualificacao oferecer visita: 'posso passar ai amanha?'"
            })
        if mediana > 60:
            ex_lentos = [f"Cliente {cv['cliente']}: respondeu em {cv['tempo_resposta_min']}min" for cv in convs if cv["tempo_resposta_min"] and cv["tempo_resposta_min"] > 60][:3]
            if ex_lentos:
                pfr.append({
                    "categoria": "Velocidade",
                    "descricao": f"Tempo de resposta mediano {mediana}min (acima de 60min)",
                    "impacto": "Lead esfria, concorrente atende primeiro",
                    "conversas_afetadas": sum(1 for cv in convs if cv["tempo_resposta_min"] and cv["tempo_resposta_min"] > 60),
                    "exemplos_clientes": ex_lentos,
                    "acao_corretiva": "Responder em ate 15min em horario comercial"
                })

        # Aderencia
        total_args = 12  # ponderacao simplificada (A2,A3,B1,B4,C1,C2,D1,D2,D3,D4,E5,F3)
        args_unicos = sum(1 for v in arg_count.values() if v > 0)
        aderencia = int((args_unicos / 28) * 100) if args_unicos else 0  # 28 args totais

        sem_resp_v = sum(1 for cv in convs if cv["status"] == "sem_resposta")
        crit_v = sum(1 for cv in convs if cv["status"] == "critico")

        vendedores_out.append({
            "nome": nome,
            "cor": info["cor"],
            "total_conversas": len(convs),
            "ligacoes_dia": LIGACOES.get(nome, 0),
            "sem_resposta": sem_resp_v,
            "criticas": crit_v,
            "mediana_resposta_min": mediana,
            "media_resposta_min": media,
            "total_respostas": len([cv for cv in convs if cv["status"] == "ok"]),
            "qualidade": {
                "nota_media": nota_media,
                "aderencia_script": aderencia,
                "argumentos_usados": arg_count,
                "argumentos_nao_usados": criticos_nao_usados,
                "pontos_fortes": pf,
                "pontos_fracos": pfr,
                "erros_cometidos": erros_list,
            },
        })

    # Ranking
    vendedores_out.sort(key=lambda v: v["qualidade"]["nota_media"], reverse=True)
    badges = ["Ouro", "Prata", "Bronze"]
    ranking = []
    for i, v in enumerate(vendedores_out):
        b = badges[i] if i < 3 else "Em desenvolvimento"
        ranking.append({
            "posicao": i+1,
            "vendedor": v["nome"],
            "nota_media": v["qualidade"]["nota_media"],
            "aderencia": v["qualidade"]["aderencia_script"],
            "badge": b
        })

    # Insights
    destaques, alertas, oportunidades = [], [], []
    for v in vendedores_out:
        convs_v = por_vendedor[v["nome"]]
        if convs_v and v["qualidade"]["nota_media"] >= 6:
            best = max(convs_v, key=lambda cv: cv["nota"])
            destaques.append({
                "vendedor": v["nome"],
                "cliente": best["cliente"],
                "acao": f"Cliente {best['cliente']}: {v['nome']} usou {','.join(best['argumentos_usados'][:5]) or 'argumentos basicos'}",
                "resultado": f"Nota {best['nota']}/10"
            })
        if v["criticas"] > 0:
            alertas.append({
                "vendedor": v["nome"],
                "problema": f"{v['criticas']} conversa(s) sem QUALQUER resposta do vendedor (X3)",
                "impacto": "Leads perdidos - cliente falou e foi ignorado",
                "acao_corretiva": "Revisar fila e responder leads pendentes"
            })
        if v["mediana_resposta_min"] > 60:
            alertas.append({
                "vendedor": v["nome"],
                "problema": f"Mediana de tempo de resposta: {v['mediana_resposta_min']}min (X8)",
                "impacto": "Leads esfriam antes da resposta",
                "acao_corretiva": "Responder em ate 15min em horario comercial"
            })

    arg_total = defaultdict(int)
    for v in vendedores_out:
        for k, c in v["qualidade"]["argumentos_usados"].items():
            arg_total[k] += c

    for k in ["D1", "D2", "D3", "D4"]:
        if arg_total[k] == 0:
            oportunidades.append({
                "tipo": "Diferenciacao subutilizada",
                "descricao": f"Argumento {k} ({ARGUMENTOS[k]['nome']}) NUNCA foi usado em nenhuma conversa hoje (DR4)",
                "acao_sugerida": f"Adicionar {ARGUMENTOS[k]['nome']} ao script padrao apos qualificacao"
            })
    if arg_total.get("B1", 0) < 5:
        oportunidades.append({
            "tipo": "Agendamento subutilizado",
            "descricao": "Gatilho de proximidade (B1) usado em pouquissimas conversas",
            "acao_sugerida": "Quando cliente mencionar bairro, oferecer visita 'tenho clientes pra atender ai perto'"
        })

    # Metricas gerais
    total = len(conversas_proc)
    nota_media_geral = round(sum(cv["nota"] for cv in conversas_proc) / total, 1) if total else 0
    aderencia_geral = round(sum(v["qualidade"]["aderencia_script"] for v in vendedores_out) / max(1, len(vendedores_out)))
    sem_resp_total = sum(1 for cv in conversas_proc if cv["status"] == "sem_resposta")
    crit_total = sum(1 for cv in conversas_proc if cv["status"] == "critico")
    sem_atrib_total = sum(1 for cv in conversas_proc if cv["vendedor"] == "Sem atribuicao")
    total_lig = sum(LIGACOES.values())

    output = {
        "data": DATA,
        "hora_execucao": HORA_EXEC,
        "observacao_metodologia": "Analise profunda do workspace DR4 (152352): cada conversa de hoje foi aberta e suas mensagens (texto + horario) coletadas via JS-injection. Filtragem por data 'Qua, 06 Mai 2026'. Conversas com nome contendo 'Ignorar' foram puladas. Argumentos detectados via regex sobre texto agregado do vendedor. Tempo de resposta calculado dentro do horario comercial 08:00-18:00.",
        "metricas": {
            "total_conversas": total,
            "sem_resposta": sem_resp_total,
            "total_ligacoes": total_lig,
            "criticas": crit_total,
            "sem_vendedor": sem_atrib_total,
            "nota_media_geral": nota_media_geral,
            "aderencia_geral": aderencia_geral,
        },
        "vendedores": vendedores_out,
        "insights": {
            "destaques_positivos": destaques[:6],
            "alertas": alertas[:8],
            "oportunidades": oportunidades[:6],
        },
        "ranking_qualidade": ranking,
        "conversas": conversas_proc,
    }

    with open(rf"C:/Botconversa/dados/{DATA}.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # Update index
    idx_path = r"C:/Botconversa/dados/index.json"
    try:
        with open(idx_path, encoding="utf-8") as f:
            idx = json.load(f)
    except Exception:
        idx = {"relatorios": []}
    relats = [r for r in idx.get("relatorios", []) if r.get("data") != DATA]
    relats.append({
        "data": DATA,
        "total_conversas": total,
        "sem_resposta": sem_resp_total,
        "criticas": crit_total,
        "nota_media": nota_media_geral,
        "vendedores": [v["nome"] for v in vendedores_out],
    })
    relats.sort(key=lambda r: r["data"], reverse=True)
    idx["relatorios"] = relats
    idx["ultima_atualizacao"] = f"{DATA}T{HORA_EXEC}"
    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)

    print(f"Saved {DATA}.json")
    print(f"Total conversas: {total}")
    print(f"Nota media geral: {nota_media_geral}")
    print(f"Aderencia geral: {aderencia_geral}%")
    print(f"Sem resposta: {sem_resp_total} | Criticas: {crit_total} | Sem atrib: {sem_atrib_total}")
    print(f"\nVendedores (ordenado por nota):")
    for v in vendedores_out:
        print(f"  {v['nome']}: {v['total_conversas']} convs | nota {v['qualidade']['nota_media']} | aderencia {v['qualidade']['aderencia_script']}% | mediana_resp {v['mediana_resposta_min']}min")

if __name__ == "__main__":
    main()
