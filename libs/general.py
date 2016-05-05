import logging
import time
import paramiko

class GenerLogger(object):
    def __init__(self, loggername):
        self.loggername = loggername

    def initLogger(self):
        logger = logging.getLogger(self.loggername)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileHandler = logging.FileHandler(
            '/home/huiwa/avocado_learn/avocado_cockpit/cockpit_test/logs/%s-%s.log' 
            % (self.loggername, time.strftime("%Y%m%d-%H:%M:%S")))
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        return logger


class EstabSSHConnect(object):
    def __init__(self, ipaddr, username, passwd):
        self.ipaddr = ipaddr
        self.username = username
        self.passwd = passwd

    def ssh_connect(self):
        conn = paramiko.SSHClient()
        conn.load_system_host_keys()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(self.ipaddr, 22, self.username, self.passwd)
        return conn