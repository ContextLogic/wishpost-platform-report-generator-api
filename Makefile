
local-service:
	FLASK_ENV=dev NEED_REGISTER=True python3 report_generator_service/server.py

local-dbshell:
	FLASK_ENV=dev python3 report_generator_service/shell.py

container-up:
	dev report-generator-service up

container-service:
	dev report-generator-service sh FLASK_ENV=dev NEED_REGISTER=True python report_generator_service/server.py

