### do this
`apt-get update --fix-missing`

### things needed to be nstalled
* git
* vim
* xz-utils
* crust
* arduino

### where are things installed
* FOSS/own github repositories: `/usr/local/src`
* Third party software: `/opt`

### setup ssh keys
```
ssh-keygen -t rsa -b 4096 -C "austinhartline@gmail.com"
# no passphrase
```

### setup ssh connecting to pi
```
ssh-copy-id root@<ip address of pi or hostname>
```


