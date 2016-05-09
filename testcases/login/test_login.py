import sys
sys.path.append("/home/huiwa/avocado_learn/avocado_cockpit/cockpit_test")
import re
from confs import comm
from libs import general
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys


class TestLogin(object):
    def __init__(self):
        init_logger = general.GenerLogger(sys.argv[0])
        self.logger = init_logger.initLogger()
        self.testurl = comm.testurl
        self.ipaddr = comm.ipaddr
        self.username = comm.username
        self.passwd = comm.passwd
        self.ssh_login = general.EstabSSHConnect(
            self.ipaddr, self.username, self.passwd)
        self.ssh_conn = self.ssh_login.ssh_connect()
        self.rhevh_version = comm.rhevh_version_36
        self.result = 0

    def init_webdirver(self):
        self.logger.info("Inital Firefox as the testing webdriver!")
        driver = Firefox()
        driver.implicitly_wait(20)
        driver.get(self.testurl)
        return driver

    def login(self, web_driver):
        web_driver = web_driver
        username_field = web_driver.find_element_by_id("login-user-input")
        username_field.send_keys(self.username)
        passwd_field = web_driver.find_element_by_id("login-password-input")
        passwd_field.send_keys(self.passwd)

        login_btn = web_driver.find_element_by_id("login-button")
        login_btn.send_keys(Keys.ENTER)
        result = self.check_login_status(web_driver)
        return result

    def check_login_status(self, web_driver):
    	web_driver = web_driver
    	web_driver.implicitly_wait(10)
    	current_user = web_driver.find_element_by_id("content-user-name").text

    	if current_user.strip() == self.username:
    		self.logger.info("Login with '%s' succeed!" % self.username)
    		self.result += 0
    	else:
    		self.logger.error("Login with '%s' failed!" % self.username)
    		self.result += 1
    	return self.result

    def get_all_infos_in_server(self):
        stdin, stdout, stderr = self.ssh_conn.exec_command("hostname")
        s_hostname = stdout.read()
        return s_hostname

    def check_server_name_in_login_page(self, web_driver):
        web_driver = web_driver
        server_name = str(web_driver.find_element_by_id('server-name').text)
        s_hostname = self.get_all_infos_in_server().strip()
        f = re.compile(s_hostname)

        if f.findall(server_name):
            self.logger.info("Login page shows '%s'" % server_name)
            self.logger.info("Hostname in host is '%s'" % s_hostname)
            self.result += 0
        else:
            self.logger.error("Login page shows '%s'" % server_name)
            self.logger.error("Hostname in host is '%s'" % s_hostname)
            self.result += 1
        return self.result

    def check_version_in_login_page(self, web_driver, verion_name):
    	web_driver = web_driver
    	version_in_login = str(web_driver.find_element_by_id("brand").text)
    	verion_name = verion_name.upper()
    	f = re.compile(verion_name)

    	if f.findall(version_in_login):
    		self.logger.info("Login Page shows '%s'" % version_in_login)
    		self.logger.info("Version should be '%s'" % verion_name)
    		self.result += 0
    	else:
    		self.logger.error("Login Page shows '%s'" % version_in_login)
    		self.logger.error("Version should be '%s'" % verion_name)
    		self.result += 1
    	return self.result


    def run(self):
        f_driver = self.init_webdirver()
        total_result = self.check_version_in_login_page(f_driver, self.rhevh_version)
        total_result += self.check_server_name_in_login_page(f_driver)
        total_result += self.login(f_driver)
        f_driver.close()
        return total_result


if __name__ == "__main__":
    login = TestLogin()
    login.run()
