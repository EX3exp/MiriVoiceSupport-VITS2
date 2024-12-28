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

IMAGE_NAME := teamcoda/vits
VERSION := $(MAJOR_VERSION).$(MINOR_VERSION).$(PATCH_VERSION)

.PHONY: all build tag run

all: build tag run

build:
	docker build -t $(IMAGE_NAME) .
tag:
	docker tag $(IMAGE_NAME) $(IMAGE_NAME):$(VERSION)
run:
	docker run --gpus all -it --rm --ipc=host \
			    -v $(pwd):/workspace \
			    -w /workspace \
				-p 6006:6006 \
				-p 7860:7860 \
				$(IMAGE_NAME):$(VERSION)

tensorboard:
	docker run --gpus all -it --rm --ipc=host \
			    -v $(pwd):/workspace \
			    -w /workspace \
				-p 6006:6006 \
				$(IMAGE_NAME):$(VERSION) tensorboard --logdir=/workspace/logs
