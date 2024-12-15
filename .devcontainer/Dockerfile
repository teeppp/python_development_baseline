FROM python:3.12-slim

# install UV
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

RUN apt-get update -y && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Install Docker cli
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN apt-get update -y && apt-get install -y \
    zip unzip \
    sudo \
    graphviz graphviz-dev git \
    docker-ce docker-ce-cli containerd.io docker-compose-plugin
# Install aws cli
# See https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install --update