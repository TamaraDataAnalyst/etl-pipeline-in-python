import re


LOG_PATTERN = re.compile(r'(\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+).*' \
        r'(\S+).* (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)')


COLNAMES = ('date','time','client_ip','username','server_ip',
        'port','method','stem','query','status','server_bytes',
        'client_bytes','time_taken','user_agent','referrer')

SAVE_TO_CSV = 'log.csv'