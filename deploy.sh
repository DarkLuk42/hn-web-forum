git status

echo "\n\n------------------------------------------\n\n"

#git reset HEAD --hard
git checkout master
git pull origin master

if [ -f tmp/server.pid ]
then
 kill `cat tmp/server.pid`
fi
fuser -n tcp 8080 -k

nohup ./server.py > tmp/log.txt 2> tmp/log.txt < /dev/null &
echo $! > tmp/server.pid

echo "\n\n------------------------------------------\n\n"

git status
