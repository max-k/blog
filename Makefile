PY=python
VENV=virtualenv2
FLASK_MANAGER=engine.py
BASEDIR=$(CURDIR)
OUTPUTDIR=$(BASEDIR)/build

SSH_HOST=ssl-offloader.max-k.org
SSH_PORT=443
SSH_USER=www-data
SSH_TARGET_DIR=/srv/http/blog

help:
	@echo 'Makefile for Flask FlatPages/Frozen static blog'
	@echo ''
	@echo 'Usage :'
	@echo 'make dev            (re)generate static webpages using dev env'
	@echo 'make prod           (re)generate static webpages using prod env'
	@echo 'make test           open development html files in xombrero'
	@echo 'make push           push production html files using rsync'
	@echo 'make environment    deploy development environment'

serve:
	. env/bin/activate; \
        $(PY) $(FLASK_MANAGER) serve; \
        deactivate

dev:
	. env/bin/activate; \
        $(PY) $(FLASK_MANAGER) build; \
        deactivate

prod:
	. env/bin/activate; \
        FLASK_MODE='production' $(PY) $(FLASK_MANAGER) build; \
        deactivate

test: dev
	xombrero $(OUTPUTDIR)/index.html

push: prod
	rsync -e "ssh -p $(SSH_PORT)" -P -rvz --delete \
	$(OUTPUTDIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR) --cvs-exclude

virtualenv:
	$(VENV) --no-site-package $(BASEDIR)/env

del-environment:
	rm -rf $(BASEDIR)/env

environment: del-environment virtualenv
	. env/bin/activate; pip install -Ur requirements.txt; deactivate

