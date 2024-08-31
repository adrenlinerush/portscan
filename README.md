# Portscan

**Description:** An API that scans for open ports on a set of IP addresses. Results returned in json. Results persist and are stored in database for later retreival by ip or scan_id.  Also, two scans may be compared via api.  API itself is stateless.

**Development:(VS Code with Docker)**

* Clone this repository
* Open directory with VS Code
* Re-Open in container ![Devcontainer](./img/devcontainer.jpeg)
* API should be available at localhost:4000

**Usage:** Refer to swagger documentation: http://localhost:4000/apidocs
![Swagger](./img/swagger.png)

**src/ports2scan** contains ports to be scanned

**Tests:** Run ```pytest``` from the src directory within venv.

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
* Given more time would probably have used other database and potentially api framework.
* Also, would optimize code for speed.  Example: not goto to database after scan to retreive scan results for return.
* Database uses root user instead of user with only permissions required for application.
* Database probably wouldn't be in a container but an managed cloud service.
* There is no authentication on the api.
* The application is running without encryption.
