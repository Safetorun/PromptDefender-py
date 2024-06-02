build:
	bash scripts/build.sh prompt_defender \
	bash scripts/build.sh prompt_defender_llm_defences

deploy_prod: build
	bash scripts/deploy.sh prompt_defender prod \
	bash scripts/deploy.sh prompt_defender_llm_defences prod

deploy_test: build
	bash scripts/deploy.sh prompt_defender test \
	bash scripts/deploy.sh prompt_defender_llm_defences test

test:
	bash scripts/tests.sh