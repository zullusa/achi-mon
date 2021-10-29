# achi-mon

Use this to monitor farm with telegram.

0. Preinstall

```bash
git clone https://github.com/zullusa/achi-mon.git
cd achi-mon
python3 -m venv venv
. activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo 149.154.167.220 api.telegram.org | sudo tee -a /etc/hosts
```

1. Create file get_wallet_info.sh in <path_to>/achi-blockchain/ with content and make executable `chmod ugo+x get_wallet_info.sh`
```bash
#!/usr/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$DIR"
. ./activate
achi wallet show -f $1
echo -----------------
achi farm summary | grep -P -e "^[^N]"
achi show -s | grep -P -e "^Current diff.*"
achi show -c | awk '{print $1"\t"$2}' | grep -P -e "FULL_NODE" | echo Nodes count: `wc -l`
```

2. Install certificate, if you want to use Heartbeat. I use Lets'Encrypt certificates. 
Or you need cabundle.pem from yours certificate form the API Service.
```
openssl x509 -in ./certs/cabundle.pem -text >> venv/lib/python<YOUR_VERSION>/site-packages/certifi/cacert.pem
```

3. Make & Edit config

```bash
cp config.example.yaml config.yaml
vim config.yaml
```
change
- api-key - use @BotFather, to get it
- channel - it works with public and private channel (private channel only via id)
- $USER - your user name
- path_to - Path to achi-blockchain directory

4. Install Daemon

```bash
chmod 777 ./install/*.sh
./install/01_install_from_user.sh
sudo ./install/02_install_from_root.sh
```

5. Pro(o)fit!

# FAQ
### Where can I find you?
In [discord](https://discord.gg/DZhBc5pCng) nickname zilog


# TODO
1. dd for bust disk cache `* * * * * /bin/bash -c 'dd if=/dev/disk/by-uuid/THE-UUID of=/dev/null count=1 skip=$RANDOM'`
2. ~~supplement information for wallet check `current_value - previous value` "growing"
and `current_time - previous_time` "expected time"~~
3. ~~switch off polling in config.yaml~~
4. ~~Heartbeat~~
5. ~~Different notification settings for different pollings~~
