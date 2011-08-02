#!/usr/bin/env python
#Recover Deletion of Data!!!!!
import os,re,urllib,sys
if sys.platform != 'linux2':
    sys.exit
else:
    recovery = 'ext3grep-0.10.2.tar.gz' #Recovered Toos

if not os.path.isfile(recovery):
    website = 'http://jy56.nimads.com' + os.sep + recovery
    print 'Downloading .............."%s"' % recovery
    loading = urllib.urlopen(website)
    localfile = open(recovery,'wb').write(loading.read())
    loading.close

#Install ext3grep
tar_command = 'tar -zxf "%s"'% recovery
checkdir = re.match (recovery[:-7],recovery)
make = './configure;make;make install'

if not os.path.isdir(checkdir.group()):
    os.system(tar_command)
    os.chdir(checkdir.group())
    os.system(make)

#Umount disk partitions
def main():
    if os.system('umount -l %s' % opt) != 0:
        raw_input ('Your disk partition are errors in the input')
def res():
    os.system("ext3grep %s --restore-file '%s'"%(opt,ans))
class disk:
    def pt(self):
        global opt 
        if part.lower() == 'q':
            sys.exit()
        elif part.lower() == 'b':
            os.system('fdisk -l') 
            opt = raw_input('Please,Enter the disk partition that you want to umount:')
            return opt
            main()
        elif part.lower() == 'c':
            os.system('fdisk -l') 
            opt = raw_input('Please,Enter the disk partition that you want to recovery:')
            return opt
            #main()
        elif part.lower() == 'a':
            os.system('df -Tlh')
            opt = raw_input('Please,Enter the disk partition that you want to umount:')
            main()
            return opt
        else:
            opt = 'err'
#Create Scan and recovery
    def sf(self):
        global age
        if opt != 'err':
            scan = 'ext3grep %s --ls --inode 2'#Scan files
            if os.system(scan%opt) == 0:
                age='--' * 40
                print age

    def info(self):
        global info
        info = raw_input('1:Recovery files\n2:Reovery anythings\nB:Back Meu\nDo you want to recover files or directorys:') 
        if info.lower() == 'b':
            info = 'stop'
        return True
    def exc(self):
            z = info 
            while z != 'stop':

                if z == '1':
                    global ans 
                    ans = raw_input('\n********************\nB:Stop and Back Meu\n********************\nPlase, you need to recovery file name:')
                    if ans.lower() == 'b':
                        z = 'stop'
                    try:
                        if type(int(ans)) is int:
                            os.system('ext3grep  %s --ls --inode %d'%(opt,int(ans))) 
                    except:
                            res() 
                elif z == '2':
                    os.system("ext3grep %s --restore-all "%opt)
                    ans = raw_input('\n********************\nData recovery success cases\n********************\nPlease,input B key back Meu:')
                    if ans.lower() == 'b':
                        z = 'stop'


                else:
                    print '************your input error*************'
                    d.info()
                    z = info

                #    res()%(opt,ans)
            
d = disk()
while 0 < 1:
    os.system('clear')
    print '--' * 30
    print '\t\tA:Unmount a disk partition\n\n'
    print '\t\tB:Unmount all disk partitions\n\n'
    print '\t\tC:Recover files and directorys\n\n'
    print '\t\tQ:Quit'
    print '--' * 30
    part = raw_input('\t\tPlase,you choose to option :')
    d.pt()
    d.sf()
    if ('age' in dir())is True:
        d.info()
        d.exc()
        del age
    del opt
    del part

