Getting Started
---------------

```shell
# Clone the repo
git clone https://github.com/LamaUrbain/LamaWeb.git
cd LamaWeb

# Create a virtualenv to isolate the package dependencies locally
virtualenv env
source env/bin/activate

# Install dependencies
python setup.py develop

# Install open layers
wget http://openlayers.org/en/v3.1.1/build/ol.js -O lamaweb/static/js/ol.js

# Install client-side dependencies & compile CSS
npm install bower
bower install
mkdir -p lamaweb/static/css/
lessc --compress lamaweb/static/less/style.less > lamaweb/static/css/style.css

# Launch server
pserve development.ini --reload
```
