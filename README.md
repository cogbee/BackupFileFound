# BackupFileFound
说明

我们在编程的时候，在配置网站的时候，很多时候会无意之间留下一些备份文件和测试文件，这些备份文件一般以.bak后缀结束。该程序就是在这样的情况下写出来的。主要目的是去捕捉这些文件。因为这些文件泄露了也是比较头疼的事情，很可能是一场灾难。
花了一个下午时间，测试了一个晚上，目前是第一版本。


过程：
url---->遍历该网站，获取每一个满足条件的url----->测试bak后缀文件是否存在或一些测试文件是否存在------>保存测试过的url以及命中的url



实现：

1、测试url后缀.bak是否存在。

2、在url后面添加1或数字加1进行测试，是否有测试文件

例如：

url:http://www.test.com/test.php  

程序会测试：

http://www.test.com/test.php.bak

http://www.test.com/test1.php

是否存在

如果url：http://www.test.com

url没有path，那么不会测试任何



如果url：http://www.test.com/test

测试url：http://www.test.com/test.bak

http://www.test.com/test1


综上。

程序可以带cookie。会让用户输入cookie。如果没有cookie，可以忽略。


目前需要改进的地方：

1、多线程。这需要一个很好的worker，以及分发主线程。目前在构思

2、将这个py文件分拆。不同的功能在各自的py文件。尤其是一些过滤的url条件。

3、需要更进一步深入打击目标，一些url这样测试没有必要。一些重要的，比如config.bak文件才比较有用。

4、挑选关键字，这样可以过滤这些东西出来。比如，后缀为.db,.sql,.log,等。这些文件比较重要

