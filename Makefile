PROJECT=yace-sea-lang
AUX_PATH=auxi

ifeq ($(PLATFORM_ID),Windows)
else
PLATFORM_ID = $$( uname -s )
endif
PLATFORM = $$( \
	case $(PLATFORM_ID) in \
		( Linux | FreeBSD | OpenBSD | NetBSD | Windows | Darwin ) echo $(PLATFORM_ID) ;; \
		( * ) echo Unrecognized ;; \
	esac)

define default-help
# invoke: 'make uninstall', 'make install'
endef
.PHONY: default
default: help

define all-help
# Do all: clean uninstall build install
endef
.PHONY: all
all: uninstall clean build install example docs

define docker-help
# drop into a docker instance with the repository bind-mounted at /tmp/sea-lang
endef
.PHONY: docker
docker:
	@echo "## ${PROJECT}: docker"
	@docker run -it -w /tmp/${PROJECT} --mount type=bind,source="$(shell pwd)",target=/tmp/${PROJECT} debian:bookworm bash
	@echo "## ${PROJECT}: docker [DONE]"

define build-help
# Build the package (source distribution package)
endef
.PHONY: build
build:
	@echo "## ${PROJECT}: make build"
	@python3 -m build -n
	@echo "## ${PROJECT}: make build [DONE]"

define install-help
# install using pipx
endef
.PHONY: install
install:
	@echo "## ${PROJECT}: make install"
	@pipx install dist/*.tar.gz
	@echo "## ${PROJECT}: make install [DONE]"

define uninstall-help
# uninstall via pipx
endef
.PHONY: uninstall
uninstall:
	@echo "## ${PROJECT}: make uninstall"
	@pipx uninstall ${PROJECT} || echo "Cannot uninstall => That is OK"
	@echo "## ${PROJECT}: make uninstall [DONE]"

define clean-help
# clean build artifacts (build, dist, output)
endef
.PHONY: clean
clean:
	rm -r build || true
	rm -r dist || true
	rm -r output || true

define example-help
# Run using the example for struct
endef
.PHONY: example
example:
	slang examples/yall.h

define release-build-help
# Produce Python distribution (sdist, bdist_wheel)
endef
.PHONY: release-build
release-build:
	python3 -m build --sdist --wheel

define release-upload-help
# Upload Python distribution (sdist, bdist_wheel)
endef
.PHONY: release-upload
release-upload:
	twine upload dist/* --verbose

define release-upload-help
# Produce + Upload Python distribution (sdist, bdist_wheel)
endef
.PHONY: release
release: clean release-build release-upload
	@echo -n "# rel: "; date

define format-help
# run code format (style, code-conventions and language-integrity) on staged changes
endef
.PHONY: format
format:
	@echo "## ${PROJECT}: format"
	@pre-commit run
	@echo "## ${PROJECT}: format [DONE]"

define format-all-help
# run code format (style, code-conventions and language-integrity) on all files
endef
.PHONY: format-all
format-all:
	@echo "## ${PROJECT}: format-all"
	@pre-commit run --all-files
	@echo "## ${PROJECT}: format-all [DONE]"

define bump-help
# run code format (style, code-conventions and language-integrity) on all files
endef
.PHONY: bump
bump:
	@echo "## ${PROJECT}: bump"
	@./$(AUX_PATH)/bump.py
	@echo "## ${PROJECT}: bump [DONE]"

define help-help
# Print the description of every target
endef
.PHONY: help
help:
	@./$(AUX_PATH)/mkhelp.py --repos .
