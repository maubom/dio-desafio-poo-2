from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):        
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta,  transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)
     
class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):        
        return self._saldo
            
    @property
    def numero(self):        
        return self._numero
    
    @property
    def agencia(self):        
        return self._agencia
    
    @property
    def cliente(self):        
        return self._cliente
    
    @property
    def historico(self):        
        return self._historico
          
    @classmethod
    def nova_conta(cls, cliente , numero ): 
        return cls(numero, cliente) 
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realizado!")
            return True
        else:
            print("Valor invalido!")
        return False
    
    def sacar(self, valor):                       
        if self._saldo < valor:  
            print("\n***   Saldo insuficiente!   ***")                      
        elif valor <=  0:
            print("\n***   Valor inválido!   ***")            
        else:
            self._saldo -= valor
            print("\nSaque realizado!")
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor) :        
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        if self._saldo < valor:
            print("\n***   Saldo insuficiente!   ***")
        elif numero_saques >= self.limite_saques:
            print("\nLimite de saques excedido!")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self) -> str:
        return f"""\
            Agencia: {self.agencia}
            Conta Corrente: {self.numero}
            Titular: {self.cliente.nome}
        """
       
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
        
    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": type(transacao).__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
        })

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass
            
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


menu = """
    =================================
    =        Sistema Bancario       =
    =================================
    = 1 - Depositar Dinheiro        =
    = 2 - Sacar Dinheiro            =
    = 3 - Ver Extrato               =
    = 4 - Cadastrar cliente         =
    = 5 - Listar cliente            =
    = 6 - Cadastrar conta           =
    = 7 - Listar conta              =
    = 8 - Sair                      =
    =================================
    
    Entre com a opção desejada: 
"""

def cadastrar_cliente(clientes):
    try:
        cpf = int(input("Digite o CPF do cliente, apenas numeros: ") )
    except ValueError:
        print("\n***   CPF invalido, apenas numeros   ***")
        return
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\n***   CPF ja cadastrado   ***")
        return
    
    nome = input("Digite o nome do cliente completo: ")
    data_nascimento = input("Informe a data do nascimento (dd-mm-aaaa): ")
    endereco = input("Digite o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,cpf=cpf,endereco=endereco)
    
    clientes.append(cliente)
    
    print("\n   Cliente cadastrado!\n")
    return 

def filtrar_cliente(cpf, clientes):    
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]  
    return clientes_filtrados[0] if clientes_filtrados else None

def listar_cliente(clientes):
    for cliente in clientes:
        print(f"Nome: {cliente.nome}, CPF: {cliente.cpf}")
    return

def cadastrar_conta(conta_numero, clientes, contas):
    try:
        cpf = int(input("Digite o CPF do cliente, apenas numeros: ") )
    except ValueError:
        print("\n***   CPF invalido, apenas numeros   ***")
        return
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\n***   Cliente não existe, cadastro de conta não realizado!   ***\n")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=conta_numero)
    contas.append(conta)
    cliente.contas.append(conta)
    
    print("\n   Conta criada!\n")

def listar_contas(contas):    
    for conta in contas:        
        print("=" * 50)
        print(str(conta))
    return

def recuperar_conta_cliente(cliente):    
    if not cliente.contas:
        print("\n***   Conta não existe!   ***\n")
        return
    return cliente.contas[0]

def depositar(clientes):
    try:
        cpf = int(input("Digite o CPF do cliente, apenas numeros: ") )
    except ValueError:
        print("\n***   CPF invalido, apenas numeros   ***")
        return  
    cliente = filtrar_cliente(cpf, clientes)
        
    if not cliente:
        print("\n***   Cliente não existe   ***")
        return
    try:
        valor = float(input("\n    Qual valor você deseja sacar? R$ "))
    except ValueError:
        print("\n***   Valor inválido   ***")
        return
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("\n***   Conta não existe   ***")
        return
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    try:
        cpf = int(input("Digite o CPF do cliente, apenas numeros: ") )
    except ValueError:
        print("\n***   CPF invalido, apenas numeros   ***")
        return 
    cliente = filtrar_cliente(cpf,clientes)
        
    if not cliente:
        print("\n***   Cliente não existe   ***")
        return
    try:
        valor = float(input("\n    Qual valor você deseja sacar? R$ "))
    except ValueError:
        print("\n***   Valor inválido   ***")
        return
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("\n***   Conta não existe   ***")
        return
    cliente.realizar_transacao(conta, transacao)    

def mostrar_extrato(clientes):
    try:
        cpf = int(input("Digite o CPF do cliente, apenas numeros: ") )
    except ValueError:
        print("\n***   CPF invalido, apenas numeros   ***")
        return
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\n***   Cliente não existe   ***")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("\n***   Conta não existe   ***")
        return
    print("\n======    Extrato    ======")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "***   Não há transações   ***"
    else:
        for transacao in transacoes:            
            extrato += f"\nData: {transacao['data']}\tTipo: {transacao['tipo']}\tValor: R$ {transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("\n===========================")
    
def main():    
    clientes = []
    contas = []
    
    while True:     
        try: 
            opcao = int(input(menu))
        except ValueError:
            print("\n\n***    Opção inválida. Por favor, tente novamente.   ***\n")
            continue
        match opcao:
            case 1:
                depositar(clientes)                
            case 2:
                sacar(clientes)
            case 3:
                mostrar_extrato(clientes)
            case 4:
                cadastrar_cliente(clientes)
            case 5:
                listar_cliente(clientes)
            case 6:   
                conta_numero = len(contas) + 1                           
                cadastrar_conta(conta_numero, clientes, contas)                
            case 7:
                listar_contas(contas)
            case 8:
                print("\n\nAté logo.\n\n--------------")
                break
            case _:
                print("\n\n***    Opção inválida. Por favor, tente novamente.")

main()       

        
        
        
        
