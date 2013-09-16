#coding=utf-8
import hashlib
import os, sys, re
import subprocess

# global definition
# base = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F]
base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]

# bin2dec

def bin2dec(string_num):
    return str(int(string_num, 2))

# hex2dec

def hex2dec(string_num):
    return str(int(string_num.upper(), 16))

# dec2bin

def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])

# dec2hex

def dec2hex(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 16)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])

# hex2tobin

def hex2bin(string_num):
    return dec2bin(hex2dec(string_num.upper()))

# bin2hex

def bin2hex(string_num):
    return dec2hex(bin2dec(string_num))





def set_hexdigest(algorithm,  raw_password):

    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, '')

    if algorithm == 'md5':
        return hashlib.md5(raw_password).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(raw_password).hexdigest()
    elif algorithm == 'passwd':
        pass1 = hashlib.sha1(raw_password).digest()
        pass2 = hashlib.sha1(pass1).hexdigest()
        return "*" + pass2.upper()

    raise ValueError("Got unkown password algorithm type in password.")





def get_hexdigest(algorithm, salt, raw_password):

    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        return hashlib.md5(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(salt + raw_password).hexdigest()


    raise ValueError("Got unkown password algorithm type in password.")



def check_password(raw_password, enc_password):

    algo, salt, hsh = enc_password.split('$')

    if hsh == get_hexdigest(algo, salt, raw_password):
        return True
    else:
        return False






def set_password(raw_password):
    import random
    algo = 'sha1'
    salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(algo, salt, raw_password)
    password = '%s$%s$%s' % (algo, salt, hsh)
    return password



def initlog():
    import logging
    logger2 = logging.getLogger(__name__)
    handler2=logging.FileHandler("/tmp/django_debug.log")
    formatter = logging.Formatter('%(asctime)s [%(pathname)s] (%(module)s.%(funcName)s) %(levelname)s > %(message)s')
    handler2.setFormatter(formatter)
    logger2.addHandler(handler2)
    logger2.setLevel(logging.INFO)
    #logger2.setLevel(logging.NOTSET)
    return logger2


#import logging
#if not hasattr(logging, "set_up_done"):
#    logging.set_up_done=False
#def initlog():
#    if logging.set_up_done:
#        return
#    logger2 = logging.getLogger(__name__)
#    handler2=logging.FileHandler("/tmp/django_debug.log")
#    formatter = logging.Formatter('%(asctime)s [%(pathname)s] (%(module)s.%(funcName)s) %(levelname)s > %(message)s')
#    handler2.setFormatter(formatter)
#    logger2.addHandler(handler2)
#    logger2.setLevel(logging.INFO)
#    #logger2.setLevel(logging.NOTSET)
#    logging.set_up_done=True
#    return logger2



#检查path中是否有无效的格式
def check_invalid_path_format(v_path=None):
    if v_path:
        invalid_format_list = [r'^\.\.\/', r'\/(\.){1,}\/', r'\/(\.){1,}$', r'(\/){2,}']
        check_result = False
        for invalid_format in invalid_format_list:
            if hasattr(re.search(invalid_format, v_path), 'group'):
                check_result = True
                break;

        return check_result
    else:
        return False



#替换路径 "/data/htdocs/www/proftpd/../proftpd/ftpadmin/"中的  'proftpd/../' 为 '' .
#替换路径 "/data/htdocs/www/./proftpd/ftpadmin/" 中的 './' 为 '' .
def fix_path(s_path=None):
    if s_path:
        s_path = s_path.strip()
        s_path = re.sub(r'([^/]+)\/\.\.\/', '', s_path)
        s_path = re.sub(r'\/{2,}', '/', s_path)
        s_path = re.sub(r'\.\/(?!$)', '', s_path)
        s_path = re.sub(r'\/(\.)+$', '/', s_path)
        if not hasattr(re.search(r'^\/$', s_path), 'group'):
            s_path = re.sub(r'\/$', '', s_path)
        
    return s_path

##替换路径 "/data/htdocs/www/proftpd/../proftpd/ftpadmin/"中的 'proftpd/../proftpd' 为 'proftpd'.
#def fix_path2(s_path=None):
#    if s_path:
#        s_path = s_path.strip()
#        sub_re = re.compile(r'(.*)\/\.\.\/(\1)')
#        def repl(m):
#            return re.sub(sub_re, m.group(1), m.group(0)) #m.group(1)为第一个括号内容”proftpd“， m.group(0) 则为匹配后的字符”proftpd/../proftpd“
#        s_path = re.sub(sub_re, repl, s_path)
#        s_path = re.sub(r'\/\/', '/', s_path)
#        s_path = re.sub(r'\.\/', '', s_path)
#
#    return s_path


def fill_path_with_slash(s_path=None):

    if s_path:
        if s_path.startswith('/') != True:
            s_path = '/' + s_path
        if s_path.endswith('/') != True:
            s_path = s_path + '/'
        return s_path
    else:
        return s_path

def check_safe_range(safe_range=(), c_type="number", v_value=None):
    if c_type == "number" and len(safe_range) == 2 and v_value:
        if int(safe_range[1]) > int(safe_range[0]):
            min_value = int(safe_range[0])
            max_value = int(safe_range[1])
        else:
            min_value = int(safe_range[1])
            max_value = int(safe_range[0])            
        if v_value in range(min_value, max_value+1):
            return True
        else:
            return False
    elif c_type == "startswith" and len(safe_range) and v_value:
        check_result = False
        for safe_value in safe_range:
            v_value = fill_path_with_slash(v_value)
            if v_value.startswith( fill_path_with_slash(safe_value) ):
                check_result = True
                break
            else:
                check_result = False
        return check_result
    else:
        return True


def do_nothing(*args, **kwargs):
    pass


def is_inside(s_array=[], d_array=[]):
    if len(s_array) > len(d_array):
        return False
    for s_a in s_array:
        if s_a not in d_array:
            return False
    return True


class shell(object):
    def __init__(self, callback=do_nothing, *args, **kwargs):
        self.error_code = 0 
        self.callback = callback
        

    def execute_c(self, x_command=None, x_parameters=[]):

        #print("exec shell_command ...\n" )
        #print("x_command=%s \n" % x_command)
        #print(x_parameters)
        self.callback(0)
        if os.path.exists(x_command) and os.path.isfile(x_command) and os.access(x_command, os.X_OK):
            parameter_string = ' '.join(x_parameters)
            #print("parameter_string = %s " % parameter_string)

            shell_command_string = 'LANG=C %s %s' %  (x_command, parameter_string)
            #print("shell_command_string = %s " % shell_command_string)

            p = subprocess.Popen(shell_command_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            shell_command_result = p.stdout.readlines()
            self.callback(0)
            return shell_command_result
        else:
            self.callback(-1)
            return None