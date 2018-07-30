PREFIX=$(HOME)/.local
BINDIR=$(PREFIX)/bin
OBIN=pmpy
CONF=config
CONFDIR=$(HOME)/.config/pm

all:
	@echo 'run make install to install'
package:
	rm -rf pmpy.tar.gz
	tar -zcvf pmpy.tar.gz *
install-all:
	install -Dm755 $(OBIN) $(BINDIR)/$(OBIN)
	install -D $(CONF) $(CONFDIR)/$(CONF)
	install -D pmpy-bash-completion /usr/share/bash-completion/completions/pmpy
install-conf:
	install -D $(CONF) $(CONFDIR)/$(CONF)

install-bin:
	install -Dm755 $(OBIN) $(BINDIR)/$(OBIN)

uninstall:
	rm -f $(BINDIR)/$(OBIN)
