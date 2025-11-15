# trabalho_algoritmos_logica.py
# Sistema de Controle de Pecas - Automacão Digital
# Autor: Joaquim Alves
# Disciplina: Algoritmos e Lógica de Programacão
# Requisitos do menu:
# 1. Cadastrar nova peca
# 2. Listar pecas aprovadas/reprovadas
# 3. Remover peca cadastrada
# 4. Listar caixas fechadas
# 5. Gerar relatório final

lista_pecas = []
caixas = []
CAIXA_CAPACIDADE = 10


def avaliar_peca(peso, cor, comprimento):
    """Retorna lista de motivos de reprovacão (vazia se aprovada)."""
    motivos = []
    if not (95 <= peso <= 105):
        motivos.append("Peso fora do padrão")
    if cor.lower() not in ["azul", "verde"]:
        motivos.append("Cor inválida (permitido: azul ou verde)")
    if not (10 <= comprimento <= 20):
        motivos.append("Comprimento fora do padrão")
    return motivos


def armazenar_peca(peca):
    """Guarda a peca aprovada na última caixa aberta ou cria nova se necessário."""
    if not caixas or len(caixas[-1]) >= CAIXA_CAPACIDADE:
        caixas.append([])
    caixas[-1].append(peca)


def cadastrar_peca():
    print("\n=== Cadastro de peca ===")
    id_peca = input("ID da peca: ").strip()
    # impedir IDs duplicados
    for p in lista_pecas:
        if p["id"] == id_peca:
            print("Já existe uma peca com esse ID. Operacão cancelada.\n")
            return
    try:
        peso = float(input("Peso (g): ").replace(",", "."))
        cor = input("Cor (azul/verde): ").strip()
        comprimento = float(input("Comprimento (cm): ").replace(",", "."))
    except ValueError:
        print("Valores inválidos. Tente novamente.\n")
        return

    motivos = avaliar_peca(peso, cor, comprimento)
    status = "Aprovada" if len(motivos) == 0 else "Reprovada"

    peca = {
        "id": id_peca,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento,
        "status": status,
        "motivos": motivos
    }
    lista_pecas.append(peca)

    if status == "Aprovada":
        armazenar_peca(peca)

    print(f"Peca {status}!\n")
    if motivos:
        print("Motivos:", ", ".join(motivos))
        print()


def listar_pecas():
    if not lista_pecas:
        print("Nenhuma peca cadastrada.\n")
        return
    aprovadas = [p for p in lista_pecas if p["status"] == "Aprovada"]
    reprovadas = [p for p in lista_pecas if p["status"] == "Reprovada"]

    print("\n=== Pecas Aprovadas ===")
    if aprovadas:
        for p in aprovadas:
            print(
                f"ID: {p['id']} | Peso: {p['peso']}g | Cor: {p['cor']} | Comp: {p['comprimento']}cm")
    else:
        print("Nenhuma.")

    print("\n=== Pecas Reprovadas ===")
    if reprovadas:
        for p in reprovadas:
            print(f"ID: {p['id']} | Motivos: {', '.join(p['motivos'])} "+
                  " | Peso: {p['peso']}g | Cor: {p['cor']} | Comp: {p['comprimento']}cm")
    else:
        print("Nenhuma.")
    print()


def remover_peca():
    if not lista_pecas:
        print("Não há pecas para remover.\n")
        return
    id_remover = input("Informe o ID da peca para remover: ").strip()
    # Remover da lista principal
    idx = next((i for i, p in enumerate(lista_pecas)
               if p["id"] == id_remover), None)
    if idx is None:
        print("Peca não encontrada.\n")
        return
    alvo = lista_pecas[idx]
    # Se estava em caixa, remover da caixa
    if alvo["status"] == "Aprovada":
        for caixa in caixas:
            for p in list(caixa):
                if p["id"] == id_remover:
                    caixa.remove(p)
                    break
        # remover caixas vazias no final da lista
        while caixas and len(caixas[-1]) == 0:
            caixas.pop()
    lista_pecas.pop(idx)
    print("Peca removida.\n")


def listar_caixas_fechadas():
    """Exibe apenas caixas com 10 pecas (fechadas)."""
    fechadas = [c for c in caixas if len(c) >= CAIXA_CAPACIDADE]
    if not fechadas:
        print("Nenhuma caixa fechada.\n")
        return
    print("\n=== Caixas Fechadas ===")
    for i, caixa in enumerate(fechadas, 1):
        ids = ", ".join([p["id"] for p in caixa])
        print(f"Caixa {i} - {len(caixa)} pecas | IDs: {ids}")
    print()


def gerar_relatorio():
    aprovadas = [p for p in lista_pecas if p["status"] == "Aprovada"]
    reprovadas = [p for p in lista_pecas if p["status"] == "Reprovada"]

    print("\n===== RELATÓRIO FINAL =====")
    print(f"Total de pecas aprovadas: {len(aprovadas)}")
    print(f"Total de pecas reprovadas: {len(reprovadas)}")
    if reprovadas:
        print("\nMotivos de reprovacão por peca:")
        for p in reprovadas:
            print(f" - ID {p['id']}: {', '.join(p['motivos'])}")
    caixas_utilizadas = sum(1 for c in caixas if len(c) > 0)
    print(f"\nCaixas utilizadas: {caixas_utilizadas}")
    print("===========================\n")


def menu():
    while True:
        print("==== MENU ====")
        print("1. Cadastrar nova peca")
        print("2. Listar pecas aprovadas/reprovadas")
        print("3. Remover peca cadastrada")
        print("4. Listar caixas fechadas")
        print("5. Gerar relatório final")
        print("0. Sair")

        opcao = input("Escolha: ").strip()

        match opcao:
            case "1":
                cadastrar_peca()
            case "2":
                listar_pecas()
            case "3":
                remover_peca()
            case "4":
                listar_caixas_fechadas()
            case "5":
                gerar_relatorio()
            case "0":
                print("Encerrando...")
                break
            case _:
                print("Opção inválida!\n")


if __name__ == "__main__":
    menu()
