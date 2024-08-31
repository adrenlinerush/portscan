# Portscan

**Description:** API for scanning open for open ports on a set of IP addresses.

**Development:**

* Clone this repository
* Open directory with VS Code
* Re-Open in container
* API should be available at localhost:4000

**Usage:** Refer to swagger documentation: http://localhost:4000/apidocs

**src/ports2scan** contains ports to be scanned

**.env** contains environment variable for databse connection in devcontainer

**Tests:** Run ```pytest``` from the src directory.

#### Kubernetes Deployment:

**Local Environment:**

* Tested on ARM64 (Orange PI 5) Running Armbian Bookworm
* Default k3s local install
* Helm installed from: deb https://baltocdn.com/helm/stable/debian/ all main
* Added ```127.0.0.1 portscan.local``` to /etc/hosts
* Container registry runing in docker. ```make registry```
* ```make build``` to build the container and push to registry.
* ```make deploy``` to deploy to local k3s.
* ```make destroy``` to remove deployment.
* Swagger: http://portscan.local/apidocs

#### Corners Cut:

* Code is not optimized. One example is that /scan writes to the db and then uses the same function as /scan/scan_id to query the db to retrieve it instead of using data in memory.  This was done for speed of development.
* No thought was put into whether functionality should be put into separate class/module for reuseability.
* I did not put much thought into language, framework, or data storage.  Is flask the best option out there and would a nosql database have been better?  Would a redis cache met the requirements?
* Very little error handling and input validation done.
* Database uses root user instead of user with only permissions required for application.
* Database probably wouldn't be in a container but an RDS instance or alike.
* There is no authentication on the api.
* The application is running without encryption.
* Makefile is very simple and rudimentary.
