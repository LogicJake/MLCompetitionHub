#!/bin/sh

# 安装 resolvconf
CheckRequirement(){
	if  [ ! -e '/usr/sbin/resolvconf' ] && [ ! -e '/sbin/resolvconf' ]; then
		echo "正在安装必要的程序 resolvconf ，请稍后..."
		sudo apt-get update
		sudo apt-get -y install resolvconf > /dev/null 2>&1
	fi
	sudo systemctl stop resolvconf.service > /dev/null 2>&1
	sudo systemctl start resolvconf.service > /dev/null 2>&1
	sudo systemctl enable resolvconf.service > /dev/null 2>&1
}

# 修改 DNS
DoChange(){
	sudo echo "nameserver 114.114.114.114" > /etc/resolv.conf
	sudo echo "nameserver 114.114.114.114" > /etc/resolvconf/resolv.conf.d/head
	sudo systemctl restart resolvconf.service
}

# 交互内容
ChangeDNS(){
	CheckRequirement
	echo "当前 Nameserver 如下："
	cat /etc/resolv.conf | grep nameserver
	DoChange
	echo "已修改，当前 Nameserver 如下："
	cat /etc/resolv.conf | grep nameserver
}

ChangeDNS