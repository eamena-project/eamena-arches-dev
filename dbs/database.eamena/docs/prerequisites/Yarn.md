Yarn is installable from many package managers, but in order to select a specific version, one must use NPM, the Node Package Manager. This in turn needs Node.JS to be installed. So we need to install all three of these. We also use npm to install n, which is a script for upgrading/downgrading to a specific version of NodeJS, which can then be used to upgrade the other two.

## Install NodeJS, NPM and Yarn

```bash
sudo apt-get update
sudo apt-get install nodejs npm
sudo npm i -g n
sudo n 14.17.6
sudo npm i -g npm@latest
sudo npm i -g yarn@latest
```

### Versions tested

Node.JS: 14.17.6
NPM: 8.19.3 / 9.6.0
Yarn: 1.22.19

If using the 'commands above installs a different version of NPM or Yarn, you can install the versions I have tested as working using...
```shell
sudo npm i -g npm@9.6.0
sudo npm i -g yarn@1.22.19
```
