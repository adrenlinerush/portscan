registry:
	docker run -d -p 5000:5000 --restart=always --name registry registry:2

build:
	docker build . --tag localhost:5000/portscan
	docker push localhost:5000/portscan

deploy:
	helm install portscan ./k8s/portscan-chart -f ./k8s/portscan-chart/values.yaml

destroy:
	helm uninstall portscan 
