## Prefab Installation

You don't need to worry about this section if you're not familiar with [Jumpscale](https://github.com/Jumpscale)

**Install Bash tools**


```
curl https://raw.githubusercontent.com/Jumpscale/bash/master/install.sh?$RANDOM > /tmp/install.sh;bash /tmp/install.sh
source ~/.bash_profile
```

**Build Docker CRM Image**

```
ZInstall_crm -p 443 -u "crm.threefoldtoken.com" -o threefold.crm_users -s UrzXJ81iWdckOoOcqUbIoTeG_BD4Xo9-6ThaMpfOC5sW8apUYwad -i production_crm -e hamdya@greenitglobe.com
```

**Build Docker CRM Container**

```
ZInstall_crm -p 443 -i production_crm
ZDockerActive -b "jumpscale/js9_docgenerator" -a "-p 443:443 -p 80:80" -c "ZInstall_docgenerator" -i crm_production
```

**Access Docker CRM Container**
```
docker exec -ti crm bash
```

