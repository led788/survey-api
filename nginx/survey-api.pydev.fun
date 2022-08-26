server {
    server_name survey-api.pydev.fun;
    listen 80;
    location / {
        proxy_pass http://unix:/run/survey-api.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

}
