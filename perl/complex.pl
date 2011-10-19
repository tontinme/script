#!/usr/bin/perl
#http://www.dongwm.com/archives/fuzashijiancepchulijieguozhanshijiaoben/#codesyntax_2
#use strict;
#use warnings;
use Term::ReadKey;
use Term::ANSIColor;
use Getopt::Long;
use Pod::Usage;
use Time::HiRes qw ( time alarm sleep );
Getopt::Long::Configure('bundling');
 
#变量设定
$|=1;					#激活autoflush，将缓冲区的内容立即送出
@ltime=localtime();
my $date=sprintf("%d-%d-%d",$ltime[5]+1900,$ltime[4]+1,$ltime[3]);		#当天日期
my $Clear=`clear`;			#调用系统命令 clear
sub Clear();				#
sub GetHead();
 
#颜色的定义
import Term::ANSIColor ':constants';
my $RESET  = RESET()   || '';
my $YELLOW = YELLOW()  || '';
my $RED    = RED()     || '';
my $GREEN  = GREEN()   || '';
my $BLUE   = BLUE()    || '';
my $WHITE  = WHITE()   || '';
my $BOLD   = BOLD()    || '';
 
#读取配置文件
my $config='/cepdata/conf/complex.cfg';
my %config;				#配置文件hash
get_config();				#读取配置文件内容，存入%config
 
#读取命令行参数
my @opt_spec=(
	{ s => 'h', d => 'display help message'},
	{ s => 'p', d => '选择默认展示页面'},
);
GetOptions(
	"p=s" => \$choose,
	"h"	  => \$help
) or pod2usage(1);
 
if ($help) {
	foreach my $spec (sort {$a->{s} cmp $b->{s}}  @opt_spec) {
        printf "  -%-4s %-15s\n",$spec->{s},$spec->{d};
		if ("$spec->{s}" eq 'p') {
			foreach my $page (sort keys %{$config{pagelist}}) {
				printf "%10s => %-10s\n",$config{pagelist}{$page}->{hotkey},$config{pagelist}{$page}->{desc} || $page;
					}
			}
    }
	exit 0;
}
 
Clear();
#日志目录
my $LogPath=$config{main}->{logpath};
#页面切换的准备
my %pagelist;					#为页面切换准备的hash, hotkey  => Page
my $hotkeylist;					# qr/[abc]/ a,b,c为快捷键
for_change_page();				#读取%config中的pagelist，生成%pagelist
 
my %printlist=reverse %pagelist;
my $listline;
foreach my $page (sort keys %printlist) {
	if ($page =~ /^C/) {
	    $listline .="\e[0;31m<$printlist{$page}>\e[0;32m$page\t";
	} elsif ($page =~ /^Java/) {
	    $listline .="\e[0;31m<$printlist{$page}>\e[0;33m$page\t";
	} elsif ($page =~ /^Ops/) {
            $listline .="\e[0;31m<$printlist{$page}>\e[0;36m$page\e[0m\t";
	} elsif ($page =~ /^Php/) {
            $listline .="\e[0;31m<$printlist{$page}>\e[0;34m$page\e[0m\t";
        }
      }
 
#打开所有文件句柄
foreach my $fh (values %pagelist) {
		my $logfile;
        if ($config{pagelist}->{$fh}->{logfile} =~ /^\//) {
            $logfile="$config{pagelist}->{$fh}->{logfile}.$date";
        } else {
            $logfile="$LogPath/$config{pagelist}->{$fh}->{logfile}.$date";
        }
		open $fh,"<$logfile";		#为每个日志文件打开句柄，句柄名为页面名
	}
 
my $warning='99999';
my $critimal='99999';
my $Page=$pagelist{$choose} || $config{main}->{defaultpage};	#默认页面
#GetOptions(
#	'p:s' => \$Page,
#	'w:f' => \$warning,
#	'c:f' => \$critimal,
#	'f:i' => \$SortOrder,
#	);
ChangePage();					#切换页面，改变参数
 
#页面切换相关变量
my $key=0;					#捕获键盘输入，默认值0
my $lines_left;					#终端行数
my $diff=0;					#值为1时,切换页面
my $listpages=0;				#值为1时,显示页面列表供切换
 
print RED();
print "Waiting for New Data.....\n";
print RESET();
 
#============#
# Main Loop	 #
#============#
 
#ReadMode
#    0    Restore original settings.
#    1    Change to cooked mode.
#    2    Change to cooked mode with echo off.
#          (Good for passwords)
#    3    Change to cbreak mode.
#    4    Change to raw mode.
#    5    Change to ultra-raw mode.
 
#ReadKey
#    0    Perform a normal read using getc
#    -1   Perform a non-blocked read
#    >0   Perform a timed read
 
#ReadLine
#    0    Perform a normal read using scalar(<FileHandle>)
#    -1   Perform a non-blocked read
#    >0   Perform a timed read
 
ReadMode(3);
while (1) {
	if ( $diff ) {
			ChangePage();		#切换页面，改变参数
			$diff = 0;		#改为0,下次循环跳过页面切换
			}
	&GetMtime(new);
	if ("$new_mtime" == "$old_mtime") {	#文件修改时间未变化时
		sleep 0.1;			#sleep 0.5秒
		next;				#继续主循环
		}
	else {
		GetHead();			#设置终端参数，输出描述信息
		OutPut();			#输出页面内容
		$key=ReadKey(5);		#捕获键盘输入
		}
	unless ($key) {				#没有键盘输入时
		next;				#继续主循环
		}
	if ( $key =~ /q/ ) {			#键入 q ，退出程序
		ReadMode(0);
		print "\n";
		exit;
		}
	if ( $key =~ /l/ ) {
		$listpages= $listpages?0:1;
		if ($listpages) {
		print "$listline\n";
		}
		$key=0;
		ReadMode(3);
		}
	if ( $key =~ /p/ ) {
        print RED();
		print '-- paused. press any key to resume --';					#暂停页面输出
		print RESET();
        ReadKey(0);
        next;
		$key=0;
		}
	if ( $key =~ $hotkeylist ) {			#读入快捷键
		ReadMode(0);
		$Page=$pagelist{$key};			#根据快捷键切换改变默认页面
		$diff =1;				#将$diff设置为1,下次主循环会先进行页面切换工作
		print RED(),"FLUSH AT NEXT TIME";
		print RESET();
		ReadMode(3);
		$key=0;					#将捕获键盘输入设为0
		$listpages=0;
		next;
		}
}
 
#==========#
#  子程序  #
#==========#
 
#==清屏==#
sub Clear()
{
	print "$Clear";
}
 
#==打印描述信息==#
sub GetHead()
{
	my ($width, $height, $wpx, $hpx) = GetTerminalSize();	#获取终端长宽高等信息
    $lines_left = $height - 3;					#获取行数，并预留3行
	my $time=`date +%T`;
	chomp($time);
	Clear();						#清屏
	print GREEN();
	print "Page: $desc\t\tTime: $time\n";			#打印页面描述，当前时间
	$lines_left--;
	print RESET();
}			
 
#==页面内容输出==#
sub OutPut{
 
    print YELLOW();
    printf "$f_title\n",@Fieldname;  #打印标题
    #printf "$f_title\n",$Fieldname[0],$Fieldname[1],$Fieldname[2],$Fieldname[3],$Fieldname[4];  #打印标题
	$lines_left--;																				
 
    print RED();
    printf "$f_title\n",'-' x $F_gang[0],'-' x $F_gang[1],'-' x $F_gang[2],'-' x $F_gang[3],'-' x $F_gang[4],'-' x $F_gang[5];	#打印 -----
    $lines_left--;
	print RESET();
 
	#记录了所有行
	my @record;
	my $href;
	while (<$Page>) {
		chomp();
		if ($_ =~ $regex) {						#正则匹配取出所需值
		next if ("$4" eq "-");
		if ("$Page" eq "OpsAgent") {
			my $agent = substr("$4",0,100);
			$href = {'1'=>$1,'2'=>$2,'3'=>$3,'4'=>$agent,'5'=>$5,'6'=>$6};
			} else {
			$href = {'1'=>$1,'2'=>$2,'3'=>$3,'4'=>$4,'5'=>$5,'6'=>$6};	#引用hash
			}
		push @record,$href;						#将引用存入数组
			}
	}
 
	#排序并输出
	my @sorted;
	@sorted = sort { $b->{$SortOrder} <=> $a->{$SortOrder} } @record;
	foreach my $row (@sorted) {
		last unless $lines_left;
		printf "$format\n",$row->{1},$row->{2},$row->{3},$row->{4},$row->{5},$row->{6};
		$lines_left--;
	}
 
	#打印常用功能键
	print "\n" while ($lines_left--);
	print RED(),"<l>",BLUE(),"PAGELIST\t",RED(),"<p>",BLUE(),"PAUSE\t",RED(),"<q>",BLUE(),"QUIT\n",RESET();
 
	#打印页面切换的快捷键
        print "$listline\n" if ($listpages);
 
	#记录文件修改时间
	&GetMtime(old);
}
 
#==读取配置文件==#
sub get_config
{
	open CEPCONF,"<$config" or die "can't open configfile!";	#打开配置文件
	while (<CEPCONF>) {
		next if /^$/;						#忽略空行
		next if /^\s*\#/;					#忽略注释
		if (my ($menu) = /\[(\w+)\]/) {				#遇到[a]
				while (<CEPCONF>) {			#循环读取[a]下的内容
					next if /^$/;
					next if /^\s*\#/;
					last if /\[\/(\w+)\]/;		#如果遇到[/a]结束此循环
					chomp;
					if (my ($pagename) = /\[(\w+)\]/) {	#又遇到[b]
						while (<CEPCONF>) {			#循环读取[]下的内容
						next if /^$/;
						next if /^\s*\#/;
						last if /\[\/(\w+)\]/;			#如果遇到[/b]结束此循环
						chomp;
						my ($cfg_key,$cfg_value)= split /=/;	#获取以=分隔的变量名，变量值
						$cfg_key =~ s/^\s+|\s+$//g;		#去掉变量名前后的空白字符
						$cfg_value =~ s/\#.*$//g;		#去掉变量值后的注释
						$cfg_value =~ s/^\s+|\s+$//g;		#去掉变量值前后的空白字符
						$cfg_value =~ s/['"]//g;		#去掉变量值前后的引号
						$config{$menu}->{$pagename}->{$cfg_key}=$cfg_value;		#将变量名、变量值存入hash $config{a}->{b}->{变量名}=变量值
							}
						}
					next if /\[\/(\w+)\]/;				#遇到[/b]跳过
					my ($cfg_key,$cfg_value)= split /=/;		#获取以=分隔的变量名，变量值
				$cfg_key =~ s/^\s+|\s+$//g;				#同上
			$cfg_value =~ s/\#.*$//g;
		$cfg_value =~ s/^\s+|\s+$//g;
		$cfg_value =~ s/['"]//g;					#去掉变量值前后的引号
	$config{$menu}->{$cfg_key} = $cfg_value;	#存入hash $config{a}->{变量名}=变量值
			}
		}
	}
	close CEPCONF;		#关闭文件句柄
}
 
#==为页面切换准备的hash==#
sub for_change_page{
	my @pages= keys %{$config{pagelist}};					#取出pagelist下的所有键，即所有页面名
	foreach my $value (@pages) {
		$pagelist{$config{pagelist}->{$value}->{hotkey}} = $value;	# hotkey => page
			}
	foreach my $hotkey (keys %pagelist) {
		$hotkeylist .= $hotkey;						#将hotkey连接起来
		}
		$hotkeylist = qr/[$hotkeylist]/;				#构建正则表达式
}
 
#==获取文件修改时间==#
sub GetMtime{
	my $type=shift;
	if ( $type =~ /new/) {
		$new_mtime=(stat ($logfile))[9];
		}
	elsif ( $type =~ /old/ ) {
		$old_mtime=(stat ($logfile))[9];
		}
}
 
#==页面切换工作==#
sub ChangePage{
	seek $Page,0,2;								#读到文件结尾
	if ($config{pagelist}->{$Page}->{logfile} =~ /^\//) {
            our $logfile="$config{pagelist}->{$Page}->{logfile}.$date";
        } else {
            our $logfile="$LogPath/$config{pagelist}->{$Page}->{logfile}.$date";
        }
#	our $logfile="$LogPath/$config{pagelist}->{$Page}->{logfile}.$date";	#日志文件名
	our $desc = $config{pagelist}->{$Page}->{desc} ||$Page ;		#描述信息，默认为页面名
	&GetMtime(old);								#记录文件修改时间，被用来比较
 
	our $SortOrder=$SortOrder ||$config{pagelist}->{$Page}->{sortorder} || 1;
 
	our $fields=$config{pagelist}->{$Page}->{fields};			#取出列名
	our @Fieldname = split /\s+/,$fields;					#将列名存入数组
	our $format=$config{pagelist}->{$Page}->{format};			#取出结果输出格式
	our $f_title=$format;							#列名的输出格式
	$f_title =~ s/\.\d+f|d/s/g;						#列名都为字符串，将其它格式转成字符串
 
	our $f_gang = $f_title;							#分割线---，和列名一样的输出格式
	$f_gang =~ s/[^\d\s]//g;						#
	our @F_gang = split /\s+/,$f_gang;					#每列要输出多少个-，计入数组
	my $count = @Fieldname;							#列的数目
 
	my $num = $count;							#定一个值，和列的数目一样，用途为计算数组下标
	my $tmp_regex;								#声明临时正则表达式
	while ($count) {
		$tmp_regex .= $Fieldname[$num -$count] . '=' . '([^,]+),\s*';	#每个列名后连一个等号和一个正则表达式
		$count--;
		}
	$tmp_regex =~ s/,\\s\*$//;						#去掉正则表达式末尾的 ,\s*
	our $regex = qr/$tmp_regex/;						#构建正则表达式，存入变量中
}
