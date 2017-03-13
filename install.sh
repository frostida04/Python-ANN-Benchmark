apt-get update
apt-get install -y python-numpy python-scipy python-pip python-nose build-essential software-properties-common unzip

apt-get install -y libboost1.58-all-dev
apt-get autoremove -y

pip install scikit-learn

cd install
for fn in lib-*.sh panns.sh nearpy.sh falconn.sh
do
  source $fn
done
