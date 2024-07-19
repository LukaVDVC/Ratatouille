import platform
import psutil
import tabulate
from datetime import datetime

class SystemInfo:
    def __init__(self):
        # Collecte des informations système lors de l'initialisation
        self.sysinfo = self.get_sys_info()
        self.boot_time = self.get_boot_time()
        self.cpu_info = self.get_cpu_info()
        self.mem_usage = self.get_mem_usage()
        self.disk_info = self.get_disk_info()
        self.net_info = self.get_net_info()

    def get_size(self, bolter, suffix="B"):
        # Convertit une taille en octets en une taille lisible (Ko, Mo, Go, etc.)
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bolter < factor:
                return f"{bolter:.2f}{unit}{suffix}"
            bolter /= factor

    def get_sys_info(self):
        # Récupère les informations de la plateforme (système d'exploitation, version, etc.)
        headers = ("Étiquette de la Plateforme", "Information")
        values = []
        uname = platform.uname()
        values.append(("Système", uname.system))
        values.append(("Nom du Nœud", uname.node))
        values.append(("Release", uname.release))
        values.append(("Version", uname.version))
        values.append(("Machine", uname.machine))
        values.append(("Processeur", uname.processor))
        return tabulate.tabulate(values, headers=headers)

    def get_boot_time(self):
        # Récupère le temps de démarrage du système
        headers = ("Étiquette de Démarrage", "Information")
        values = []
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        values.append(("Temps de Démarrage", f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"))
        return tabulate.tabulate(values, headers=headers)

    def get_cpu_info(self):
        # Récupère les informations sur le processeur (nombre de cœurs, fréquence, utilisation, etc.)
        headers = ("Étiquette CPU", "Valeur")
        values = []
        cpufreq = psutil.cpu_freq()
        values.append(("Cœurs Physiques", psutil.cpu_count(logical=False)))
        values.append(("Cœurs Totals", psutil.cpu_count(logical=True)))
        values.append(("Fréquence Max", f"{cpufreq.max:.2f}MHz"))
        values.append(("Fréquence Min", f"{cpufreq.min:.2f}MHz"))
        values.append(("Fréquence Actuelle", f"{cpufreq.current:.2f}MHz"))
        values.append(("Utilisation CPU", f"{psutil.cpu_percent()}%"))
        return tabulate.tabulate(values, headers=headers)

    def get_mem_usage(self):
        # Récupère les informations sur l'utilisation de la mémoire (RAM et swap)
        headers = ("Étiquette Mémoire", "Valeur")
        values = []
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        values.append(("Mémoire Totale", self.get_size(svmem.total)))
        values.append(("Mémoire Disponible", self.get_size(svmem.available)))
        values.append(("Mémoire Utilisée", self.get_size(svmem.used)))
        values.append(("Pourcentage", f"{svmem.percent}%"))
        values.append(("Swap Total", self.get_size(swap.total)))
        values.append(("Swap Libre", self.get_size(swap.free)))
        values.append(("Swap Utilisé", self.get_size(swap.used)))
        values.append(("Pourcentage Swap", f"{swap.percent}%"))
        return tabulate.tabulate(values, headers=headers)

    def get_disk_info(self):
        # Récupère les informations sur les disques (taille totale, utilisée, libre, etc.)
        headers = ("Périphérique", "Point de Montage", "Système de Fichiers", "Taille Totale", "Utilisée", "Libre", "Pourcentage")
        values = []
        partitions = psutil.disk_partitions()
        for partition in partitions:
            partition_info = [
                partition.device,
                partition.mountpoint,
                partition.fstype,
            ]
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                partition_info.extend([
                    self.get_size(partition_usage.total),
                    self.get_size(partition_usage.used),
                    self.get_size(partition_usage.free),
                    f"{partition_usage.percent}%",
                ])
            except PermissionError:
                partition_info.extend(["", "", "", ""])
            values.append(partition_info)
        return tabulate.tabulate(values, headers=headers)

    def get_net_info(self):
        # Récupère les informations sur les interfaces réseau (adresse IP, MAC, etc.)
        headers = ('Interface', 'Adresse IP', 'Adresse MAC', 'Masque de Sous-Réseau', 'IP de Diffusion', 'MAC de Diffusion')
        values = []
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    values.append([
                        interface_name,
                        address.address,
                        '',
                        address.netmask,
                        address.broadcast,
                        '',
                    ])
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    values.append([
                        interface_name,
                        '',
                        address.address,
                        address.netmask,
                        '',
                        address.broadcast,
                    ])
        return tabulate.tabulate(values, headers=headers)

    def get_data(self):
        # Retourne toutes les informations collectées sous forme de chaîne de caractères
        return "\n".join([
            self.sysinfo,
            self.boot_time,
            self.cpu_info,
            self.mem_usage,
            self.disk_info,
            self.net_info,
        ])
