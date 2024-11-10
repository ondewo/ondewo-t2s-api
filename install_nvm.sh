export NVM_VERSION_DEFAULT=20.12.0

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install $NVM_VERSION_DEFAULT
nvm use $NVM_VERSION_DEFAULT
nvm alias default $NVM_VERSION_DEFAULT
