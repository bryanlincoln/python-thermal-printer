SCRIPT="/etc/rc.local"
HERE=${PWD}
if [ ! -f $SCRIPT ]; then
    echo "exit 0" > /etc/rc.local
else
    N=$(wc -l "$SCRIPT")
    if [ "$N" == "0 /etc/rc.local" ]; then
        echo "exit 0" > /etc/rc.local
    fi
fi

sed -i '$ i # begin ticket generator' $SCRIPT
sed -i '$ i _OLD_DIR=${PWD}' $SCRIPT
sed -i '$ i cd '"$HERE" $SCRIPT
sed -i '$ i sudo python3 ticket.py &' $SCRIPT
sed -i '$ i echo "Ticket generator initialized!"' $SCRIPT
sed -i '$ i cd $_OLD_DIR' $SCRIPT
sed -i '$ i # end ticket generator' $SCRIPT