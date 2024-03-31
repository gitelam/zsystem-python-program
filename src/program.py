import time
import os
import socket
import platform
import psutil
import platform,socket,re,uuid,json,psutil,logging
import json
import platform
import cpuinfo
import psutil
import socket
import datetime
import uuid
import re



def obtener_mac_conexion_internet():
    conexiones_activas = psutil.net_connections(kind='inet')
    interfaces_activas = psutil.net_if_addrs()
    
    for conexion in conexiones_activas:
        # Filtrar conexiones que están establecidas y no son locales
        if conexion.status == 'ESTABLISHED' and not conexion.laddr.ip.startswith('127.'):
            for interface, addrs in interfaces_activas.items():
                # Verificar si la dirección IP de la conexión pertenece a una interfaz activa
                for addr in addrs:
                    if addr.family == socket.AF_INET and addr.address == conexion.laddr.ip:
                        # Si coincide, obtener la dirección MAC de la interfaz
                        mac_address = psutil.net_if_addrs()[interface][0].address
                        #obtener direccion ip de la interfaz
                        ip_address = psutil.net_if_addrs()[interface][1].address
                        return mac_address, interface, ip_address


mac_internet = obtener_mac_conexion_internet()

# info={}
# def getSystemInfo():
#     try:
#         info['platform']=platform.system()
#         info['platform-release']=platform.release()
#         info['platform-version']=platform.version()
#         info['architecture']=platform.machine()
#         info['hostname']=socket.gethostname()
#         info['ip-address']=socket.gethostbyname(socket.gethostname())
#         info['mac-address']=mac_internet[0]
#         info['conection-interface']=mac_internet[1]
#         info['processor']=platform.processor()
#         info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
#         return json.dumps(info)
#     except Exception as e:
#         logging.exception(e)

#funcion que retorna la ultima cantidad de datos enviados y recibidos 
def get_network():
    net1_out = psutil.net_io_counters().bytes_sent
    net1_in = psutil.net_io_counters().bytes_recv
    time.sleep(1)
    net2_out = psutil.net_io_counters().bytes_sent
    net2_in = psutil.net_io_counters().bytes_recv
    sent = net2_out - net1_out
    recv = net2_in - net1_in
    # convertir a Kbps
    sent = sent/1024
    recv = recv/1024
    return sent, recv


#funcion que retorna los paquetes enviados y recibidos por el sistema
def get_network_packets():
    net1_out = psutil.net_io_counters().packets_sent
    net1_in = psutil.net_io_counters().packets_recv
    time.sleep(1)
    net2_out = psutil.net_io_counters().packets_sent
    net2_in = psutil.net_io_counters().packets_recv
    sent = net2_out - net1_out
    recv = net2_in - net1_in
    return sent, recv

#funcion que retorna la cantidad de errores en la red
def get_network_errors():
    net1_out = psutil.net_io_counters().errout
    net1_in = psutil.net_io_counters().errin
    time.sleep(1)
    net2_out = psutil.net_io_counters().errout
    net2_in = psutil.net_io_counters().errin
    sent = net2_out - net1_out
    recv = net2_in - net1_in
    return sent, recv

#funcion que retorna la cantidad de paquetes descartados   
def get_network_drop():
    net1_out = psutil.net_io_counters().dropin
    net1_in = psutil.net_io_counters().dropout
    time.sleep(1)
    net2_out = psutil.net_io_counters().dropin
    net2_in = psutil.net_io_counters().dropout
    sent = net2_out - net1_out
    recv = net2_in - net1_in
    return sent, recv

#calcular total de bytes recibidos y enviados
def get_bandwidth():
    net1_out = psutil.net_io_counters().bytes_sent
    net1_in = psutil.net_io_counters().bytes_recv
    time.sleep(1)
    net2_out = psutil.net_io_counters().bytes_sent
    net2_in = psutil.net_io_counters().bytes_recv
    sent = net2_out - net1_out
    recv = net2_in - net1_in
    return sent, recv




def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}"
        bytes /= factor

def System_information():
    system_info = {}
    
    # System Information
    uname = platform.uname()
    system_info["System"] = uname.system + " " + uname.release + " " + uname.version
    system_info["Node Name"] = uname.node
    system_info["Machine"] = uname.machine
    system_info["Processor (CPU)"] = cpuinfo.get_cpu_info()["brand_raw"]
    system_info['mac-address']=mac_internet[0]
    system_info['conection-interface']=mac_internet[1]
    system_info['ip-address']=mac_internet[2]

    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
    system_info["Boot Time"] = f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"

    # Network Information
    network_info = {}
    network_info["Bytes Sent"], network_info["Bytes Received"] = get_network()
    system_info["Network Information"] = network_info


    # Network Packets
    network_packets = {}
    network_packets["Packets Sent"], network_packets["Packets Received"] = get_network_packets()
    system_info["Network Packets"] = network_packets

    # Network Errors
    network_errors = {}
    network_errors["Errors Sending"], network_errors["Errors Receiving"] = get_network_errors()
    system_info["Network Errors"] = network_errors

    # Network Drop
    network_drop = {}
    network_drop["Packets Drop Sending"], network_drop["Packets Drop Receiving"] = get_network_drop()
    system_info["Network Drop"] = network_drop

    # Bandwidth
    bandwidth = {}
    bandwidth["Bandwidth Sent"], bandwidth["Bandwidth Received"] = get_bandwidth()
    system_info["BPS Bandwidth"] = bandwidth



    # CPU Information
    cpu_info = {}
    cpu_percent = psutil.cpu_percent()
    cpu_info["Physical cores"] = psutil.cpu_count(logical=False)
    cpu_info["Total cores"] = psutil.cpu_count(logical=True)
    # cpu_info["CPU Usage Per Core"] = {f"Core {i}": f"{percentage}%" for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1))}
    cpu_info["Total CPU Usage"] = f"{cpu_percent}"
    system_info["MHz CPU Info"] = cpu_info

    # Memory Information
    mem_info = {}
    svmem = psutil.virtual_memory()
    mem_info["Total"] = get_size(svmem.total)
    mem_info["Available"] = get_size(svmem.available)
    mem_info["Used"] = get_size(svmem.used)
    mem_info["Percentage"] = f"{svmem.percent}"
    system_info["GB Memory Information"] = mem_info

    # Guardar en archivo JSON
    with open('system_info.json', 'w') as f:
        json.dump(system_info, f, indent=4)

if __name__ == "__main__":
    while True:
        get_network()
        System_information()
        time.sleep(0.2)
        os.system('cls')