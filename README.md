# Portscan

**Description:** An API that scans for open ports on a set of IP addresses. Results returned in json. Results persist and are stored in database for later retreival by ip or scan_id.  Also, two scans may be compared via API.

**Development:(VS Code with Docker)**

* Clone this repository
* Open directory with VS Code
* Re-Open in container ![Devcontainer](./img/devcontainer.jpeg)
* API should be available at localhost:4000

**Usage:** Refer to swagger documentation: http://localhost:4000/apidocs
![Swagger](./img/swagger.png)

**src/ports2scan** contains ports to be scanned

**Tests:** Run ```pytest``` from the src directory.  When openning a terminal in VS Code it should already be in a venv with requirements installed from within the devcontainer.
![pytest](./img/pytest.png)

## Kubernetes Deployment:

**Local Environment(run outside devcontainer):**

* ```make setup_dev_kubernetes``` to setup local k3s environment and install helm (Debian)
* Potentially could fail to add ```127.0.0.1 portscan.local``` to /etc/hosts
* ```make registry``` to start local registry in docker.
* ```make build``` to build the container and push to registry.
* ```make deploy``` to deploy to local k3s.
* ```make destroy``` to remove deployment.
* Swagger: http://portscan.local/apidocs

## Things I may have changed or have done diffently...

* Considered other backends such as nosql, redis or opensearch.
* Optimize code for speed.
* Create database user with only permissions required for application.
* Add authentication such as saml or oauth to API.
