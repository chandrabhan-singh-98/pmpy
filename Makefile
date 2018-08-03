PREFIX=/usr/local
BINDIR=$(PREFIX)/bin
OBIN=pmpy
SRC=pm.py
CONF=config
CONFDIR=$(HOME)/.config/pm

all:
	@echo 'run make install to install'
package:
	rm -rf pmpy.tar.gz
	tar -zcvf pmpy.tar.gz *
install:
	install -Dm755 $(SRC) $(BINDIR)/$(OBIN)
	install -D $(CONF) $(CONFDIR)/$(CONF)

uninstall:
	rm -f $(BINDIR)/$(OBIN)
