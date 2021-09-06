# achi-mon

0. Preinstall
```bash
python3 -m venv venv
. activate
pip install -r requirements.txt
```

1. Create file get_wallet_info.sh in <path_to>/achi-blockchain/
```bash
#!/usr/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$DIR"
. ./activate
achi wallet show -f $1
```


2. Make & Edit config

```bash
cp config.example.yaml config.yaml
vim config.yaml
```

3. Install Daemon

```bash
chmod 777 ./install/*.sh
./install/01_install_from_user.sh
sudo ./install/02_install_from_root.sh
```

4. Proof It!
