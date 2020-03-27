[0;1;32m●[0m mysql.service - LSB: Start and stop the mysql database server daemon
   Loaded: loaded (/etc/init.d/mysql; generated)
   Active: [0;1;32mactive (running)[0m since Tue 2020-03-24 07:17:41 EDT; 16min ago
     Docs: man:systemd-sysv-generator(8)
  Process: 476 ExecStart=/etc/init.d/mysql start (code=exited, status=0/SUCCESS)
   Memory: 76.6M
   CGroup: /system.slice/mysql.service
           ├─517 /bin/bash /usr/bin/mysqld_safe
           ├─671 /usr/sbin/mysqld --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib/arm-linux-gnueabihf/mariadb18/plugin --user=mysql --skip-log-error --pid-file=/var/run/mysqld/mysqld.pid --socket=/var/run/mysqld/mysqld.sock --port=3306
           └─672 logger -t mysqld -p daemon error

Mar 24 07:17:40 sentinel-0 mysqld[672]: [0;1;31m[0;1;39m[0;1;31mVersion: '10.0.28-MariaDB-2+b1'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  Raspbian testing-staging[0m
Mar 24 07:17:41 sentinel-0 mysql[476]: Starting MariaDB database server: mysqld . ..
Mar 24 07:17:41 sentinel-0 systemd[1]: Started LSB: Start and stop the mysql database server daemon.
Mar 24 07:17:41 sentinel-0 /etc/mysql/debian-start[730]: Upgrading MySQL tables if necessary.
Mar 24 07:17:42 sentinel-0 /etc/mysql/debian-start[734]: [0;1;39m[0;1;31m[0;1;39m/usr/bin/mysql_upgrade: the '--basedir' option is always ignored[0m
Mar 24 07:17:42 sentinel-0 /etc/mysql/debian-start[734]: [0;1;39m[0;1;31m[0;1;39mLooking for 'mysql' as: /usr/bin/mysql[0m
Mar 24 07:17:42 sentinel-0 /etc/mysql/debian-start[734]: [0;1;39m[0;1;31m[0;1;39mLooking for 'mysqlcheck' as: /usr/bin/mysqlcheck[0m
Mar 24 07:17:42 sentinel-0 /etc/mysql/debian-start[734]: [0;1;39m[0;1;31m[0;1;39mThis installation of MySQL is already upgraded to 10.0.28-MariaDB, use --force if you still need to run mysql_upgrade[0m
Mar 24 07:17:42 sentinel-0 /etc/mysql/debian-start[742]: Checking for insecure root accounts.
Mar 24 07:17:42 sentinel-0 /etc/mysql/debian-start[746]: Triggering myisam-recover for all MyISAM tables and aria-recover for all Aria tables
