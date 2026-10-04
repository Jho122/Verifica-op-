import netmiko
# import logging
from getpass import getpass
from datetime import datetime

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

def execução_segura(device_params, comando):
    """
    Executa comandos no dispositivo e captura erros detalhados.
    """
    try:
        print(f"Conectando ao dispositivo {device_params['host']}...")
        net_connect = netmiko.ConnectHandler(**device_params)
       # net_connect.confgure_terminal()
        output = net_connect.send_command_set(comando)
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
    #try:
    #    print(f"Executando comando: {comando}")
    #    output = executar_comando(device_params, comando)
    #    if output is None or output.strip() == "":
    #        print(f"Comando '{comando}' executado, mas não retornou saída.")
    #    else:
    #        print(f"Resposta do dispositivo: {output}")
    #    return output
    #except Exception as e:
    #    print(f"Erro ao executar o comando '{comando}': {e}")
    #    return None


# Menus alterção 
def menu_principal():
    print("\n=== Menu Principal ===")
    print("1 - Firewall") 
    print("2 - Fortinet")
    print("3 - Palo alto em Desenvolvimento")
    print("4 - Router em Desenvolvimento")
    print("5 - Switch em Desenvolvimento")
    print("6 - APIC em Desenvolvimento")
    print("7 - Sair")
    return input("Escolha uma opção: ")

# Menu de Verificação
# Menu Cisco ASA
def menu_firewall():
    print("\n=== Menu Firewall ===")
    print("1 - Verificação")
    print("2 - Configuração")
    print("3 - Voltar")
    return input("Escolha uma opção: ")

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
def menu_Pauloalto():
    print("\n=== Menu Palo Alto ===")
    print("1 - Verificação de NAT")
    print("2 - Verificação de Rota")
    print("3 - Teste de Regra")
    print("4 - Voltar")
    return input("Escolha uma opção: ")

# Menu de Configuração 
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

def capturar_pacotes(device_params):
    ip_origem = input("Digite o IP de origem: ")
    ip_destino = input("Digite o IP de destino: ")
    comando = f"capture teste interface nucleo real-time match ip host {ip_origem} host {ip_destino}"
    output = executar_comando(device_params, comando)
    if output:
        print("\nCaptura de pacotes iniciada.")
        print(output)
        print("Para parar a captura, use 'Ctrl + C' e execute o comando para parar a captura.")
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
    comando = f"get vpn ipsec tunnel summary | grep -i {nome_vpn}"
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
    destination = input("Digite o IP de destino para captura: ")
    comando = f"diagnose sniffer packet any 'host {source} and host {destination}' 4 0 l"
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
    comando = f"show  router static | grep -fi {IP}"
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


def criação_Regra_asa(device_params):
    """
    Função para criar regras no Cisco ASA. Configura grupos de origem, destino e portas, e adiciona a regra ACL.
    """
    try:
        # Garantir que estamos no modo privilegiado
        print("Garantindo modo privilegiado...")
        if not execução_segura(device_params, "enable"):
            print("Erro: Não foi possível entrar no modo privilegiado. Verifique as credenciais ou permissões.")
            return

        # Entrar no modo de configuração
        print("Entrando no modo de configuração...")
        config_output = execução_segura(device_params, "configure terminal")
        if config_output is None or "Invalid input" in config_output:
            print("Erro: Não foi possível entrar no modo de configuração.")
            return
        
        # Entrar no modo de configuração
        print("Entrando no modo de configuração...")
        execução_segura(device_params, "configure terminal")
        print("Modo de configuração habilitado (ignorar ausência de retorno).")

        print("\n=== Configuração de Regra - Nome da Regra será Conta + GSTI ===")

        # Solicitar nomes dos grupos
        nome_obj_src_asa = input("Nome do grupo de origem (ex: Conta + GSTI): ").strip()
        nome_obj_dst_asa = input("Nome do grupo de destino (ex: Projeto ou GSTI): ").strip()
        nome_obj_port_asa = input("Nome do grupo de portas: ").strip()

        # Configurar grupo de origem
        print("\n--- Configurando grupo de origem ---")
        execução_segura(device_params, f"object-group network {nome_obj_src_asa}")
        while True:
            ip = input("Digite um IP ou rede para a origem (ex: 192.168.1.0/24 ou 192.168.1.10). Digite 'fim' para finalizar: ").strip()
            if ip.lower() == "fim":
                break
            if "/" in ip:  # Rede CIDR
                network, mask = ip.split("/")
                execução_segura(device_params, f"network-object {network} {mask}")
            else:  # Host individual
                execução_segura(device_params, f"network-object host {ip}")

        # Configurar grupo de destino
        print("\n--- Configurando grupo de destino ---")
        execução_segura(device_params, f"object-group network {nome_obj_dst_asa}")
        while True:
            ip = input("Digite um IP ou rede para o destino (ex: 192.168.1.0/24 ou 192.168.1.10). Digite 'fim' para finalizar: ").strip()
            if ip.lower() == "fim":
                break
            if "/" in ip:  # Rede CIDR
                network, mask = ip.split("/")
                execução_segura(device_params, f"network-object {network} {mask}")
            else:  # Host individual
                execução_segura(device_params, f"network-object host {ip}")

        # Configurar grupo de portas
        print("\n--- Configurando grupo de portas ---")
        execução_segura(device_params, f"object-group service {nome_obj_port_asa} tcp")
        while True:
            porta = input("Digite uma porta para o grupo de portas (ex: 80, 443). Digite 'fim' para finalizar: ").strip()
            if porta.lower() == "fim":
                break
            execução_segura(device_params, f"port-object eq {porta}")

        # Criar a regra de acesso
        print("\n--- Criando a regra ACL ---")
        comando_acl = (
            f"access-list global_in extended permit tcp "
            f"object-group {nome_obj_src_asa} "
            f"object-group {nome_obj_dst_asa} "
            f"object-group {nome_obj_port_asa} log notifications"
        )
        output = execução_segura(device_params, comando_acl)

        # Exibir resultado
        if output:
            print("\n=== A Regra Foi Configurada com Sucesso ===")
            print(output)
        else:
            print("Erro ao configurar a regra. Verifique as entradas e tente novamente.")

    except Exception as e:
        print(f"Erro inesperado durante a criação da regra: {e}")

#    print("1. Criar regra de acesso ASA")
#    print("2. Sair")
#    opcao = input("Escolha uma opção: ")
#    return opcao

# Funções de Conexão
def conectar_cisco():
    print("\n=== Conexão com Cisco ===")
    # incirido 
    print("FIREWALL")
    print("IBM_HOR_DC_FW_INT_,       IBM_HOR_DC_FW_INT_02 ") 
    print("IBM_HOR_DC_FW_FL_01 ,        IBM_HOR_DC_FW_VPN_P_01 ")
    print("IBM_HOR_DC_FW_OOB_01 ,        IBM_HOR_DC_FW_OOB_02 ")
    print("IBM_HOR_DC_FW_VPN_P_02 ,     IBM_HOR_DC_FW_TRS-01 ,") 
    print("IBM_HOR_DC_FW_EXTRA-NET-01 , IBM_HOR_DC_FW_VPN_NP ") 

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
def conectar_Pauloalto():
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
        
        elif escolha_firewall == "2":  # Configuração (Exemplo: criar regra ASA)
           while True:
                escolha_config = menu_configuracao_asa()
                if escolha_config == "1":
                    criação_Regra_asa(device_params)
                elif escolha_config == "2":
                    break
        elif escolha == "3":
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
def handle_Pauloalto(device_params):
    while True:
        escolha_Pauloalto = menu_Pauloalto()
        
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
            # Suponha que você já tenha implementado `conectar_cisco` e `handle_cisco`
            device_cisco = conectar_cisco()
            if device_cisco:
                handle_cisco(device_cisco)
                
        elif escolha == "2":
            # Suponha que você já tenha implementado `conectar_fortinet` e `handle_fortinet`
            device_fortinet = conectar_fortinet()
            if device_fortinet:
                handle_fortinet(device_fortinet)

        elif escolha == "3":
            device_Pauloalto = conectar_Pauloalto()
            if device_Pauloalto:
                handle_Pauloalto(device_Pauloalto)

        elif escolha == "6":
            device_APIC = conectar_cisco()
            if device_APIC:
                handle_APIC(device_APIC)

        elif escolha == "7":
            print("Encerrando o programa. Até mais!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()

