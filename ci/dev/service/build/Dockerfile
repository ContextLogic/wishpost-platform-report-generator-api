FROM harbor.infra.wish-cn.com/wish/wish_flask/dev-base:latest AS service

USER app

ARG proj_name=report_generator_service
ARG proj_name_snake=report_generator_service
RUN mkdir -p /home/app/$proj_name

# We do not have clroot mounted in at build time so we have to copy these in to
# get the python dependencies loaded. An alternative would be to do the pip
# install when the container is started, but this would slow down container
# start time and it would be non-obvious when the container is ready. Also,
# this means we can bring the container up/down without installing pips, which
# is a better user experience as it is not required most of the time.
WORKDIR /home/app/$proj_name
COPY $proj_name_snake/requirements /home/app/$proj_name/requirements

# prior to pip run
ENV PYTHONDONTWRITEBYTECODE 1
ENV LC_ALL=C.UTF-8

# Note that docker will cache this, so this is only getting done once, until you remove
# all the cached layers..which is why we must do it again when we start the container. We
# do this here so that subsequent pip installs are faster. Periodically remove your
# old containers for a faster 'up'.
# Add "--use-deprecated=legacy-resolver" to resolve package version conflict.
RUN /home/app/virtualenv/bin/pip install --exists-action w -r /home/app/$proj_name/requirements/dev-requirements
RUN sudo rm -rf /home/app/$proj_name

ENV PYTHONPATH=/home/app/$proj_name

CMD ["/bin/bash", "-c", "echo Feel free to ctrl-c! Container will stick around. && while true ; do sleep 3600; done"]
