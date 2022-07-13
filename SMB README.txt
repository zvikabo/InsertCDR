https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/storage_administration_guide/mounting_an_smb_share

As root user do the following:

1.  install the cif package :
	# yum install cifs-utils

2. creat directory :
	/SBCLOG
3. creat file 
	/root/smb.cred  (chmod 600)
	
	username=Admin
	password=1234567
	domain=workgroup

4. add to /etc/fstab
//10.10.10.10/SBC  /SBCLOG  cifs  sec=ntlmssp,credentials=/root/smb.cred  0 0

How to....
1. show all mountes device 
	# mount
2. un mount 
	#unmount /SBC_CTILOG
3. mount all mountes that configured in /etc/fstab
	# mount -a
	
	
