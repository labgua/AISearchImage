
#### installer, compatible for python2.7 on Ubuntu (unix-compatible?)
#### based on : https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/

# 1) installing dependencies from requirements.txt
pip install -r requirements.txt

# 3) download WordNet data for nltk
#### https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet.zip
wget -O /tmp/wordnet.zip https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/wordnet.zip
mkdir nltk_data
mkdir nltk_data/corpora
unzip /tmp/wordnet.zip -d nltk_data/corpora

# 2) download InceptionV3 CNN Pre-trained
#### http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz
wget -O /tmp/inception-2015-12-05.tgz http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz
mkdir imagenet
tar -xvzf /tmp/inception-2015-12-05.tgz -C imagenet

# 4) installing opencv
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
unzip opencv.zip

wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
unzip opencv_contrib.zip

cd ~/opencv-3.1.0/
mkdir build
cd build


##### ATTENZIONE, aggiustare questo passo...
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
    -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
    -D BUILD_EXAMPLES=ON ..

make -j4
sudo make install
sudo ldconfig