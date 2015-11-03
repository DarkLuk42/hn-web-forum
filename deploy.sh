git reset HEAD --hard
git checkout master
git pull origin master

kill `cat tmp/server.pid`
nohup ./server.py > tmp/out.log 2> tmp/out.err < /dev/null &
echo $! > server.pid
