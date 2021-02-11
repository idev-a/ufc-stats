<!-- gunicorn.service -->
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/ufc-stats/fighter
ExecStart=/home/ubuntu/ufc-stats/fighter/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/ufc-stats/fighter/fighter.sock fighter.wsgi:application   

[Install]           
WantedBy=multi-user.target                          

<!-- Daphne deploy -->
[Unit]              
Description=myproject Daphne Service           
After=network.target       
[Service]
Type=simple
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/ufc-stats/fighter
ExecStart=/home/ubuntu/ufc-stats/fighter/venv/bin/daphne -b 0.0.0.0 -p 9001  fighter.asgi:application
[Install]           
WantedBy=multi-user.target 

<!-- nginx -->
upstream socket_server {                  	
	server localhost:9001;          
}       server {
	listen 80;
	listen [::]:80;
	server_name 18.220.33.195 test.fightquake.com;       
	root /home/ubuntu/ufc-stats/frontend/dist;
	index index.html index.htm index.nginx-debian.html;

	location /robots.txt {
		alias /home/ubuntu/ufc-stats/frontend/public/robots.txt;           
	}

	location /sitemap.xml {
		alias /home/ubuntu/ufc-stats/frontend/public/sitemap.xml;
	}

	location / {
		try_files $uri $uri/ /index.html;
		#proxy_pass http://localhost:8085;
	}

	location /api {           
		#proxy_pass http://localhost:8000;
		include proxy_params;    
		proxy_pass http://unix:/run/gunicorn.sock;
		#proxy_pass http://gunicorn_server;
	}                       

	location /auth {          
		#proxy_pass http://localhost:8000;            
		include proxy_params;    
		proxy_pass http://unix:/run/gunicorn.sock;    
		#proxy_pass http://gunicorn_server; 
	}


	location /admin {         
		include proxy_params;    
		proxy_pass http://unix:/run/gunicorn.sock;    
		#proxy_pass http://localhost:8000;   
	}                       

	location /ws/ {           
		include proxy_params;    
		#proxy_pass http://unix:/run/gunicorn.sock;    
		proxy_pass http://socket_server;              
		proxy_http_version 1.1;                       
		proxy_set_header Upgrade $http_upgrade;       
		proxy_set_header Connection "upgrade";        
		#proxy_set_header Host $host;         
	}

	location = /favicon.ico { 
		access_log off; log_not_found off; 
	}

	location /static/ {
		root /home/ubuntu/ufc-stats/fighter;
	}

	location /robots.txt {
		alias /home/ubuntu/ufc-stats/frontend/public/robots.txt
	}                         
}  

 ## psycopg2
 sudo apt install libpq-dev python3-dev gcc