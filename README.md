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

# Install client-side dependencies & compile CSS
npm install bower
bower install
mkdir -p lamaweb/static/css/
lessc --compress lamaweb/static/less/style.less > lamaweb/static/css/style.css

# Launch server
pserve development.ini --reload
```
