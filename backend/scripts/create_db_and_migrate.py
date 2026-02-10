import mysql.connector
import os
import subprocess
import sys

# Read DATABASE_URL from .env
from urllib.parse import urlparse

def read_env():
    env = {}
    p = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(p):
        with open(p) as f:
            for line in f:
                line=line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k,v=line.split('=',1)
                    env[k.strip()]=v.strip()
    return env

env = read_env()
url = env.get('DATABASE_URL')
if not url:
    print('DATABASE_URL not found in .env')
    raise SystemExit(1)

# parse mysql+mysqlconnector://user:pass@host:port/db
if url.startswith('mysql+mysqlconnector://'):
    stripped = url[len('mysql+mysqlconnector://'):]
else:
    stripped = url

# split credentials and db
creds, host_db = stripped.split('@')
user, password = creds.split(':',1)
host_port, dbname = host_db.split('/',1)
if ':' in host_port:
    host, port = host_port.split(':',1)
else:
    host = host_port
    port = '3306'

print(f'Using host={host} port={port} user={user} db={dbname}')

# Connect as root/admin and create database if not exists
try:
    conn = mysql.connector.connect(user=user, password=password, host=host, port=int(port))
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbname} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print(f'Database {dbname} ensured')
    cur.close()
    conn.close()
except Exception as e:
    print('Failed to create database:', e)
    raise

# Run alembic upgrade head
print('Running alembic migrations...')
subprocess.check_call([sys.executable, '-m', 'alembic', '-c', 'alembic.ini', 'upgrade', 'head'], cwd=os.path.join(os.path.dirname(__file__), '..'))
print('Migrations applied')
