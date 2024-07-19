import platform
import psutil
import tabulate
from datetime import datetime

class SystemInfo:
    def __init__(self):
        self.sysinfo = self.get_sys_info()
        self.boot_time = self.get_boot_time()
        self.cpu_info = self.get_cpu_info()
        self.mem_usage = self.get_mem_usage()
        self.disk_info = self.get_disk_info()
        self.net_info = self.get_net_info()

    def get_size(self, bolter, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bolter < factor:
                return f"{bolter:.2f}{unit}{suffix}"
            bolter /= factor

    def get_sys_info(self):
        headers = ("Platform Tag", "Information")
        values = []
        uname = platform.uname()
        values.append(("System", uname.system))
        values.append(("Node Name", uname.node))
        values.append(("Release", uname.release))
        values.append(("Version", uname.version))
        values.append(("Machine", uname.machine))
        values.append(("Processor", uname.processor))
        return tabulate.tabulate(values, headers=headers)

    def get_boot_time(self):
        headers = ("Boot Tags", "Information")
        values = []
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        values.append(("Boot Time", f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"))
        return tabulate.tabulate(values, headers=headers)

    def get_cpu_info(self):
        headers = ("CPU Tag", "Value")
        values = []
        cpufreq = psutil.cpu_freq()
        values.append(("Physical Cores", psutil.cpu_count(logical=False)))
        values.append(("Total Cores", psutil.cpu_count(logical=True)))
        values.append(("Max Frequency", f"{cpufreq.max:.2f}Mhz"))
        values.append(("Min Frequency", f"{cpufreq.min:.2f}Mhz"))
        values.append(("Current Frequency", f"{cpufreq.current:.2f}Mhz"))
        values.append(("CPU Usage", f"{psutil.cpu_percent()}%"))
        return tabulate.tabulate(values, headers=headers)

    def get_mem_usage(self):
        headers = ("Memory Tag", "Value")
        values = []
        svmem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        values.append(("Total Mem", self.get_size(svmem.total)))
        values.append(("Available Mem", self.get_size(svmem.available)))
        values.append(("Used Mem", self.get_size(svmem.used)))
        values.append(("Percentage", f"{svmem.percent}%"))
        values.append(("Total Swap", self.get_size(swap.total)))
        values.append(("Free Swap", self.get_size(swap.free)))
        values.append(("Used Swap", self.get_size(swap.used)))
        values.append(("Percentage Swap", f"{swap.percent}%"))
        return tabulate.tabulate(values, headers=headers)

    def get_disk_info(self):
        headers = ("Device", "Mountpoint", "File System", "Total Size", "Used", "Free", "Percentage")
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
        headers = ('Interface', 'IP Address', 'MAC Address', 'Netmask', 'Broadcast IP', 'Broadcast MAC')
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
        return "\n".join([
            self.sysinfo,
            self.boot_time,
            self.cpu_info,
            self.mem_usage,
            self.disk_info,
            self.net_info,
        ])
