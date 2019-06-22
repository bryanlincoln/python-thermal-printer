echo "Criando startup.sh"
echo "#!/bin/bash" > startup.sh
# echo PASSWORD | sudo -S COMMAND
echo "/usr/bin/python3 ${PWD}/ticket.py &" > startup.sh
echo "Copiando para /etc/init.d"
cp startup.sh /etc/init.d/startup.sh
echo "Linkando para /etc/rc0.d"
rm -rf /etc/rc0.d/startup.sh
ln -s /etc/init.d/startup.sh /etc/rc0.d/
rm -rf startup.sh
echo "Limpando..."