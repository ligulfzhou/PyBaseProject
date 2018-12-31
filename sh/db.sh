cd /Users/zhouligang/Projects/oa/python3/api/sh
mysqldump -uroot -pMYSQLzhouligang153 xwx > xwx.sql

scp xwx.sql dajin:

ssh dajin << EOF 
mysql -uroot -pMYSQLzhouligang153 xwx < ~/xwx.sql 
EOF
