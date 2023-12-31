import math
import psutil
import time
import platform
import mysql.connector
import ping3
import socket


def converter_segundos_para_horas_minutos_segundos(segundos):
    horas = segundos // 3600  # 1 hora = 3600 segundos
    segundos_restantes = segundos % 3600
    minutos = segundos_restantes // 60
    segundos_final = math.ceil(segundos_restantes % 60)

    return horas, minutos, segundos_final

def bytes_para_gb(bytes_value):
    return bytes_value / (1024 ** 3)

mydb = mysql.connector.connect(host = 'localhost',user = 'root',passwd = '5505',database = 'SecureATM')
cursor = mydb.cursor()
id_atm = 1
id_empresa = 1

print("\n-----------------------------------------")
componente = input("Qual componente você deseja monitorar? (CPU, Disco, Memória, Rede, Sensor)")

if(componente == "CPU"):
    print("\n-----------------------------------------")
    print("\nComponente selecionado = CPU\n")
    print("-----------------------------------------")

    while(True):
        
        print("\nSituação geral: ")
        print("-----------------------------------------")
        
        ps = psutil.cpu_times()
        
        TempoUsuarioHoras, TempoUsuarioMinutos, TempoUsuarioSegundos = converter_segundos_para_horas_minutos_segundos(ps[0])
        TempoSistemaHoras, TempoSistemaMinutos, TempoSistemaSegundos = converter_segundos_para_horas_minutos_segundos(ps[1])
        tempo_usuario = "{:.2f}".format(ps[0])
        tempo_sistema = ps[1] 
        porcentagem_utilizacao = psutil.cpu_percent(percpu = False)
        numeroCpu = psutil.cpu_count()
        frequenciaCpuMhz = psutil.cpu_freq(percpu=False)
        velocidade = "{:.2f}".format(frequenciaCpuMhz.current / 1000)
        processos = len(psutil.pids())

        print("Número de processos", processos)
        print("Tempo:")
        print("Tempo de usuário:", TempoUsuarioHoras, "h", TempoUsuarioMinutos, 'm e',TempoUsuarioSegundos, 's')  
        print("Tempo de sistema:", TempoSistemaHoras, "h", TempoSistemaMinutos, 'm e',TempoSistemaSegundos, 's')      
        

        print("\nUtilização:")
        print("Porcentagem sendo utilizada da CPU: ", porcentagem_utilizacao, "%")
        print()

        print("Outros:")
        print("\nNúmero de CPUs lógicas no sistema:", numeroCpu)
        print("\nFrequencia das CPUs no sistema:", velocidade, "GHz")
        print()
        aberto = True

        query = 'INSERT INTO cpu(aberto, porcentagem_utilizacao, velocidade, processos, tempo_usuario, tempo_sistema, fk_atm, fk_empresa ) VALUES(%s, %s,%s, %s, %s, %s, %s, %s)'
        param = [aberto, porcentagem_utilizacao, velocidade, processos, tempo_usuario, tempo_sistema, id_atm, id_empresa]
        cursor.execute(query, param)
        mydb.commit()
        time.sleep(20)
    
elif(componente == "Disco"):
    print("\n-----------------------------------------")
    print("\nComponente selecionado = Disco\n")
    print("-----------------------------------------")

    while(True):
        print("\nSituação geral: ")
        print("-----------------------------------------")
        particoes = psutil.disk_partitions()

        print("Partições de Disco:")
        for particao in particoes:
            print("Ponto de Montagem:", particao.mountpoint)
            print("Sistema de Arquivos:", particao.fstype)
            print("Dispositivo:", particao.device)
        print()
        
        meu_so = platform.system()
        if(meu_so == "Linux"):
            nome_disco = '/'
            disco = psutil.disk_usage(nome_disco)
        elif(meu_so == "Windows"):
            nome_disco = 'C:\\'
            disco = psutil.disk_usage(nome_disco) 

        porcentagem_uso = disco.percent
        capacidade_total = "{:.2f}".format(bytes_para_gb(disco.total))
        capacidade_usada = "{:.2f}".format(bytes_para_gb(disco.used))
        capacidade_livre = "{:.2f}".format(bytes_para_gb(disco.free))

        print("Uso de Disco:")
        print(f"Nome do Disco:", nome_disco)
        print(f"Total:", capacidade_total, "bytes")
        print(f"Usado:", capacidade_usada, "bytes")
        print(f"Livre:", capacidade_livre, "bytes")
        print(f"Percentual de Uso:", porcentagem_uso, "%")
        print()

        io_disco = psutil.disk_io_counters(perdisk=True)
        print("E/S de Disco:")
        for disco, io in io_disco.items():
            leituras = io.read_count
            escritas = io.write_count
            print(f"Disco:", disco)
            print(f"Leituras:", io.read_count)
            print(f"Escritas:", io.write_count)
            print()

        aberto = True

        query = 'INSERT INTO disco(aberto, nome_disco, porcentagem_uso, capacidade_total, capacidade_usada, capacidade_livre, leituras, escritas, fk_atm, fk_empresa) VALUES(%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)'
        param = [aberto, nome_disco,porcentagem_uso, capacidade_total, capacidade_usada, capacidade_livre, leituras, escritas, id_atm, id_empresa]
        cursor.execute(query, param)
        mydb.commit()
        time.sleep(20)

elif(componente == "Memória"):
    print("\n-----------------------------------------")
    print("\nComponente selecionado = Memória\n")
    print("-----------------------------------------")

    while(True):
        memoria_virtual = psutil.virtual_memory()
        total = "{:.2f}".format(bytes_para_gb(memoria_virtual.total))
        livre = "{:.2f}".format(bytes_para_gb(memoria_virtual.available))
        usado = "{:.2f}".format(bytes_para_gb(memoria_virtual.used))
        porcentagem_uso = memoria_virtual.percent
        print("Memória Virtual:")
        print("Total:", total,"GB")
        print("Disponível:", livre,"GB")
        print("Usado:", usado,"GB")
        print("Percentual de Uso:", porcentagem_uso,"%")
        print()

        swap = psutil.swap_memory()
        print("Swap:")
        print("Total: {:.2f} GB".format(bytes_para_gb(swap.total)))
        print("Usado: {:.2f} GB".format(bytes_para_gb(swap.used)))
        print("Livre: {:.2f} GB".format(bytes_para_gb(swap.free)))
        print("Percentual de Uso:", swap.percent,"%")
        print()
        
        aberto = True

        query = 'INSERT INTO memoria(aberto, total, usado, livre, porcentagem_uso, fk_atm, fk_empresa) VALUES(%s, %s,%s, %s, %s, %s, %s)'
        param = [aberto, total, usado, livre, porcentagem_uso, id_atm, id_empresa]
        cursor.execute(query, param)
        mydb.commit()
        
        time.sleep(20)
   
elif(componente == "Rede"):
    print("\n-----------------------------------------")
    print("\nComponente selecionado = Rede\n")
    print("-----------------------------------------")
    while(True):
        print("\nSituação geral: ")
        print("-----------------------------------------")

        # Coletar informações de rede com psutil
        network_info = psutil.net_if_addrs()

        # Iterar pelas interfaces de rede
        for interface, addresses in network_info.items():
            for address in addresses:
                if address.family == socket.AF_INET:
                    #endereco_ip = address.address
                    nome_host = address.broadcast or ""
                    tipo_conexao = interface
                    velocidade_conexao = psutil.net_if_stats()[interface].speed
                    #uso_banda = psutil.net_io_counters(pernic=True)[interface].bytes_sent / 1024 / 1024  # MB
                    #latencia_ms = ping3.ping(endereco_ip) 
                    status = "Ativo"  # obs: lógica para verificar o status da conexão aqui
        io_rede = psutil.net_io_counters()
        bytes_enviados = io_rede.bytes_sent
        bytes_recebidos = io_rede.bytes_recv
        print("Tráfego de Rede Total:")
        #print("Nome host:", nome_host)
        #print("Endereço IP:", endereco_ip)
        print("Tipo conexão:", tipo_conexao)
        print("Velocidade conexão:", velocidade_conexao)
        #print("Latencia(ms):", latencia_ms)
        print("Bytes Recebidos:", io_rede.bytes_recv)
        print("Bytes Enviados:", io_rede.bytes_sent)

        aberto = True
        
        query = 'INSERT INTO rede(aberto, tipo_conexao, velocidade_conexao, bytes_enviados, bytes_recebidos, fk_atm, fk_empresa) VALUES(%s, %s, %s, %s, %s, %s, %s)'
        param = [aberto, tipo_conexao, velocidade_conexao, bytes_enviados, bytes_recebidos,  id_atm, id_empresa]
        cursor.execute(query, param)
        mydb.commit()
        
        time.sleep(20)

elif(componente == "Sensor"):
    print("\n-----------------------------------------")
    print("\nComponente selecionado = Sensor\n")
    print("-----------------------------------------")
    while(True):
        print("\nSituação geral: ")
        print("-----------------------------------------")
        
        
        dadosBateria = psutil.sensors_battery()
        TempoRestanteHoras, TempoRestanteMinutos, TempoRestanteSegundos = converter_segundos_para_horas_minutos_segundos(dadosBateria.secsleft)
        bateriaEstado = 'Desligado'
        if dadosBateria.power_plugged == True:
            bateriaEstado = 'Ligado'
        print("Bateria:")
        print("Porcentagem:", dadosBateria.percent, "%")
        print("Tempo restante:", TempoRestanteHoras, "h", TempoRestanteMinutos, 'm e',TempoRestanteSegundos, 's')  
        print("Carregamento:", bateriaEstado)
        print()
        
        time.sleep(20)


