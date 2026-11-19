

# ---------------------------- DADOS INICIAIS ----------------------------

bairro = "Jardim das Flores"

# Valores padronizados que o usuário digita no menu (sem acento).
categorias = ["iluminacao", "acessibilidade", "limpeza", "conservacao"]
status_validos = ["aberta", "em_analise", "concluida"]

# Nomes usados apenas na exibição para o usuário.
nomes_categorias = {
    "iluminacao": "Iluminação",
    "acessibilidade": "Acessibilidade",
    "limpeza": "Limpeza",
    "conservacao": "Conservação"
}

nomes_status = {
    "aberta": "Aberta",
    "em_analise": "Em análise",
    "concluida": "Concluída"
}

# Lista: guarda o conjunto principal de ocorrências.
ocorrencias = [
    {"codigo": "OC001", "categoria": "iluminacao", "descricao": "Poste apagado perto da escola", "local": "Rua das Flores", "dia_abertura": 1, "status": "em_analise", "dia_conclusao": None},
    {"codigo": "OC002", "categoria": "acessibilidade", "descricao": "Calçada sem rampa de acesso", "local": "Avenida Central", "dia_abertura": 2, "status": "aberta", "dia_conclusao": None},
    {"codigo": "OC003", "categoria": "limpeza", "descricao": "Acúmulo de lixo na praça", "local": "Praça Central", "dia_abertura": 3, "status": "concluida", "dia_conclusao": 7},
    {"codigo": "OC004", "categoria": "conservacao", "descricao": "Banco danificado", "local": "Praça das Árvores", "dia_abertura": 3, "status": "em_analise", "dia_conclusao": None},
    {"codigo": "OC005", "categoria": "iluminacao", "descricao": "Lâmpada quebrada", "local": "Rua do Sol", "dia_abertura": 4, "status": "concluida", "dia_conclusao": 8},
    {"codigo": "OC006", "categoria": "acessibilidade", "descricao": "Obstáculo na passagem de pedestres", "local": "Rua das Palmeiras", "dia_abertura": 5, "status": "em_analise", "dia_conclusao": None},
    {"codigo": "OC007", "categoria": "limpeza", "descricao": "Entulho próximo à calçada", "local": "Rua Azul", "dia_abertura": 6, "status": "aberta", "dia_conclusao": None},
    {"codigo": "OC008", "categoria": "conservacao", "descricao": "Buraco na área de lazer", "local": "Praça Central", "dia_abertura": 7, "status": "concluida", "dia_conclusao": 10},
    {"codigo": "OC009", "categoria": "iluminacao", "descricao": "Poste com luz piscando", "local": "Rua das Acácias", "dia_abertura": 8, "status": "em_analise", "dia_conclusao": None},
    {"codigo": "OC010", "categoria": "acessibilidade", "descricao": "Calçada irregular", "local": "Rua do Comércio", "dia_abertura": 9, "status": "concluida", "dia_conclusao": 12},
    {"codigo": "OC011", "categoria": "limpeza", "descricao": "Lixeira danificada e lixo no chão", "local": "Rua Verde", "dia_abertura": 10, "status": "aberta", "dia_conclusao": None},
    {"codigo": "OC012", "categoria": "conservacao", "descricao": "Playground precisando de reparo", "local": "Praça das Crianças", "dia_abertura": 11, "status": "concluida", "dia_conclusao": 15}
]

# Dicionário: permite localizar uma ocorrência diretamente pelo código.
ocorrencias_por_id = {}
for ocorrencia in ocorrencias:
    ocorrencias_por_id[ocorrencia["codigo"]] = ocorrencia

# Hierarquia: bairro -> categoria -> códigos das ocorrências.
hierarquia = {bairro: {}}
for categoria in categorias:
    hierarquia[bairro][categoria] = []

for ocorrencia in ocorrencias:
    categoria = ocorrencia["categoria"]
    hierarquia[bairro][categoria].append(ocorrencia["codigo"])

# Fila: ocorrências abertas aguardando análise, na ordem de registro.
fila_analise = []
for ocorrencia in ocorrencias:
    if ocorrencia["status"] == "aberta":
        fila_analise.append(ocorrencia["codigo"])

# Pilha: os eventos mais recentes ficam no final da lista.
# O sistema já começa com oito eventos simulados de acompanhamento.
pilha_atualizacoes = [
    {"codigo": "OC001", "dia": 2, "mensagem": "Status alterado de Aberta para Em análise."},
    {"codigo": "OC003", "dia": 7, "mensagem": "Status alterado de Em análise para Concluída."},
    {"codigo": "OC005", "dia": 8, "mensagem": "Status alterado de Em análise para Concluída."},
    {"codigo": "OC006", "dia": 9, "mensagem": "Ocorrência encaminhada para análise."},
    {"codigo": "OC008", "dia": 10, "mensagem": "Status alterado de Em análise para Concluída."},
    {"codigo": "OC009", "dia": 11, "mensagem": "Ocorrência encaminhada para análise."},
    {"codigo": "OC010", "dia": 12, "mensagem": "Status alterado de Em análise para Concluída."},
    {"codigo": "OC012", "dia": 15, "mensagem": "Status alterado de Em análise para Concluída."}
]


# ---------------------------- FUNÇÕES AUXILIARES ----------------------------

def validar_ocorrencia(registro):
    """Verifica campos obrigatórios, tipos, categoria, status e código."""
    campos_obrigatorios = ["codigo", "categoria", "descricao", "local", "dia_abertura", "status"]

    for campo in campos_obrigatorios:
        if campo not in registro or registro[campo] is None or registro[campo] == "":
            return False, "Campo obrigatório ausente ou vazio: " + campo

    # Os campos textuais precisam ser textos e não podem conter apenas espaços.
    campos_textuais = ["codigo", "categoria", "descricao", "local", "status"]
    for campo in campos_textuais:
        if not isinstance(registro[campo], str):
            return False, "O campo " + campo + " deve conter texto."
        if registro[campo].strip() == "":
            return False, "O campo " + campo + " não pode ficar vazio."

    codigo = registro["codigo"].strip().upper()
    if codigo in ocorrencias_por_id:
        return False, "Esse código já está cadastrado."

    if registro["categoria"] not in categorias:
        return False, "Categoria desconhecida."

    if registro["status"] not in status_validos:
        return False, "Status desconhecido."

    # bool é uma subclasse de int em Python, por isso é rejeitado separadamente.
    if isinstance(registro["dia_abertura"], bool) or not isinstance(registro["dia_abertura"], int) or registro["dia_abertura"] < 1:
        return False, "O dia de abertura deve ser um número inteiro positivo."

    return True, "Cadastro válido."


def ultimo_dia_registrado(codigo):
    """Retorna o dia do evento mais recente de uma ocorrência."""
    ultimo_dia = 0
    for evento in pilha_atualizacoes:
        if evento["codigo"] == codigo and evento["dia"] > ultimo_dia:
            ultimo_dia = evento["dia"]
    return ultimo_dia


def registrar_evento(codigo, dia, mensagem):
    """Empilha um novo evento no histórico."""
    evento = {"codigo": codigo, "dia": dia, "mensagem": mensagem}
    pilha_atualizacoes.append(evento)


def mostrar_status(status):
    if status in nomes_status:
        return nomes_status[status]
    return status


def mostrar_categoria(categoria):
    if categoria in nomes_categorias:
        return nomes_categorias[categoria]
    return categoria


def ler_dia(mensagem):
    """Lê um dia simulado. Retorna -1 quando o valor não é um número inteiro."""
    valor = input(mensagem).strip()
    if valor.isdigit():
        return int(valor)
    return -1


def porcentagem(parte, total):
    """Calcula a proporção em porcentagem, com uma casa decimal."""
    return round((parte / total) * 100, 1)


# ---------------------------- CADASTRO E CONSULTAS ----------------------------

def listar_ocorrencias():
    print("\n--- OCORRÊNCIAS CADASTRADAS ---")
    if len(ocorrencias) == 0:
        print("Nenhuma ocorrência cadastrada.")
    else:
        for ocorrencia in ocorrencias:
            print("Código:", ocorrencia["codigo"],
                  "| Categoria:", mostrar_categoria(ocorrencia["categoria"]),
                  "| Local:", ocorrencia["local"],
                  "| Status:", mostrar_status(ocorrencia["status"]))


def cadastrar_ocorrencia():
    print("\n--- NOVO CADASTRO ---")
    codigo = input("Código único (ex.: OC013): ").strip().upper()
    categoria = input("Categoria (iluminacao, acessibilidade, limpeza, conservacao): ").strip().lower()
    descricao = input("Descrição breve: ").strip()
    local = input("Localidade genérica: ").strip()
    dia_abertura = ler_dia("Dia simulado de abertura (número inteiro): ")

    nova_ocorrencia = {
        "codigo": codigo,
        "categoria": categoria,
        "descricao": descricao,
        "local": local,
        "dia_abertura": dia_abertura,
        "status": "aberta",
        "dia_conclusao": None
    }

    valido, mensagem = validar_ocorrencia(nova_ocorrencia)
    if valido:
        # O mesmo cadastro atualiza todas as estruturas de forma coordenada.
        ocorrencias.append(nova_ocorrencia)
        ocorrencias_por_id[codigo] = nova_ocorrencia
        hierarquia[bairro][categoria].append(codigo)
        fila_analise.append(codigo)
        registrar_evento(codigo, dia_abertura, "Ocorrência cadastrada com status Aberta.")
        print("Ocorrência cadastrada com sucesso!")
    else:
        print("Cadastro não realizado:", mensagem)


def consultar_por_codigo():
    codigo = input("Digite o código da ocorrência: ").strip().upper()
    if codigo in ocorrencias_por_id:
        ocorrencia = ocorrencias_por_id[codigo]
        print("\nCódigo:", ocorrencia["codigo"])
        print("Categoria:", mostrar_categoria(ocorrencia["categoria"]))
        print("Descrição:", ocorrencia["descricao"])
        print("Local:", ocorrencia["local"])
        print("Dia de abertura:", ocorrencia["dia_abertura"])
        print("Status:", mostrar_status(ocorrencia["status"]))
        if ocorrencia["dia_conclusao"] is not None:
            print("Dia de conclusão:", ocorrencia["dia_conclusao"])
    else:
        print("Ocorrência não encontrada.")


def filtrar_ocorrencias():
    categoria = input("Categoria (iluminacao, acessibilidade, limpeza, conservacao ou todas): ").strip().lower()
    status = input("Status (aberta, em_analise, concluida ou todos): ").strip().lower()

    if categoria != "todas" and categoria not in categorias:
        print("Categoria inválida.")
        return

    if status != "todos" and status not in status_validos:
        print("Status inválido.")
        return

    encontrou = False
    print("\n--- RESULTADO DO FILTRO ---")
    for ocorrencia in ocorrencias:
        # AND combina os dois filtros; OR permite escolher todas as categorias ou todos os status.
        if (categoria == "todas" or ocorrencia["categoria"] == categoria) and (status == "todos" or ocorrencia["status"] == status):
            print(ocorrencia["codigo"], "|", mostrar_categoria(ocorrencia["categoria"]), "|", ocorrencia["local"], "|", mostrar_status(ocorrencia["status"]))
            encontrou = True

    if not encontrou:
        print("Nenhuma ocorrência corresponde aos filtros.")


# ---------------------------- FILA E PILHA ----------------------------

def mostrar_fila():
    print("\n--- FILA DE OCORRÊNCIAS AGUARDANDO ANÁLISE ---")
    if len(fila_analise) == 0:
        print("A fila está vazia.")
    else:
        for codigo in fila_analise:
            ocorrencia = ocorrencias_por_id[codigo]
            print(codigo, "|", ocorrencia["descricao"], "|", ocorrencia["local"])


def processar_proxima_da_fila():
    if len(fila_analise) == 0:
        print("Não há ocorrências aguardando análise.")
        return

    # Consulta o primeiro código sem retirá-lo da fila antes de validar o dia.
    codigo = fila_analise[0]
    ocorrencia = ocorrencias_por_id[codigo]
    print("Próxima da fila:", codigo, "|", ocorrencia["descricao"])
    dia_evento = ler_dia("Dia simulado em que a ocorrência foi analisada: ")

    if dia_evento < ocorrencia["dia_abertura"]:
        print("Dia inválido. A data não pode ser anterior à abertura.")
        return

    if dia_evento < ultimo_dia_registrado(codigo):
        print("Dia inválido. A data não pode ser anterior ao último evento.")
        return

    fila_analise.pop(0)
    status_anterior = ocorrencia["status"]
    ocorrencia["status"] = "em_analise"
    registrar_evento(codigo, dia_evento, "Status alterado de " + mostrar_status(status_anterior) + " para Em análise pela fila.")
    print("A ocorrência", codigo, "foi encaminhada para análise.")


def atualizar_status():
    codigo = input("Código da ocorrência: ").strip().upper()

    if codigo not in ocorrencias_por_id:
        print("Ocorrência não encontrada.")
        return

    ocorrencia = ocorrencias_por_id[codigo]
    print("Status atual:", mostrar_status(ocorrencia["status"]))
    novo_status = input("Novo status (aberta, em_analise, concluida): ").strip().lower()

    # NOT e OR rejeitam um status desconhecido ou igual ao atual.
    if not (novo_status in status_validos) or novo_status == ocorrencia["status"]:
        print("Status inválido ou igual ao status atual. Nenhuma alteração realizada.")
        return

    dia_evento = ler_dia("Dia simulado da atualização: ")
    if dia_evento < 1:
        print("Dia inválido. Nenhuma alteração realizada.")
        return

    if dia_evento < ocorrencia["dia_abertura"]:
        print("A data da atualização não pode ser anterior à abertura.")
        return

    if dia_evento < ultimo_dia_registrado(codigo):
        print("A data da atualização não pode ser anterior ao último evento.")
        return

    if novo_status == "concluida":
        ocorrencia["dia_conclusao"] = dia_evento
    else:
        ocorrencia["dia_conclusao"] = None

    status_anterior = ocorrencia["status"]
    ocorrencia["status"] = novo_status

    # Só ocorrências abertas ficam na fila de análise.
    if novo_status == "aberta":
        if codigo not in fila_analise:
            fila_analise.append(codigo)
    else:
        if codigo in fila_analise:
            fila_analise.remove(codigo)

    mensagem = "Status alterado de " + mostrar_status(status_anterior) + " para " + mostrar_status(novo_status) + "."
    registrar_evento(codigo, dia_evento, mensagem)
    print("Status atualizado com sucesso!")


def mostrar_historico():
    print("\n--- HISTÓRICO: EVENTOS MAIS RECENTES PRIMEIRO ---")
    if len(pilha_atualizacoes) == 0:
        print("Ainda não existem eventos.")
    else:
        # A pilha é percorrida de trás para frente, sem remover os eventos.
        for indice in range(len(pilha_atualizacoes) - 1, -1, -1):
            evento = pilha_atualizacoes[indice]
            print("Dia", evento["dia"], "|", evento["codigo"], "|", evento["mensagem"])


# ---------------------------- INDICADORES E MATRIZ ----------------------------

def mostrar_indicadores():
    total = len(ocorrencias)
    if total == 0:
        print("Não há ocorrências para calcular os indicadores.")
        return

    contagem_categoria = {}
    contagem_status = {}

    for categoria in categorias:
        contagem_categoria[categoria] = 0

    for status in status_validos:
        contagem_status[status] = 0

    for ocorrencia in ocorrencias:
        contagem_categoria[ocorrencia["categoria"]] = contagem_categoria[ocorrencia["categoria"]] + 1
        contagem_status[ocorrencia["status"]] = contagem_status[ocorrencia["status"]] + 1

    # Matriz: as linhas representam categorias e as colunas representam status.
    matriz = []
    for categoria in categorias:
        linha = []
        for status in status_validos:
            quantidade = 0
            for ocorrencia in ocorrencias:
                if ocorrencia["categoria"] == categoria and ocorrencia["status"] == status:
                    quantidade = quantidade + 1
            linha.append(quantidade)
        matriz.append(linha)

    print("\n========== PAINEL DO BAIRRO", bairro.upper(), "==========")
    print("Total de ocorrências:", total)

    print("\nQuantidade por categoria:")
    for categoria in categorias:
        quantidade = contagem_categoria[categoria]
        print(" ", mostrar_categoria(categoria) + ":", quantidade, "(" + str(porcentagem(quantidade, total)) + "%)")

    print("\nQuantidade por status:")
    for status in status_validos:
        quantidade = contagem_status[status]
        print(" ", mostrar_status(status) + ":", quantidade, "(" + str(porcentagem(quantidade, total)) + "%)")

    print("\nMatriz categoria x status")
    print("Categoria".ljust(16), "Aberta".rjust(8), "Em análise".rjust(12), "Concluída".rjust(11))
    for indice in range(len(categorias)):
        print(mostrar_categoria(categorias[indice]).ljust(16),
              str(matriz[indice][0]).rjust(8),
              str(matriz[indice][1]).rjust(12),
              str(matriz[indice][2]).rjust(11))

    pendentes = total - contagem_status["concluida"]
    print("\nTotal de pendências (abertas + em análise):", pendentes)

    # Indicador adicional: tempo médio simulado entre abertura e conclusão.
    soma_dias = 0
    quantidade_concluidas = 0
    for ocorrencia in ocorrencias:
        if ocorrencia["status"] == "concluida" and ocorrencia["dia_conclusao"] is not None:
            soma_dias = soma_dias + (ocorrencia["dia_conclusao"] - ocorrencia["dia_abertura"])
            quantidade_concluidas = quantidade_concluidas + 1

    if quantidade_concluidas > 0:
        media = soma_dias / quantidade_concluidas
        print("Tempo médio simulado entre abertura e conclusão:", round(media, 1), "dia(s)")
    else:
        print("Ainda não há ocorrências concluídas para calcular o tempo médio.")

    print("\nInterpretação dos resultados:")

    maior_quantidade = 0
    categorias_mais_frequentes = []
    for categoria in categorias:
        quantidade = contagem_categoria[categoria]
        if quantidade > maior_quantidade:
            maior_quantidade = quantidade
            categorias_mais_frequentes = [mostrar_categoria(categoria)]
        elif quantidade == maior_quantidade:
            categorias_mais_frequentes.append(mostrar_categoria(categoria))

    if len(categorias_mais_frequentes) == len(categorias):
        print("As ocorrências estão distribuídas igualmente entre as quatro categorias.")
    elif len(categorias_mais_frequentes) == 1:
        print("A categoria com mais registros é", categorias_mais_frequentes[0], "com", maior_quantidade, "ocorrência(s).")
    else:
        print("As categorias com mais registros são", ", ".join(categorias_mais_frequentes), "com", maior_quantidade, "ocorrência(s) cada.")

    concluidas = contagem_status["concluida"]
    print("Há", pendentes, "pendência(s), o que equivale a", str(porcentagem(pendentes, total)) + "% do total.")
    print(concluidas, "ocorrência(s) concluída(s), o que equivale a", str(porcentagem(concluidas, total)) + "% do total.")
    if pendentes > concluidas:
        print("A maioria dos registros ainda precisa de acompanhamento.")
    elif pendentes < concluidas:
        print("A maioria dos registros já foi concluída no conjunto simulado.")
    else:
        print("Há a mesma quantidade de pendências e de ocorrências concluídas.")


def mostrar_hierarquia():
    print("\n--- HIERARQUIA DE OCORRÊNCIAS ---")
    print(bairro)
    for categoria in categorias:
        codigos = hierarquia[bairro][categoria]
        if len(codigos) == 0:
            print("  ", mostrar_categoria(categoria) + ": nenhuma ocorrência")
        else:
            print("  ", mostrar_categoria(categoria) + ":", ", ".join(codigos))


def demonstrar_validacao():
    # Registro propositalmente incompleto: está sem o campo "local".
    registro_incompleto = {
        "codigo": "OC999",
        "categoria": "iluminacao",
        "descricao": "Registro de teste incompleto",
        "dia_abertura": 16,
        "status": "aberta"
    }

    valido, mensagem = validar_ocorrencia(registro_incompleto)
    print("\n--- TESTE DE VALIDAÇÃO ---")
    print("Foi analisado um registro de teste sem o campo local.")
    print("Resultado:", mensagem)
    if not valido:
        print("Tratamento: o registro foi rejeitado e não entrou na lista de ocorrências.")


# ---------------------------- MENU PRINCIPAL ----------------------------

def menu():
    demonstrar_validacao()

    while True:
        print("\n==========================================")
        print("      NEIGHBORHOOD ACTION DASHBOARD")
        print("      Bairro:", bairro)
        print("==========================================")
        print("1 - Listar ocorrências")
        print("2 - Cadastrar ocorrência")
        print("3 - Consultar por código")
        print("4 - Filtrar por categoria e/ou status")
        print("5 - Atualizar status")
        print("6 - Mostrar fila de análise")
        print("7 - Processar próxima ocorrência da fila")
        print("8 - Consultar histórico de atualizações")
        print("9 - Mostrar indicadores")
        print("10 - Mostrar hierarquia")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            listar_ocorrencias()
        elif opcao == "2":
            cadastrar_ocorrencia()
        elif opcao == "3":
            consultar_por_codigo()
        elif opcao == "4":
            filtrar_ocorrencias()
        elif opcao == "5":
            atualizar_status()
        elif opcao == "6":
            mostrar_fila()
        elif opcao == "7":
            processar_proxima_da_fila()
        elif opcao == "8":
            mostrar_historico()
        elif opcao == "9":
            mostrar_indicadores()
        elif opcao == "10":
            mostrar_hierarquia()
        elif opcao == "0":
            print("Encerrando o Neighborhood Action Dashboard. Até mais!")
            break
        else:
            print("Opção inválida. Escolha uma opção do menu.")


# O programa começa pelo menu principal.
if __name__ == "__main__":
    menu()
