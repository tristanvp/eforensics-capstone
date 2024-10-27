
# Foren6
Foren6 is an automated e-forensics system designed to facilitate forensic investigations on image files. This system streamlines usual forensic investigations, automating tasks such as file and drive hashing, finding carved files, suspicious artifacts, renamed files, and registry activities.

### OS
- Any Linux-based distribution (Kali Linux, Ubuntu 20.04+)

### Software, Dependencies, and Libraries
- Python 3.8 or higher
- Pytsk
- docxtpl
- filetype
- libewf_python
- pytsk3
- virtualenv


### Usage ###
Create a local project directory for project files
```bash
mkdir Foren6
```

### Virtual Environment Config ###
To ensure consistency when using Foren6, it is recommended to use virtualenv to create a virtual environment to actively avoid package inconsistency.

Install virtualenv packages
```bash
pip install virtualenv==20.21.1
```

Create a new environment 
```bash
virtualenv py3-env -p $(which python3.12)
```

Activate environment
```bash
source py3-env/bin/activate
```

CD into the project folder, and install the project repository using this command
```bash
git clone https://github.com/tristanvp/eforensics-capstone.git
```

Install all libraries, using:
```bash
pip install -r requirements.txt
```

Verify Installation and libraries
```bash
pip freeze
```

```bash
python3 --version
```

```bash
python3 main.py --help
```
