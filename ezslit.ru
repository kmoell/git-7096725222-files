# =================================================================
# Серверный блок для домена ezslit.ru
# Основная конфигурация для работы по HTTPS
# =================================================================
server {
    # Прослушивание 443 порта (HTTPS) с поддержкой SSL и HTTP/2
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    # Имя вашего домена. Nginx будет отвечать на запросы к ezslit.ru
    server_name ezslit.ru;

    # Путь к файлам вашего сайта. 
    # Ваш index.html должен лежать в /var/www/ezslit.ru/html/
    root /var/www/ezslit.ru/html;
    index index.html;

    # --- SSL/TLS Конфигурация ---
    # Эти пути будут автоматически созданы и настроены программой Certbot
    ssl_certificate /etc/letsencrypt/live/ezslit.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ezslit.ru/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # --- Настройки кэширования и сжатия ---
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # --- Заголовки безопасности ---
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    # Content Security Policy (CSP) - очень важный заголовок
    # Разрешает загрузку ресурсов только с доверенных источников
    add_header Content-Security-Policy "default-src 'self'; style-src 'self' 'unsafe-inline' fonts.googleapis.com; font-src 'self' fonts.gstatic.com; img-src 'self' i.ibb.co raw.githubusercontent.com; script-src 'self' 'unsafe-inline'; frame-ancestors 'none';" always;

    # --- Основная логика обработки запросов ---
    location / {
        # Пытаемся найти файл с точным именем. Если не находим - отдаем 404 ошибку.
        try_files $uri $uri/ =404;
    }

    # --- Логирование ---
    access_log /var/log/nginx/ezslit.ru.access.log;
    error_log /var/log/nginx/ezslit.ru.error.log;
}

# =================================================================
# Переадресация с WWW на основной домен
# Если кто-то зайдет на www.ezslit.ru, его перекинет на ezslit.ru
# =================================================================
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name www.ezslit.ru;

    # Пути к SSL сертификатам (также настраиваются Certbot)
    ssl_certificate /etc/letsencrypt/live/ezslit.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ezslit.ru/privkey.pem;

    # 301 редирект (постоянный) на основной домен без www
    return 301 https://ezslit.ru$request_uri;
}

# =================================================================
# Переадресация всего HTTP трафика на HTTPS
# Если кто-то зайдет на http://ezslit.ru, его перекинет на https://ezslit.ru
# =================================================================
server {
    listen 80;
    listen [::]:80;
    server_name ezslit.ru www.ezslit.ru;
    
    # 301 редирект на HTTPS версию сайта
    return 301 https://ezslit.ru$request_uri;
}