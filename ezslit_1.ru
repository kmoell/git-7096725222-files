# =================================================================
# Переадресация с HTTP на HTTPS для ezslit.ru
# =================================================================
server {
    listen 80;
    listen [::]:80;
    server_name ezslit.ru;

    # Эта секция нужна Certbot для автообновления сертификата
    location ~ /.well-known/acme-challenge/ {
        root /var/www/ezslit.ru/html;
        allow all;
    }

    location / {
        return 301 https://ezslit.ru$request_uri;
    }
}

# =================================================================
# Основной серверный блок для ezslit.ru (HTTPS)
# =================================================================
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name ezslit.ru;

    root /var/www/ezslit.ru/html;
    index index.html;

    # --- SSL/TLS Конфигурация ---
    # Указываем пути к сертификатам, которые у вас уже есть
    ssl_certificate /etc/letsencrypt/live/ezslit.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ezslit.ru/privkey.pem;

    # Базовые настройки безопасности SSL (вместо отсутствующих файлов)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;

    # --- Настройки производительности и безопасности ---
    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Content-Security-Policy "default-src 'self'; style-src 'self' 'unsafe-inline' fonts.googleapis.com; font-src 'self' fonts.gstatic.com; img-src 'self' i.ibb.co raw.githubusercontent.com; script-src 'self' 'unsafe-inline'; frame-ancestors 'none';" always;

    # --- Логика обработки запросов ---
    location / {
        try_files $uri $uri/ =404;
    }

    # --- Логи ---
    access_log /var/log/nginx/ezslit.ru.access.log;
    error_log /var/log/nginx/ezslit.ru.error.log;
}