# Get OS type
os=""
case "$OSTYPE" in
  solaris*) os=SOLARIS ;;
  darwin*)  os=OSX ;;
  linux*)   os=LINUX ;;
  bsd*)     os=BSD ;;
  msys*)    os=WINDOWS ;;
  *)        os=unknown: $OSTYPE ;;
esac

if [[ "$os" == 'LINUX' ]]; then
    # Make a directory named venvs
    mkdir venvs
    # Install virtualenv
    pip3 install virtualenv --user
    # Create a virtualenv named test_venv
    virtualenv -p python3 venvs/test_venv
    # Activate the created env
    source venvs/test_venv/bin/activate
elif [[ "$os" == 'WINDOWS' ]]; then
    # Make a directory named venvs
    mkdir \venvs
    # Install virtualenv
    pip install virtualenv
    # Create a virtualenv named test_venv
    virtualenv \venvs\test_venv
    # Activate the created env
    \venvs\test_venv\Scripts\activate
fi

# Clone project from git
git clone https://github.com/tssovi/user-info.git

# Go to project directory
cd user-info

# Install required packages
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations

# Migrate database
python manage.py migrate

# Test projects
python manage.py test

# Run project
python manage.py runserver