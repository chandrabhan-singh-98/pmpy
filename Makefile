PREFIX=/usr/local
BINDIR=$(PREFIX)/bin
OBIN=pmpy
CONF=config
CONFDIR=$(HOME)/.config/pm

all:
	@echo 'run make install to install'
package:
	rm -rf pmpy.tar.gz
	tar -zcvf pmpy.tar.gz *
install:
	install -Dm755 $(OBIN) $(BINDIR)/$(OBIN)
	install -D $(CONF) $(CONFDIR)/$(CONF)
	install -D bash-completion /usr/share/bash-completion/completions/pmpy

uninstall:
	rm -f $(BINDIR)/$(OBIN)
