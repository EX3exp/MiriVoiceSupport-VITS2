ifeq ($(OS),Windows_NT)
	is_windows := true
	pwd := $(shell powershell -Command "(Get-Location).Path")
else
	is_windows := false
	pwd := $(PWD)
endif

MAJOR_VERSION := 0
MINOR_VERSION := 0
PATCH_VERSION := 1

VERSION := $(MAJOR_VERSION).$(MINOR_VERSION).$(PATCH_VERSION)

.PHONY: all build tag run

all: build tag run

build:
	docker build -t mirivoice/vits .
tag:
	docker tag mirivoice/vits mirivoice/vits:$(VERSION)
run:
	docker run --gpus all -it --rm --ipc=host \
			    -v $(pwd):/workspace \
			    -w /workspace \
				-p 6006:6006 \
				-p 7860:7860 \
				mirivoice/vits:$(VERSION)

tensorboard:
	docker run --gpus all -it --rm --ipc=host \
			    -v $(pwd):/workspace \
			    -w /workspace \
				-p 6006:6006 \
				mirivoice/vits:$(VERSION) tensorboard --logdir=/workspace/logs
