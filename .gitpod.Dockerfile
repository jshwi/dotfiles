FROM gitpod/workspace-full

USER gitpod

# Install custom tools, runtime, etc. using apt-get
# For example, the command below would install "bastet" - a command line tetris clone:
RUN sudo apt update
RUN sudo install -y zsh
RUN sudo apt clean
RUN sudo rm -rf /var/cache/apt/* /var/lib/apt/lists/*

# More information: https://www.gitpod.io/docs/42_config_docker/