import subprocess
import re, os

from proftpd.ftpadmin.settings import  FILE_PATH
from proftpd.ftpadmin.lib.common import is_inside, shell, fix_path, initlog

def get_ftpwho_server_info(line=None):
    server_info = {}
    s_re = re.compile(r'^(?P<server_type>.*)\s+\[(?P<server_pid>\d+)\],\sup\sfor\s*(-)?((?P<up_day>\d+)\sday)?(s)?(,)?\s*(-)?((?P<up_hour>\d+)\shr)?(s)?\s+(-)?(?P<up_min>\d+)\smin$')
    m = s_re.search(line)
    if hasattr(m, 'group'):
        server_info['server_type'] = m.group('server_type')
        server_info['server_pid'] = m.group('server_pid')
        if m.group('up_day'):
            server_info['up_day'] = m.group('up_day')
        else:
            server_info['up_day'] = 0
        if m.group('up_hour'):
            server_info['up_hour'] = m.group('up_hour')
        else:
            server_info['up_hour'] = 0
        server_info['up_min'] = m.group('up_min')

    return server_info

        

def get_ftpwho_user_count(line=None):
    server_info = {}
    s_re = re.compile(r'^Service\sclass\s+-\s+(?P<user_count>\d+)\susers$')
    m = s_re.search(line)
    server_info['user_count'] = 0
    if hasattr(m, 'group'):
        server_info['user_count'] = m.group('user_count')

    return server_info


def get_ftpwho_status(ftpwho_list=[]):
    s_re = re.compile(r'^\s*(?P<pid>\d+)\s(?P<username>.*)\s\[\s(?P<time1>.*)\]\s+(?P<time2>.*)\s(?P<cmd>.*)\sclient:\s(?P<client_ip>.*)\sserver:\s(?P<server_ip>.*)\s\((?P<server_name>.*)\)\sprotocol:\s(?P<protocol>.*)\slocation:\s(?P<location>.*)$')
    output_list = []
    for line in ftpwho_list:
        line_dict = {}
        m = s_re.search(line)
        if hasattr(m, 'group'):
            line_dict['pid'] = m.group('pid')
            line_dict['username'] = m.group('username')
            line_dict['time1'] = m.group('time1')
            line_dict['time2'] = m.group('time2')
            line_dict['cmd'] = m.group('cmd')
            line_dict['client_ip'] = m.group('client_ip')
            line_dict['server_ip'] = m.group('server_ip')
            line_dict['server_name'] = m.group('server_name')
            line_dict['protocol'] = m.group('protocol')
            line_dict['location'] = m.group('location')
            output_list.append(line_dict)
    
    return output_list

def get_proftpd_compile_time_settings():
    pass
    #./proftpd -V

def get_proftpd_compiled_in_modules():
    pass
    #./proftpd -l

def get_proftpd_loaded_modules():
    pass
    # ./proftpd -vv

def get_ftp_info():
    ftp_server_info = {}
    ftpwho = FILE_PATH.get('ftpwho_path', '/opt/proftpd/bin/ftpwho')
    if os.path.exists(ftpwho) and os.path.isfile(ftpwho) and os.access(ftpwho, os.X_OK):
        ftpwho_command = 'LANG=C %s --outform "oneline" -v' %  ftpwho
        p = subprocess.Popen(ftpwho_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ftpwho_list = p.stdout.readlines()
        
        first_line = ftpwho_list.pop(0)
        last_line = ftpwho_list.pop()
    
        ftp_server_info = get_ftpwho_server_info(line=first_line)
        ftp_server_info.update( get_ftpwho_user_count(line=last_line) )
        ftp_server_info['status'] = get_ftpwho_status(ftpwho_list=ftpwho_list)

    return ftp_server_info





class proftpd_conf(object):
    pass







class proftpd_ctrls(object):
    

    def __init__(self, *args, **kwargs):
        self.error_code = 0
        self.proftpd_base_path = fix_path( FILE_PATH.get('proftpd_path', '/opt/proftpd') )
        self.proftpd_ftpdctl_sock = self.proftpd_base_path + '/var/proftpd.sock'
        self.ftpdctl_init_parameter = " -s %s " % self.proftpd_ftpdctl_sock
        self.ftpdctl_path = self.proftpd_base_path + '/bin/ftpdctl'
        

    def error_count(self, error_code=None):
        if error_code != None:
            self.error_code = error_code
        else:
            return self.error_code

    def shell_command(self, x_command=None, x_parameters=[]):
        self.shell = shell(callback=self.error_count)
        shell_command_result = self.shell.execute_c(x_command=x_command, x_parameters=x_parameters)
        return shell_command_result

    def debug(self):
        pass

    def dns(self):
        pass

    def down(self):
        pass

    def dump(self):
        pass

    def get(self):
        pass


    def kick(self, **kwargs):
        '''
        from proftpd.ftpadmin.lib.ftp_info import proftpd_ctrls
        ctrls = proftpd_ctrls()
        ctrls.kick(k_type='user', k_objective=['test1'])
        '''
        k_type = kwargs.get('k_type', None)
        k_objective = kwargs.get('k_objective',  [])
        k_host = kwargs.get('k_host', None)
        k_host_n = kwargs.get('k_host_n', None)
        k_class = kwargs.get('k_class',  [])

        valid_k_type = ['user', 'host', 'class']
        valid_k_class = ['eval' 'intranet']
        if k_type in valid_k_type and len(k_objective)>0:
            k_parameters = [ self.ftpdctl_init_parameter, 'kick', k_type ]
            if k_type == 'host' and k_host is not None:
                if k_host_n is not None:
                    k_parameters.append("-n %s" % k_host_n)
                k_parameters.append(k_host)
            elif k_type == 'user' and len(k_objective)>0:
                k_parameters.append(' '.join(k_objective))
            elif k_type == 'class' and len(k_class)>0 and is_inside(k_class, valid_k_class):
                k_parameters.append(' '.join(k_class))
            else:
                return 'invalid args'
            k_result = self.shell_command(x_command=self.ftpdctl_path, x_parameters=k_parameters)
            if self.error_count() < 0:
                return 'kick exec error'
            else:
                return  k_result
        else:
            return 'invalid k_type or k_objective is null'
 

    def restart(self):
        pass

    def scoreboard(self):
        pass

    def shutdown(self):
        pass

    def status(self):
        status_result = self.shell_command(x_command=self.ftpdctl_path, x_parameters=['status  all'])
        return status_result

    def trace(self):
        pass

    def up(self):
        pass



