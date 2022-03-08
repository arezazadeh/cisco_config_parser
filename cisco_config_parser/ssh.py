from netmiko import ConnectHandler


class MySSH:
    def __init__(self, host, user, password, device_type):
        self.user = user
        self.password = password
        self.host = host

        shc_router = {
            'device_type': device_type,
            'host': host,
            'username': self.user,
            'password': self.password,
        }

        self.ssh_conn = ConnectHandler(**shc_router)

    def ssh(self, cmd):
        result = self.ssh_conn.send_command_timing(cmd, cmd_verify=True, delay_factor=1000)
        return result

    def send_config(self, config):
        result = self.ssh_conn.send_config_set(config, cmd_verify=False)
        return result
