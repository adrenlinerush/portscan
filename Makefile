setup_dev_kubernetes:
	curl -sfL https://get.k3s.io | sh -
	export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
	curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
	sudo apt-get install apt-transport-https --yes
	echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
	sudo apt-get update
	sudo apt-get install helm
	sudo echo "127.0.0.1 portscan.local" >> /etc/hosts

registry:
	docker run -d -p 5000:5000 --restart=always --name registry registry:2

build:
	docker build . --tag localhost:5000/portscan
	docker push localhost:5000/portscan

deploy:
	sudo KUBECONFIG=/etc/rancher/k3s/k3s.yaml helm install portscan ./k8s/portscan-chart -f ./k8s/portscan-chart/values.yaml
	sudo KUBECONFIG=/etc/rancher/k3s/k3s.yaml kubectl get pods

destroy:
	sudo KUBECONFIG=/etc/rancher/k3s/k3s.yaml helm uninstall portscan
	sudo KUBECONFIG=/etc/rancher/k3s/k3s.yaml kubectl get pods
