#Update system
#sudo apt-get update
#sudo apt-get upgrade -y

#Install Apache2
if [ ! $(dpkg -l | grep apache2 | wc -l) ]
then
	sudo apt-get install apache2 -y
	sudo a2enmod rewrite
	sudo service apache2 restart
	#Install PHP
	sudo apt-get install php libapache2-mod-php -y
else
	echo "Apache2 already installed"
fi
#Install MySQL
if [ ! $(dpkg -l | grep mariadb-server | wc -l) ]
then
	sudo apt-get install mariadb-server-10.0 python3-dev libpython3-dev python3-mysqldb -y
	sudo service apache2 restart
else 
	echo "MySQL already installed"
fi
if [ ! $(dpkg -l | grep python3-mysql.connector | wc -l) ]
then
	sudo apt-get install python3-mysql.connector -y
else 
        echo "Python3 MySQL-connector already installed"
fi
echo "create database IF NOT EXISTS Sentry" | mysql -uroot -pa-51d41e

if [ ! $(echo "SELECT User FROM mysql.user;"  | mysql -uroot -pa-51d41e | grep "pi" | wc -c) ]
then
	echo "CREATE USER 'pi'@'localhost' IDENTIFIED BY 'a-51d41e';"  | mysql -uroot -pa-51d41e
	echo "GRANT ALL PRIVILEGES ON Sentry.* TO 'database_user'@'localhost';"  | mysql -uroot -pa-51d41e
	echo "create table BattDATA (date (datetime) PRIMARY KEY,ChargeLevel INT(3),ChargeStatus VARCHAR(15),Vbat FLOAT(6,2),IBat FLOAT(6,2),Wbat FLOAT(6,2),Vio FLOAT(6,2),Iio FLOAT(6,2),Wio FLOAT(6,2),RPIPower varchar(15),HATPower varchar(15)" | mysql -upi -pa-51d41e Sentry
fi

if [ ! $(dpkg -l | grep pijuice-base | wc -l) ]
then
	sudo apt-get install pijuice-base -y
else 
        echo "PiJuice already installed"
fi

if [ ! $(dpkg -l | grep  grafana-rpi | wc -l) ]
then
	echo "installing Grafana"
	wget https://dl.grafana.com/oss/release/grafana-rpi_6.6.1_armhf.deb
	sudo dpkg -i grafana-rpi_6.6.1_armhf.deb
	rm -f ./grafana-rpi_6.6.1_armhf.deb
else
	echo "Grafana already installed"
fi

if [ ! $(dpkg -l | grep  git | wc -l) ]
then
	sudo apt-get install git -y
fi
if [ -d ./Sentry ]
then 
	mv -f ./Sentry ./Sentry-backup
fi 
git clone https://github.com/re3e-yul/Sentry.git

cd ./Sentry
./Sentry.py
