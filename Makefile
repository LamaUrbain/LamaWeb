DATADIR := lamaweb/static/

setup: $(DATADIR)
	@ mkdir -p $(DATADIR)/ol
	@ wget http://openlayers.org/en/v3.1.1/build/ol.js -O $(DATADIR)/ol/ol.js
	@ bower install
	@ mkdir -p $(DATADIR)/css/
	@ lessc --compress $(DATADIR)less/style.less > $(DATADIR)css/style.css
