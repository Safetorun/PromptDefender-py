build:
	bash scripts/build.sh prompt_defender &&\
	bash scripts/build.sh prompt_defender_llm_defences &&\
	bash scripts/build.sh prompt_defender_aws_defences

deploy_prod: build
	bash scripts/deploy.sh prompt_defender prod &&\
	bash scripts/deploy.sh prompt_defender_llm_defences prod &&\
	bash scripts/deploy.sh prompt_defender_aws_defences prod

deploy_test: build
	bash scripts/deploy.sh prompt_defender test &&\
	bash scripts/deploy.sh prompt_defender_llm_defences test &&\
	bash scripts/deploy.sh prompt_defender_aws_defences test

test:
	bash scripts/tests.sh

set_version:
	bash scripts/update_versions.sh

docs:
	bash scripts/generate_documentation.sh prompt_defender &&\
	bash scripts/generate_documentation.sh prompt_defender_llm_defences &&\
	bash scripts/generate_documentation.sh prompt_defender_aws_defences