# achi-mon

0. Preinstall

```bash
git clone https://github.com/zullusa/achi-mon.git
cd achi-mon
python3 -m venv venv
. activate
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

3. Install Daemon

```bash
chmod 777 ./install/*.sh
./install/01_install_from_user.sh
sudo ./install/02_install_from_root.sh
```

4. Pro(o)fit!

# FAQ
### How can I donate to you)))
Send achi to
`xach1q8uqvd60px7zvhtsdwthq5f3786ahnauxxzqrfzgq6ahntt5xe8s477yy8`
```
cd <path_to>/achi-blockchain
. activate
achi wallet send -f <your_fingerprint> -a <how_much> -t xach1q8uqvd60px7zvhtsdwthq5f3786ahnauxxzqrfzgq6ahntt5xe8s477yy8 
```

