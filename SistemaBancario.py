menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
"""

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

def formatar_numero(numero):
    return f"R$ {numero:.2f}"

def depositar(saldo, extrato):
    try:
        deposito = float(input("Digite o valor a ser depositado: "))
        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito: {formatar_numero(deposito)}\n"
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")
    except ValueError:
        print("Valor inválido. Por favor, insira um número.")
    return saldo, extrato

def sacar(saldo, limite, extrato, numero_saques):
    try:
        valor = float(input("Informe o valor do saque: "))
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: {formatar_numero(valor)}\n"
            numero_saques += 1
            print("Saque realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")
    except ValueError:
        print("Valor inválido. Por favor, insira um número.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    print("\n" + "=" * 20 + " Extrato " + "=" * 20 + "\n")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: {formatar_numero(saldo)}")
    print("=" * 49)

# Loop principal
while True:
    opcao = input(menu).lower()

    if opcao == "d":
        saldo, extrato = depositar(saldo, extrato)

    elif opcao == "s":
        saldo, extrato, numero_saques = sacar(saldo, limite, extrato, numero_saques)

    elif opcao == "e":
        exibir_extrato(saldo, extrato)

    elif opcao == "q":
        print("Saindo do sistema...")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
