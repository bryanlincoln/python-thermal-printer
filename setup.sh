SCRIPT="/etc/rc.local"
HERE=${PWD}

echo "Criaremos uma entrada para executar $HERE/ticket.py no arquivo /etc/rc.local"
echo ""

if [ ! -f $SCRIPT ]; then
    echo "/etc/rc.local não existe. Criando..."
    echo ""
    echo "exit 0" > /etc/rc.local
else
    N=$(wc -l "$SCRIPT")
    if [ "$N" == "0 /etc/rc.local" ]; then
        echo "/etc/rc.local existe mas não tem conteúdo. Populando..."
        echo ""
        echo "exit 0" > /etc/rc.local
    else
        echo "/etc/rc.local não está vazio. Criaremos um backup chamado /etc/rc.local.old"
        echo ""
        cp /etc/rc.local /etc/rc.local.old
    fi
fi

echo "Adicionando entradas ao /etc/rc.local..."
echo ""

sed -i '$ i # begin ticket generator' $SCRIPT
sed -i '$ i _OLD_DIR=${PWD}' $SCRIPT
sed -i '$ i cd '"$HERE" $SCRIPT
sed -i '$ i sudo python3 ticket.py &' $SCRIPT
sed -i '$ i echo "Ticket generator initialized!"' $SCRIPT
sed -i '$ i cd $_OLD_DIR' $SCRIPT
sed -i '$ i # end ticket generator' $SCRIPT

echo "Pronto. Você pode reiniciar o dispositivo."