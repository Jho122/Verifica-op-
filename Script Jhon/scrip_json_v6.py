import ipaddress
import netmiko # type: ignore
from netmiko import ConnectHandler # type: ignore
from getpass import getpass
from datetime import datetime
import os
import json  # Certifique-se de importar esta biblioteca
from datetime import datetime
import re

# Versionamento do código
VERSION = "1.2.0"
ERRO_LOG_PATH = r"C:\Users\jhonatas.rodrigues\Desktop\erro_log.txt"

def registrar_erro(mensagem):
    """Registra uma mensagem de erro no arquivo de log."""
    with open(ERRO_LOG_PATH, "a") as log_file:
        log_file.write(f"{datetime.now()} - {mensagem}\n")

def executar_comando(device_params, comando):
    """Tenta conectar-se ao dispositivo e executar um comando."""
    try:
        print(f"Conectando ao dispositivo {device_params['host']}...")
        net_connect = netmiko.ConnectHandler(**device_params)
        net_connect.enable()
        output = net_connect.send_command(comando)
        net_connect.disconnect()
        return output
    except netmiko.NetmikoTimeoutException as e:
        registrar_erro(f"Timeout ao conectar-se ao {device_params['host']}: {str(e)}")
        print("Erro: Tempo limite ao conectar-se ao dispositivo.")
    except netmiko.NetmikoAuthenticationException as e:
        registrar_erro(f"Falha de autenticação no {device_params['host']}: {str(e)}")
        print("Erro: Falha de autenticação.")
    except Exception as e:
        registrar_erro(f"Erro inesperado no {device_params['host']}: {str(e)}")
        print("Erro inesperado ao executar o comando.")
    return None

def menu_principal():
    print("\n=== Menu Principal ===")
    print("1 - Firewall")
    print("2 - Fortinet")
    print("3 - Palo Alto em Desenvolvimento")
    print("4 - Router em Desenvolvimento")
    print("5 - Switch em Desenvolvimento")
    print("6 - APIC em Desenvolvimento")
    print("7 - Sair")
    return input("Escolha uma opção: ")

# Menu de Verificação e Configiração 
def menu_firewall():
    print("\n=== Menu Firewall ===")
    print("1 - Verificação")
    print("2 - Configuração")
    print("3 - Voltar")
    return input("Escolha uma opção: ")

# Menu de Verificação
def menu_verificacao_firewall():
    print("\n=== Verificação de Firewall ===")
    print("1 - Interface")
    print("2 - Regras de Firewall")
    print("3 - Teste de Regra")
    print("4 - Captura de Pacotes")
    print("5 - Análise de Rotas")
    print("6 - Verificação de NAT")
    print("7 - Verificação de Object-Group")
    print("8 - Verificação de VPN")
    print("9 - Verificação de Configuração")
    print("10 - Voltar")
    print("11 - Verificação de Status de Link")
    print("12 - Verificação de SLA Monitor")
    print("13 - Verificação de VPNs L2L Ativas")
    print("14 - Total de VPNs Configuradas Ativas")
    return input("Escolha uma opção: ")

# Menu Fortinet
def menu_fortinet():
    print("\n=== Menu Fortinet ===")
    print("1 - Verificação de VPN")
    print("2 - Verificação de Nat")
    print("3 - Captura de Pacotes")
    print("4 - Analise de rota")
    print("5 - Voltar")
    return input("Escolha uma opção: ")

#Menu Paulo Alto
def menu_Paloalto():
    print("\n=== Menu Palo Alto ===")
    print("1 - Verificação de NAT")
    print("2 - Verificação de Rota")
    print("3 - Teste de Regra")
    print("4 - Voltar")
    return input("Escolha uma opção: ")

# Menu de Configuração ASA 
def menu_configuracao_asa():
    print("\n=== Menu de Configuração da Regra ===")
    print("1. Criar regra de acesso ASA ")
    print("2. Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

# FUNCOES DE VERIFICAÇÕES 
    # Nova função para verificação de VPN Cisco
def verificar_vpn(device_params):
    ip_vpn = input("Digite o IP para verificação de VPN: ")
    comando = f"show vpn-sessiondb detail l2l filter ipaddress {ip_vpn}"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Detalhes da VPN ---")
        print(output)
    else:
        print("Erro ao verificar a VPN ou nenhuma sessão encontrada para esse IP.")

# Nova função para verificação de configuração
def verificar_configuracao(device_params):
    nome_parceiro = input("Digite o nome do parceiro: ")
    comando = f"show run | include {nome_parceiro.upper()}|{nome_parceiro.lower()}"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Configuração associada ao parceiro ---")
        print(output)
    else:
        print("Erro ao verificar a configuração ou nenhuma configuração encontrada para esse parceiro.")

# Funções Cisco
def verificar_interface(device_params):
    comando = "show interface ip brief"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Interfaces do Firewall ---")
        print(output)
    else:
        print("Erro ao obter as interfaces.")

    

def verificar_regra_firewall(device_params):
    ip_especifico = input("Digite o IP para verificar nas regras de firewall: ")
    comando = f"show run access-list | include {ip_especifico}"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Regras associadas ao IP ---")
        print(output)
    else:
        print("Nenhuma regra encontrada para esse IP.")

def testar_regra_packet_tracer(device_params):
    interface_entrada = input("Digite a interface de entrada (ex: nucleo): ")
    ip_origem = input("Digite o IP de origem: ")
    porta_origem = input("Digite a porta de origem: ")
    ip_destino = input("Digite o IP de destino: ")
    porta_destino = input("Digite a porta de destino: ")
    protocolo = "tcp"
    comando = f"packet-tracer input {interface_entrada} {protocolo} {ip_origem} {porta_origem} {ip_destino} {porta_destino}"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Resultado do teste de regra com packet-tracer ---")
        print(output)
    else:
        print("Erro ao realizar o teste de regra com packet-tracer.")



def validar_ip(ip):
    """Valida o formato de um endereço IP."""
    padrao = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(padrao, ip):
        partes = ip.split('.')
        return all(0 <= int(parte) <= 255 for parte in partes)
    return False

def capturar_pacotes(device_params):
    """Inicia a captura de pacotes entre dois IPs no dispositivo especificado."""
    ip_origem = input("Digite o IP de origem: ")
    if not validar_ip(ip_origem):
        print("IP de origem inválido.")
        return
    
    ip_destino = input("Digite o IP de destino: ")
    if not validar_ip(ip_destino):
        print("IP de destino inválido.")
        return

    # Comando para iniciar a captura
    comando_iniciar = f"capture teste interface nucleo real-time match ip host {ip_origem} host {ip_destino}"
    output = executar_comando(device_params, comando_iniciar)
    
    if output:
        print("\nCaptura de pacotes iniciada com sucesso.")
        print(output)
        print("\nPara parar a captura, pressione 'Ctrl + C' e o comando apropriado será enviado.")
        
        try:
            while True:
                pass  # Captura em execução até ser interrompida
        except KeyboardInterrupt:
            print("\nParando a captura...")
            # Comando para parar a captura
            comando_parar = f"no capture teste interface nucleo real-time match ip host {ip_origem} host {ip_destino}"
            output_parar = executar_comando(device_params, comando_parar)
            if output_parar:
                print("Captura encerrada com sucesso.")
            else:
                print("Erro ao encerrar a captura.")
    else:
        print("Erro ao iniciar captura de pacotes.")


def verificar_rotas(device_params):
    print("\n--- Análise de Rotas ---")
    escolha_rota = input("Digite 1 para rota padrão ou 2 para buscar uma rota específica por IP: ")
    if escolha_rota == "1":
        comando = "show route | include Gateway of last resort"
    elif escolha_rota == "2":
        ip_especifico = input("Digite o IP ou o prefixo que deseja buscar (ex: 192.168.18.): ")
        comando = f"show route | include {ip_especifico}"
    else:
        print("Escolha inválida.")
        return
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Rotas do dispositivo ---")
        print(output)
    else:
        print("Nenhuma rota encontrada ou erro ao obter rotas.")

def verificar_nat_asa(device_params):
    print("\n--- Verificação de NAT ---")
    Nat = input(" Digite IP ")
    comando = f"show nat t {Nat}"
    output = executar_comando(device_params, comando)
    if output:
        print(output)
    else:
        print("Erro ao verificar NAT.")

def verificar_object_group(device_params):
    print("\n--- Verificação de Object-Group ---")
    object_group = input("Digite nome object ")
    comando = f"show object id {object_group}"
    output = executar_comando(device_params, comando)
    if output:
        print(output)
    else:
        print("Erro ao verificar Object-Group.")

#nova funcoes dia 19/11
def verificar_status_link(device_params):
    """Verifica o status dos links com 'show track'."""
    comando = "show track"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Status dos Links ---")
        print(output)
    else:
        print("Erro ao verificar o status dos links.")

def verificar_sla_monitor(device_params):
    """Verifica o SLA monitor com 'show run sla monitor'."""
    comando = "show run sla monitor"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Configurações de SLA Monitor ---")
        print(output)
    else:
        print("Erro ao verificar o SLA monitor.")

def verificar_vpns_l2l_ativas(device_params):
    """Verifica VPNs L2L ativas com 'show vpn-sessiondb l2l'."""
    comando = "show vpn-sessiondb l2l"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- VPNs L2L Ativas ---")
        print(output)
    else:
        print("Erro ao verificar VPNs L2L ativas.")

def verificar_total_vpns_ativas(device_params):
    """Verifica o total de VPNs configuradas ativas com 'show vpn-sessiondb summary'."""
    comando = "show vpn-sessiondb summary"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Resumo de VPNs Configuradas Ativas ---")
        print(output)
    else:
        print("Erro ao verificar o total de VPNs configuradas ativas.")

# FORTNET        
    # Funções verificar VPN Fortinet
def verificar_vpn_fortinet(device_params):
    nome_vpn = input("Insira o nome da VPN: ")
    comando = f"""
                get vpn ipsec tunnel summary | grep -i {nome_vpn}
                get vpn ipsec tunnel name {nome_vpn}
            """
    output = executar_comando(device_params, comando)
    if output:
        print(f"\n--- Resultado do comando: {comando} ---")
        print(output)
    else:
        print("Erro ao verificar a VPN.")

    # Funções Verificar Nat Fortinet
def verificar_Nat_fortinet(device_params):
    nome_vpn = input("Insira o nome do Nat: ")
    comando = f"show firewall ippool | grep -f {nome_vpn}"
    output = executar_comando(device_params, comando)
    if output:
        print(f"\n--- Resultado do comando: {comando} ---")
        print(output)
    else:
        print("Erro ao verificar a VPN.")

def capturar_pacotes_fortinet(device_params):
    source = input("Digite o IP de origem para captura: ")
    comando = f"diagnose sniffer packet any 'host {source}' 4 0 l"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Captura de pacotes iniciada no Fortinet ---")
        print(output)
        print("Para parar a captura, use 'Ctrl + C' no terminal e interrompa o processo.")
    else:
        print("Erro ao iniciar captura de pacotes no Fortinet.")

#novo
def Analise_rota_fortinet(device_params):
    IP = input(" Digite o IP para analise de rota: ")
    comando = f"""
                show  router static | grep -fi {IP}
                get router info routing-table details {IP}

             """
    output = executar_comando(device_params, comando)
    if output:
        print(" \n === Resulatdo da anlise de rota === ")
        print(output)
    else:
        print(" Erro para executar comando ")


# Fução de Verificação Paulo Alto
    #teste de regra 
def verificar_Regra_Paulo(device_params):
    source = input("Digite o IP de origem para teste: ")
    destino = input("Digite o IP destino para teste: ")
    port = input("Digite a porta destino para teste: ")
    comando = f"test security-policy-match source {source} destination {destino} destination_port {port} protocol 6"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Teste de regra ---")
        print(output)
    else:
        print("Erro ao executar comando.")

def verificar_Rota_Paulo(device_params):
    IP = input("Digite o IP: ")
    comando = f"show routing route virtual-router VR-DEFAULT | match {IP}"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Teste de rota ---")
        print(output)
    else:
        print("Erro ao executar comando.")

def verificar_nat_palo(device_params):
    Nat = input("Digite o IP para verificação de NAT: ")
    comando = f"show nat policy rule {Nat}"
    output = executar_comando(device_params, comando)
    if output:
        print("\n--- Detalhes de NAT ---")
        print(output)
    else:
        print("Erro ao verificar NAT.")

# Fução de configuração 


def save_to_file_json(data, folder="C://documento"):
    """Salva os dados coletados em um arquivo JSON com versionamento e cria um backup se necessário."""
    # Garante que a pasta exista
    os.makedirs(folder, exist_ok=True)

    # Cria um nome de arquivo único com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"dados_gsti_{timestamp}.json")

    # Verifica se já existe algum arquivo `dados_gsti` na pasta
    existing_files = [f for f in os.listdir(folder) if f.startswith("dados_gsti") and f.endswith(".json")]
    if existing_files:
        for file in existing_files:
            original_path = os.path.join(folder, file)
            backup_path = os.path.join(folder, f"backup_de_conf_{file}")
            os.rename(original_path, backup_path)
            print(f"Backup criado: {backup_path}")

    # Salva os dados no formato JSON
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"Dados salvos no arquivo JSON: {filename}")



def obter_mascara(ip):
    """Retorna a máscara de rede para um IP ou Net informado."""
    try:
        # Tenta criar um objeto de rede a partir do IP
        rede = ipaddress.ip_network(ip, strict=False)
        return str(rede.netmask)
    except ValueError:
        # Caso o IP não esteja em formato CIDR, solicita a máscara manualmente
        print(f"IP '{ip}' inválido ou sem máscara. Informe a máscara manualmente.")
        mask = input("Máscara de rede (ex: /16): ")
        return mask

def criar_regra_firewall_asa_json(device_params):
    try:
        # Coleta de informações
        print("Preencha as informações abaixo:")
        numero_gsti = input("Número GSTI: ")
        conta = input("Conta: ")
        ip_origem = input("IP ou Net de origem (ex: 192.168.1.0/16): ")
        mask_origem = obter_mascara(ip_origem)
        ip_destino = input("IP ou Net de destino (ex: 10.0.0.0/16): ")
        mask_destino = obter_mascara(ip_destino)
        porta = input("Porta: ")

        # Dados em formato de dicionário
        dados = {
            "Número GSTI": numero_gsti,
            "Conta": conta,
            "Origem": {
                "IP": ip_origem.split('/')[0],
                "Máscara": mask_origem
            },
            "Destino": {
                "IP": ip_destino.split('/')[0],
                "Máscara": mask_destino
            },
            "Porta": porta,
            "Data/Hora": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Salva os dados no arquivo JSON, criando backups se necessário
        save_to_file_json(dados, folder=r"C:\Users\jhonatas.rodrigues\Desktop\erros")

        # Gera configuração em formato texto para enviar ao dispositivo
        configuracao = f"""
            object-group network src_{conta}
            network-object {ip_origem.split('/')[0]} {mask_origem}
            object-group network dst_{numero_gsti}
            network-object {ip_destino.split('/')[0]} {mask_destino}
            object-group service {numero_gsti} tcp
            port-object eq {porta}
            access-list global_in extended permit tcp object-group network srv_{conta} object-group network dst_{numero_gsti} object-group service {numero_gsti} log notifications
        """
        
        connect = ConnectHandler(**device_params)  # Passa os parâmetros do dispositivo
        output = connect.send_config_set(configuracao.splitlines())  # Envia as configurações
        print("Configuração aplicada com sucesso.")
        print(output)

    except Exception as e:
        print(f"Erro inesperado: {e}")
        
def aplicar_regra_firewall(device, caminho_arquivo):
    """Aplica a regra de firewall ao dispositivo.

    Args:
        device: Parâmetros de conexão do dispositivo.
        caminho_arquivo: Caminho do arquivo com a regra.
    """

    try:
        with open(caminho_arquivo, r"C:\Users\jhonatas.rodrigues\Desktop\erros\script.json") as file:
            config = file.read()

        connect = ConnectHandler(**device)
        output = connect.send_config_set(config.splitlines())
        print(output)

    except FileNotFoundError:
        print("Arquivo não encontrado.")
    except Exception as e:
        print(f"Erro ao aplicar a regra: {str(e)}")
    
    

def conectar_cisco():
    print("\n=== Conexão com Cisco ===")
    # incirido 
    print("FIREWALL")
    print("IBM_HOR_DC_FW_INT_01 10.109.3.228,       IBM_HOR_DC_FW_INT_02 10.109.3.244") 
    print("IBM_HOR_DC_FW_FL_01 10.109.3.226,        IBM_HOR_DC_FW_VPN_P_01 10.109.3.247")
    print("IBM_HOR_DC_FW_OOB_01 10.109.3.50,        IBM_HOR_DC_FW_OOB_02 10.109.3.51")
    print("IBM_HOR_DC_FW_VPN_P_02 10.109.3.224,     IBM_HOR_DC_FW_TRS-01 10.109.3.248,") 
    print("IBM_HOR_DC_FW_EXTRA-NET-01 10.109.3.251, IBM_HOR_DC_FW_VPN_NP 10.109.3.225") 

    ip_dispositivo = input("Digite o IP do dispositivo Cisco: ")
    user = input("Digite o usuário: ")
    password = getpass("Digite a senha: ")
    
    device = {
        'device_type': 'cisco_asa',
        'host': ip_dispositivo,
        'username': user,
        'password': password,
        'secret': password,
        'port': 22  # Altere se necessário
    }
    
    # Teste de conexão
    if executar_comando(device, "show version"):
        print("Conexão com Cisco estabelecida com sucesso.")
        return device
    else:
        print("Falha na conexão com Cisco. Verifique as credenciais e tente novamente.")
        return None

def conectar_fortinet():
    print("\n=== Conexão com Fortinet ===")
    print("FW-PRACEIROS-CONT-ACESSO-ORG-VELHA 10.73.2.12")
    print(" Login@picpay.com ")
    ip_dispositivo = input("Digite o IP do dispositivo Fortinet: ")
    user = input("Digite o usuário: ")
    password = getpass("Digite a senha: ")
    
    device = {
        'device_type': 'fortinet',
        'host': ip_dispositivo,
        'username': user,
        'password': password,
        'secret': password,
        'port': 22  # Altere se necessário
    }
    
    # Teste de conexão
    if executar_comando(device, "get system status"):
        print("Conexão com Fortinet estabelecida com sucesso.")
        return device
    else:
        print("Falha na conexão com Fortinet. Verifique as credenciais e tente novamente.")
        return None

# Função de conexão para Palo Alto
def conectar_Paloalto():
    print("\n=== Conexão com Palo Alto ===")
    ip_dispositivo = input("Digite o IP do dispositivo Palo Alto: ")
    user = input("Digite o usuário: ")
    password = getpass("Digite a senha: ")
    
    device = {
        'device_type': 'paloalto_panos',
        'host': ip_dispositivo,
        'username': user,
        'password': password,
    #    'secret': password,
        'port': 22  # Altere se necessário
    }
      # Teste de conexão
    if executar_comando(device, "show system info"):
        print("Conexão com Palo Alto estabelecida com sucesso.")
        return device
    else:
        print("Falha na conexão com Palo Alto. Verifique as credenciais e tente novamente.")
        return None


# Funções para Gerenciar Cisco
def handle_cisco(device_params):
    while True:
        escolha_firewall = menu_firewall()
        
        if escolha_firewall == "1":  # Menu de Verificação
            while True:
                escolha_verificacao = menu_verificacao_firewall()

                if escolha_verificacao == "1":
                    verificar_interface(device_params)
                elif escolha_verificacao == "2":
                    verificar_regra_firewall(device_params)
                elif escolha_verificacao == "3":
                    testar_regra_packet_tracer(device_params)
                elif escolha_verificacao == "4":
                    capturar_pacotes(device_params)
                elif escolha_verificacao == "5":
                    verificar_rotas(device_params)
                elif escolha_verificacao == "6":
                    verificar_nat_asa(device_params)
                elif escolha_verificacao == "7":
                    verificar_object_group(device_params)
                elif escolha_verificacao == "8":
                    verificar_vpn(device_params)
                elif escolha_verificacao == "9":
                    verificar_configuracao(device_params)
                elif escolha_verificacao == "10":  # Voltar ao menu principal
                    break
                elif escolha_verificacao == "11":
                    verificar_status_link(device_params)
                elif escolha_verificacao == "12":
                    verificar_sla_monitor(device_params)
                elif escolha_verificacao == "13":
                    verificar_vpns_l2l_ativas(device_params)
                elif escolha_verificacao == "14":
                    verificar_total_vpns_ativas(device_params)
                else:
                    print("Opção inválida. Tente novamente.")
            pass  # Substitua por chamadas reais às funções.

        elif escolha_firewall == "2":  # Configuração (Exemplo: criar regra ASA)
            while True:
                escolha_config = menu_configuracao_asa()
                if escolha_config == "1":
                    criar_regra_firewall_asa_json(device_params)
                elif escolha_config == "2":
                    break
            pass  # Substitua por chamadas reais às funções.

        elif escolha_firewall == "3":  # Voltar ao menu principal
            break

        else:
            print("Opção inválida. Tente novamente.")

# Funções para Gerenciar Fortinet
def handle_fortinet(device_params):
    while True:
        escolha_fortinet = menu_fortinet()
        
        if escolha_fortinet == "1":
            verificar_vpn_fortinet(device_params)
        elif escolha_fortinet == "2":
            verificar_Nat_fortinet(device_params)
        elif escolha_fortinet == "3":
            capturar_pacotes_fortinet(device_params)
        elif escolha_fortinet == "4":
            Analise_rota_fortinet(device_params) 
        elif escolha_fortinet == "5":
            break
        else:
            print("Opção inválida.")

# Funções para Gerenciar Palo Alto
def handle_Paloalto(device_params):
    while True:
        escolha_Pauloalto = menu_Paloalto()
        
        if escolha_Pauloalto == "1":
            verificar_nat_palo(device_params)
        elif escolha_Pauloalto == "2":
            verificar_Rota_Paulo(device_params)
        elif escolha_Pauloalto == "3":
            verificar_Regra_Paulo(device_params)
        elif escolha_Pauloalto == "4":
            break
        else:
            print("Opção inválida.")

# Função principal para controle dos menus
def main():
    print(f"\n=== Aplicação de Verificação de Rede - Versão {VERSION} ===")

    while True:
        escolha = menu_principal()

        if escolha == "1":
            device_cisco = conectar_cisco()  # Certifique-se de que essa função está definida.
            if device_cisco:
                handle_cisco(device_cisco)

        elif escolha == "2":
            device_fortinet = conectar_fortinet()  # Certifique-se de que essa função está definida.
            if device_fortinet:
                handle_fortinet(device_fortinet)  # Certifique-se de que essa função está definida.

        elif escolha == "3":
            device_paloalto = conectar_Paloalto()  # Certifique-se de que essa função está definida.
            if device_paloalto:
                handle_Paloalto(device_paloalto)  # Certifique-se de que essa função está definida.

        elif escolha == "7":
            print("Encerrando o programa. Até mais!")
            break

        else:
            print("Opção inválida.")

# Função para criar regra de firewall


if __name__ == "__main__":
    main()