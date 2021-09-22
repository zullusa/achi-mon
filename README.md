# achi-mon

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

1. Create file get_wallet_info.sh in <path_to>/achi-blockchain/ with content

```bash
#!/usr/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$DIR"
. ./activate
achi wallet show -f $1
```

2. Create file get_farm_summary.sh in <path_to>/achi-blockchain/

```bash
#!/usr/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$DIR"
. ./activate
achi farm summary
```
3. Install certificate, if you want to use Heartbeat. I use Lets'Encrypt certificates. 
Or you need cabundle.pem from yours certificate form the API Service.
```
openssl x509 -in ./certs/cabundle.pem -text >> venv/lib/python<YOUR_VERSION>/site-packages/certifi/cacert.pem
```

4. Make & Edit config

```bash
cp config.example.yaml config.yaml
vim config.yaml
```
change
- api-key - use @BotFather, to get it
- channel - it works with public and private channel (private channel only via id)
- $USER - your user name
- path_to - Path to achi-blockchain directory

5. Install Daemon

```bash
chmod 777 ./install/*.sh
./install/01_install_from_user.sh
sudo ./install/02_install_from_root.sh
```

6. Pro(o)fit!

# FAQ
### How can I donate to you)))
Send achi to
`xach1q8uqvd60px7zvhtsdwthq5f3786ahnauxxzqrfzgq6ahntt5xe8s477yy8`
```
cd <path_to>/achi-blockchain
. activate
achi wallet send -f <your_fingerprint> -a <how_much> -t xach1q8uqvd60px7zvhtsdwthq5f3786ahnauxxzqrfzgq6ahntt5xe8s477yy8 
```
### Where can I find you?
In [discord](https://discord.gg/DZhBc5pCng) nickname zilog


# TODO
1. dd for bust disk cache `* * * * * /bin/bash -c 'dd if=/dev/disk/by-uuid/THE-UUID of=/dev/null count=1 skip=$RANDOM'`
2. ~~supplement information for wallet check `current_value - previous value` "growing"
and `current_time - previous_time` "expected time"~~
3. ~~switch off polling in config.yaml~~
4. ~~Heartbeat~~
5. ~~Different notification settings for different pollings~~