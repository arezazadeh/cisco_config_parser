from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException


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
            'fast_cli': False,
            'conn_timeout': 300,
            'timeout': 300,
            'read_timeout': 300,
        }
        try:
        
            self.ssh_conn = ConnectHandler(**shc_router)
        
        except NetmikoTimeoutException:
            return f"Timeout Failed for {host}"

        except NetmikoAuthenticationException:
            return f"Authentication Failed for {host}"

    def ssh(self, cmd):
        result = self.ssh_conn.send_command(cmd, cmd_verify=True)
        return result

    def send_config(self, config):
        result = self.ssh_conn.send_config_set(config, cmd_verify=False)
        return result

