import re
from datetime import datetime

# Funções de CPF e Data
def limpar_cpf(cpf):
    return re.sub(r'\D', '', cpf)

def formatar_cpf(cpf):
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

def validar_data(data):
    try:
        return datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        return False

    # Implementar a lógica de validação do CPF
def validar_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    return True

# Funções de operação bancária
def depositar(saldo, extrato):
    try:
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("Operação falhou! O valor informado é inválido.")
    except ValueError:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    try:
        valor = float(valor)
    except ValueError:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato, numero_saques

    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Funções de usuário e conta
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    cpf = limpar_cpf(cpf)

    if not validar_cpf(cpf):
        print("CPF inválido! Por favor, insira um CPF válido.")
        return None  # Retorna None se o CPF não for válido

    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("Já existe um usuário com esse CPF!")
        return None  # Retorna None se o usuário já existir

    nome = input("Informe o nome: ")
    
    # Validação da data de nascimento
    while True:
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        data_valida = validar_data(data_nascimento)
        if data_valida:
            break
        else:
            print("Data inválida! Por favor, insira no formato correto (dd/mm/aaaa).")

    logradouro = input("Informe o logradouro: ")
    numero = input("Informe o número: ")
    bairro = input("Informe o bairro: ")
    cidade_uf = input("Informe a cidade e estado (cidade/UF): ")

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade_uf}"

    usuario = {
        "nome": nome,
        "data_nascimento": data_valida.strftime("%d/%m/%Y"),  # Armazena a data formatada
        "cpf": cpf,
        "endereco": endereco
    }

    usuarios.append(usuario)
    print("\n=== Usuário criado com sucesso! ===")
    return usuario  # Retorna o usuário criado

def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        for usuario in usuarios:
            cpf_formatado = formatar_cpf(usuario["cpf"])
            print("=" * 50)
            print(f"Nome: {usuario['nome']}")
            print(f"Data de Nascimento: {usuario['data_nascimento']}")
            print(f"CPF: {cpf_formatado}")
            print(f"Endereço: {usuario['endereco']}")
            print("=" * 50)

def criar_conta(usuarios, contas, numero_conta, usuario):
    contas.append({
        "agencia": "0001",
        "numero_conta": numero_conta,
        "usuario": usuario
    })
    print(f"\n=== Conta {numero_conta:03d} criada com sucesso para o usuário {usuario['nome']}! ===")
    return numero_conta + 1

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            cpf_formatado = formatar_cpf(conta["usuario"]["cpf"])
            print("=" * 50)
            print(f"Agência: {conta['agencia']}")
            print(f"Conta: {conta['numero_conta']:03d}")
            print(f"Titular: {conta['usuario']['nome']}")
            print(f"CPF do Titular: {cpf_formatado}")
            print("=" * 50)

# Função principal  menu 
def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    numero_conta = 1  # Inicia as contas com 001

    menu = """
[d] Depositar
[s] Sacar
[e] Exibir Extrato
[nu] Novo Usuário
[lu] Listar Usuários
[nc] Nova Conta Corrente
[lc] Listar Contas
[q] Sair
=> """

    while True:
        opcao = input(menu)

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)

        elif opcao == "s":
            valor = input("Informe o valor do saque: ")
            saldo, extrato, numero_saques = sacar(
                saldo=saldo, valor=valor, extrato=extrato, 
                limite=limite, numero_saques=numero_saques, 
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            usuario = criar_usuario(usuarios)
            if usuario:  # Se o usuário foi criado com sucesso
                numero_conta = criar_conta(usuarios, contas, numero_conta, usuario)
        
        elif opcao == "lu":
            listar_usuarios(usuarios)
        
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Saindo... Até logo!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
