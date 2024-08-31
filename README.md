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

## Corners Cut:

* Code was cranked out quickly using tools that was most comfortable with.
* Given more time would have used a nosql database or even a redis cache depending on retention requirements.
* Also, would optimize code for speed.  Example: I would not read from database after scan to retreive scan results for return.  This however reduces and simplifies the code.
* API uses database root user instead of user with only permissions required for application.
* In production the database wouldn't be in a container but an managed cloud service such as Elasticache or DyanmoDB.
* There is no authentication on the api.  Generally, this would be SAML or OAUTH unless isolated access in other ways.
* The application is running without encryption.  In production it would have a valid certificate and run under HTTPS.
* Given a production environment a CI/CD pipeline would have been created along with changes to the helm chart to accomodate.
