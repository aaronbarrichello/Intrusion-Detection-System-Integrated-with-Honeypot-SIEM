import subprocess, time, random, datetime, os

VM4_IP       = '192.168.100.40'
WEB_URL      = 'http://192.168.100.40'
LOG_FILE     = 'admin_activity.log'
DURASI_MENIT = 30

def log(msg):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = '[' + now + '] ' + msg
    print(line)
    with open(LOG_FILE, 'a') as fl:
        fl.write(line + chr(10))

def akses_web():
    pages = ['/', '/index.html', '/about', '/login', '/dashboard']
    page = random.choice(pages)
    try:
        result = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', WEB_URL + page], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        code = result.stdout.decode().strip()
        log('[WEB] GET ' + page + ' -> HTTP ' + code)
    except Exception as e:
        log('[WEB] Gagal: ' + str(e))

def cek_service(nama):
    try:
        result = subprocess.run(['systemctl', 'is-active', nama], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        status = result.stdout.decode().strip()
        log('[SERVICE] ' + nama + ' -> ' + status)
    except Exception as e:
        log('[SERVICE] Gagal cek ' + nama + ': ' + str(e))

def cek_log(path):
    try:
        result = subprocess.run(['tail', '-5', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        lines = result.stdout.decode().strip().split(chr(10))
        log('[LOG] ' + path + ' -> ' + str(len(lines)) + ' entri')
    except Exception as e:
        log('[LOG] Gagal baca ' + path + ': ' + str(e))

def cek_disk():
    try:
        result = subprocess.run(['df', '-h', '/'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        out = result.stdout.decode().strip().split(chr(10))
        if len(out) > 1:
            log('[DISK] ' + out[1])
    except Exception as e:
        log('[DISK] Gagal: ' + str(e))

def cek_network():
    targets = ['192.168.100.10', '192.168.100.30', '192.168.100.1']
    target = random.choice(targets)
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '2', target], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        status = 'OK' if result.returncode == 0 else 'UNREACHABLE'
        log('[PING] ' + target + ' -> ' + status)
    except Exception as e:
        log('[PING] Gagal: ' + str(e))

def cek_memory():
    try:
        result = subprocess.run(['free', '-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        out = result.stdout.decode().strip().split(chr(10))
        if len(out) > 1:
            log('[MEM] ' + out[1])
    except Exception as e:
        log('[MEM] Gagal: ' + str(e))

def tulis_file_test():
    try:
        fname = '/tmp/admin_' + str(random.randint(1000,9999)) + '.txt'
        with open(fname, 'w') as fl:
            fl.write('admin activity test')
        os.remove(fname)
        log('[FILE] Buat dan hapus: ' + fname)
    except Exception as e:
        log('[FILE] Gagal: ' + str(e))

def nginx_config_test():
    try:
        result = subprocess.run(['sudo', 'nginx', '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        status = 'OK' if result.returncode == 0 else 'ERROR'
        log('[NGINX] Config test -> ' + status)
    except Exception as e:
        log('[NGINX] Gagal: ' + str(e))

def jalankan_aktivitas():
    pilihan = random.randint(1, 10)
    if pilihan <= 3:
        akses_web()
    elif pilihan == 4:
        cek_service('nginx')
    elif pilihan == 5:
        cek_service('mysql')
    elif pilihan == 6:
        cek_service('vsftpd')
    elif pilihan == 7:
        cek_log('/var/log/nginx/access.log')
    elif pilihan == 8:
        cek_disk()
    elif pilihan == 9:
        cek_network()
    elif pilihan == 10:
        cek_memory()

start = time.time()
durasi_detik = DURASI_MENIT * 60
log('====== Admin Simulator Dimulai ======')
log('Service: Nginx, MySQL, FTP (vsftpd)')
log('Durasi : ' + str(DURASI_MENIT) + ' menit')
try:
    while time.time() - start < durasi_detik:
        jalankan_aktivitas()
        jeda = random.randint(10, 30)
        time.sleep(jeda)
except KeyboardInterrupt:
    pass
log('====== Admin Simulator Selesai ======')
log('Log tersimpan di: ' + LOG_FILE)
