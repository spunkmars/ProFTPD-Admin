import re, os

from proftpd.ftpadmin.settings import  FILE_PATH
from proftpd.ftpadmin.lib.common import is_inside, shell, fix_path, initlog

class proftpd_base(object):
    
    def __init__(self, *args, **kwargs):
        self.error_code = 0
        self.proftpd_base_path = fix_path( FILE_PATH.get('proftpd_path', '/opt/proftpd') )

    def error_count(self, error_code=None):
        if error_code != None:
            self.error_code = error_code
        else:
            return self.error_code

    def shell_command(self, x_command=None, x_parameters=[]):
        self.shell = shell(callback=self.error_count)
        shell_command_result = self.shell.execute_c(x_command=x_command, x_parameters=x_parameters)
        return shell_command_result


class proftpd_info(proftpd_base):

    def __init__(self, *args, **kwargs):
        self.error_code = 0
        self.proftpd_base_path = fix_path( FILE_PATH.get('proftpd_path', '/opt/proftpd') )
        self.proftpd_path = self.proftpd_base_path + '/sbin/proftpd'
        self.ftpwho = FILE_PATH.get('ftpwho_path', self.proftpd_base_path + '/bin/ftpwho')

    def compile_time_settings(self):
        settings_result = self.shell_command(x_command=self.proftpd_path, x_parameters=[' -V'])
        if self.error_count() < 0:
            return 'proftpd -V  error'
        else:
            return  settings_result

    def compiled_in_modules(self):
        compiled_in_modules_result = self.shell_command(x_command=self.proftpd_path, x_parameters=[' -l'])
        if self.error_count() < 0:
            return 'proftpd -l  error'
        else:
            return  compiled_in_modules_result

    def loaded_modules(self):
        loaded_modules_result = self.shell_command(x_command=self.proftpd_path, x_parameters=[' -vv'])
        if self.error_count() < 0:
            return 'proftpd -vv  error'
        else:
            return  loaded_modules_result

    def online_status(self):
        ftp_server_info = {}
        k_parameters = []
        k_parameters.append(' --outform "oneline" -v')
        
        ftpwho_restult = []
        ftpwho_restult = self.shell_command(x_command=self.ftpwho, x_parameters=k_parameters)
        if self.error_count() < 0:
            return ' exec ' + self.ftpwho + 'error !'
        else:
            ftpwho_list = ftpwho_restult
            
            first_line = ftpwho_list.pop(0)
            last_line = ftpwho_list.pop()
        
            ftp_server_info = self.get_ftpwho_server_info(line=first_line)
            ftp_server_info.update( self.get_ftpwho_user_count(line=last_line) )
            ftp_server_info['status'] = self.get_ftpwho_status(ftpwho_list=ftpwho_list)
            return ftp_server_info


    def get_ftpwho_server_info(self, line=None):
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
    
            
    
    def get_ftpwho_user_count(self, line=None):
        server_info = {}
        s_re = re.compile(r'^Service\sclass\s+-\s+(?P<user_count>\d+)\susers$')
        m = s_re.search(line)
        server_info['user_count'] = 0
        if hasattr(m, 'group'):
            server_info['user_count'] = m.group('user_count')
    
        return server_info
    
    
    def get_ftpwho_status(self, ftpwho_list=[]):
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



class proftpd_conf(object):
    pass




class proftpd_ctrls(proftpd_base):
    

    def __init__(self, *args, **kwargs):
        self.error_code = 0
        self.proftpd_base_path = fix_path( FILE_PATH.get('proftpd_path', '/opt/proftpd') )
        self.proftpd_ftpdctl_sock = self.proftpd_base_path + '/var/proftpd.sock'
        self.ftpdctl_init_parameter = " -s %s " % self.proftpd_ftpdctl_sock
        self.ftpdctl_path = self.proftpd_base_path + '/bin/ftpdctl'
        

    def debug(self, **kwargs):
        k_parameters=[]
        k_objective = kwargs.get('k_objective',  [])
        k_parameters.append('debug')
        if len(k_objective) > 0 :
            k_parameters.append(' '.join(k_objective))
        else:
            k_parameters.append('config')
            #k_parameters.append('memory')
            #k_parameters.append('level')

        debug_result = self.shell_command(x_command=self.ftpdctl_path, x_parameters=k_parameters)
        

        if self.error_count() < 0:
            return 'ftpdctl get  error'
        else:
            return  debug_result

    def dns(self, **kwargs):
        k_parameters=[]
        k_objective = kwargs.get('k_objective',  [])
        k_parameters.append('dns')
        if len(k_objective) > 0 :
            k_parameters.append(' '.join(k_objective))
        else:
            k_parameters.append('on')
            #k_parameters.append('off')
            #k_parameters.append('clear cache')

        dns_result = self.shell_command(x_command=self.ftpdctl_path, x_parameters=k_parameters)
        
        if self.error_count() < 0:
            return 'ftpdctl get  error'
        else:
            return  dns_result


    def down(self, **kwargs):
        k_parameters=[]
        k_objective = kwargs.get('k_objective',  [])
        k_parameters.append('down')
        if len(k_objective) > 0 :
            k_parameters.append(' '.join(k_objective))
        else:
            k_parameters.append('"all"')

        down_result = self.shell_command(x_command=self.ftpdctl_path, x_parameters=k_parameters)
        

        if self.error_count() < 0:
            return 'ftpdctl down  error'
        else:
            return  down_result

    def dump(self, **kwargs):
        k_parameters=[]
        k_objective = kwargs.get('k_objective',  [])
        k_parameters.append('dump')
        if len(k_objective) > 0 :
            k_parameters.append(' '.join(k_objective))
        else:
            k_parameters.append('config')
            #k_parameters.append('memory')
            #k_parameters.append('classes')
        dump_result = self.shell_command(x_command=self.ftpdctl_path, x_parameters=k_parameters)
        

        if self.error_count() < 0:
            return 'ftpdctl get  error'
        else:
            return  dump_result


    def get(self, **kwargs):
        k_parameters=[]
        k_objective = kwargs.get('k_objective',  [])
        k_parameters.append('get')
        if len(k_objective) > 0 :
            k_parameters.append(' '.join(k_objective))
        else:
            k_parameters.append('"config"')
            #k_parameters.append('"directives"')
        get_result = self.shell_command(x_command=self.ftpdctl_path, x_parameters=k_parameters)
        

        if self.error_count() < 0:
            return 'ftpdctl get  error'
        else:
            return  get_result


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
 

    def restart(self, **kwargs):
        k_parameters=[]
        k_objective = kwargs.get('k_objective',  [])
        k_parameters.append('restart')
        if len(k_objective) > 0 :
            k_parameters.append(' '.join(k_objective))

        restart_result = self.shell_command(x_command=self.ftpdctl_path, x_parameters=k_parameters)
        

        if self.error_count() < 0:
            return 'ftpdctl restart  error'
        else:
            return  restart_result


    def scoreboard(self):
        pass


    def shutdown(self, **kwargs):
        k_parameters = []
        k_parameters.append('shutdown')
        shutdown_result = self.shell_command(x_command=self.ftpdctl_path, x_parameters=k_parameters)
        
        if self.error_count() < 0:
            return 'ftpdctl shutdown  error'
        else:
            return  shutdown_result


    def status(self, **kwargs):

        k_type = kwargs.get('k_type', None)
        k_objective = kwargs.get('k_objective',  [])
        k_parameters = ['status']
        if len(k_objective) > 0 :
            k_parameters.append(' '.join(k_objective))
        else:
            k_parameters.append('"all"')

        status_result = self.shell_command(x_command=self.ftpdctl_path, x_parameters=k_parameters)
        if self.error_count() < 0:
            return 'ftpdctl status  error'
        else:
            return  status_result


    def trace(self):
        pass

    def up(self, **kwargs):
        k_parameters=[]
        k_objective = kwargs.get('k_objective',  [])
        k_parameters.append('up')
        if len(k_objective) > 0 :
            k_parameters.append(' '.join(k_objective))
        else:
            k_parameters.append('0.0.0.0')

        up_result = self.shell_command(x_command=self.ftpdctl_path, x_parameters=k_parameters)
        

        if self.error_count() < 0:
            return 'ftpdctl up  error'
        else:
            return  up_result



