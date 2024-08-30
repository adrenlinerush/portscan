# Portscan

**Description:** API for scanning open for open ports on a set of IP addresses.

**Development:**

* Clone this repository
* Open directory with VS Code
* Re-Open in container
* API should be available at localhost:4000

**Usage:**

| Route         | Method | Payload Example                                                                                          |
| ------------- | ------ | -------------------------------------------------------------------------------------------------------- |
| /health       | GET    |                                                                                                          |
| /scan         | POST   | ```{"ip_list": ["10.1.1.1","10.1.1.2","10.1.1.102","101.1.1.112"]}```                                    |
| /scan/ip      | GET    | ```{"ip": "10.1.1.1"}```                                                                                 |
| /scan/scan_id | GET    | ```{"scan_id": "92c0500a8e234bd7b10e22688dc61cd4"}```                                                    |
| /compare      | GET    | ```{"scan_id_1": "92c0500a8e234bd7b10e22688dc61cd4", "scan_id_2": "6735ec7ce9564ebdb3a2e662913c6d72"}``` |

**example_usage.sh** provides curl examples

**src/ports2scan** contains ports to be scanned

**.env** contains environment variable for databse connection in devcontainer

**Kubernetes Deployment:**

**Corners Cut:**

* Code is not optimized. One example is that /scan writes to the db and then uses the same function as /scan/scan_id to query the db to retrieve it instead of using data in memory.
* No thought was put into whether functionality should be put into separate class/module for reuseability.
* There is no unit testing. I tried to break everything down to very simple functions to limit potential for error but only simple curl spot testing was done.
* I did not put much thought into language, framework, or data storage.  Is flask the best option out there and would a nosql database have been better.  Would a redis cache met the requirements?
* Swagger doc wasn't added hence curl being using to validate.
* Very little error handling and input validation done.
* Database uses root user instead of user with only permissions required for application.
* Database probably wouldn't be in a container but an RDS instance or alike.
* There is no authentication on the api.
* The application is running without encryption.
