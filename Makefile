SHELL=/bin/bash

build-image:
	cd image; packer validate ami.json && packer build ami.json

deploy:
	aws cloudformation package \
		--template-file ./template.yaml \
		--s3-bucket $(ARTIFACTS_BUCKET) \
		--output-template-file ./packaged-template.yaml
	aws cloudformation deploy \
		--template-file ./packaged-template.yaml \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides InstanceTypeParam=$(INSTANCE_TYPE) \
				ImageIdParam=$(IMAGE_ID) \
				DurationParam=$(DURATION)

destroy:
	aws s3 rm s3://$(STACK_NAME)-results --recursive
	aws cloudformation delete-stack --stack-name $(STACK_NAME)
	aws ec2 deregister-image --image-id $(IMAGE_ID)
