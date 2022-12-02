build:
	docker build -t server .
run:
	docker run -d -p 8080:80 server
compose:
	docker-compose up 

	

