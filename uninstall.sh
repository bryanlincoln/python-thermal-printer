echo "Creating a backup of current /etc/rc.local to /etc/rc.local.restore"
mv /etc/rc.local /etc/rc.local.restore
echo "Restoring /etc/rc.local previous backup..."
mv /etc/rc.local.old /etc/rc.local
echo "Done. You may reboot now but it's not necessary."