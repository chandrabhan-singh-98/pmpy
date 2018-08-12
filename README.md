# pmpy

## About

`pmpy` is a small python script to act as a a project status tracker and viewer.

## Usage

```
pmpy [-ildhv] [ -m active,inactive,abandoned,complete]
```

### Supported Options:

   `-i` :  Initialization process to populate project database

   `-d` : Delete the central database json file

   `-h` : Print usage help and all supported options

   `-v` : Print pmpy version info

   `-m [active,inactive,abandoned,complete]` : Set project status

   `-s` : Show detailed information of one or all projects

   `-l` : List names of all projects

### Configuration:

`pmpy` uses an INI style configuration file to store options such as project location
and VCS integration.

## Architecture:

`pmpy` uses simple JSON serialization to store information about projects and uses
deserialization when required to read it.The project can optionally provide VCS integration
given the appropriate dependent modules are installed.

(I am well aware of how bad the code quality is, however this project was written in a 
very short period and thus code performance and reliability was not of much significance
given the purpose of this project.
This script was originally intended to be used as a simply throwaway script to provide
an at-a-glance look at my projects.

## Installation:
Clone the repository and install using the following instructions

```
git clone https://github.com/canopeerus/pmpy
cd pmpy
make install
```

### Dependencies:
* `python3`

* `pygit2` (Optional)

## To-do

* ~~Implement list all projects option(`pmpy -l`)~~

* ~~Implement show individual project details(`pmpy -s`)~~

* Implement update database option(`pmpy -u`)

## License
[LICENSE](./LICENSE)
