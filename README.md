

# Welcome to PINGIT [![Build Status](https://www.travis-ci.org/EMS-TU-Ilmenau/PINGIT.svg?branch=master)](https://www.travis-ci.org/EMS-TU-Ilmenau/PINGIT) [![Version](https://img.shields.io/pypi/v/PINGIT.svg)](https://pypi.python.org/pypi/PINGIT)
## A batch management tool for multiple nested git repositories
[![License](https://img.shields.io/pypi/l/PINGIT.svg)](https://pypi.python.org/pypi/PINGIT) [![Python versions](https://img.shields.io/pypi/pyversions/PINGIT.svg)](https://pypi.python.org/pypi/PINGIT) [![Implementation](https://img.shields.io/pypi/implementation/PINGIT.svg)](https://pypi.python.org/pypi/PINGIT) [![Status](https://img.shields.io/pypi/status/PINGIT.svg)](https://pypi.python.org/pypi/PINGIT)

PINGIT is not a git indexing tool. Instead it offers a command-line interface
for managing multiple git repositories nested in a hierarchic directory structure.

# Description
PINGIT generates an index of all git repositories and their directory
structure of the current working directory and works with it.

Currently PINGIT supports:
 - Export and import (batch-clone) the directory structure
 - List the directory structure
 - Ping, fetch and pull the remotes of all repos within that structure
 - Show the status of all repos within that structure
 - Archive all repos within that structure (for backup purposes)

Pingit is written in Python and supports Python2 and Python3 since
Python 2.7+

## Installation
PINGIT can be installed simply by running `pip install pingit` from your
favorite python-powered Linux/*nix/Windows shell. It comes with no importable
package but a command-line tool

## Dependencies
- gitpython
- arghandler


# Motivation, Usage and Examples
If you happen to use git intensively for a wide range of projects you sooner or
later find yourself having the need to comfortably deal with a large number of
git repositories, often embedded into an more-or-less hierarchical directory
structure.

PINGIT is the tool that aims at reliefing some pain for some common tasks that
more-or-less regularly hit your task schedule. The following sections introduce
some of them and show how to handle them conveniently.

Please let me know if you have other examples of how PINGIT could be of help
that are worth mentioning (contact the author) or if you have something in mind
where PINGIT could be of help but is currently lacking a feature or two (issue
section or pull request) . Any help, feedback or contribution is happily
appreciated. Thank you!

## A few words on git repository organization
Based on the fact that the common git repository services (github, gitlab, ...)
are organized hierarchically it is a common pattern that clones repositories
often reflect this hierarchy to some degree. You may easily find yourself
arranging the cloned repositories in a subdirectory called `git` or something
alike, effectively reproducing the structure of the service itself. Some users
choose subdirectories for different services, some for different users and
again some users tend to build large tree-like structures of groups and
subgroups. What scheme you are running depends heavily on the way you or your
organization works but as soon as you have more than a few repositories you
work with often, or even manage, some kind of structure is inevitable.

Following some of the (quite often annoying) tasks are presented that in the
past required repetitive manual work to resolve, that ultimatively resulted in
the creation of PINGIT. Each task comes with a usage example.

## Is there unpublished or git-unrelated stuff in my git collection?
Each successful backup scheme relies on scrupulous checking of violations --
that in the worst case may lead to data loss in case of a failure requiring the
fall-back of one of the backups.

Often larger collections of git repositories are arranged in a directory named
`git` or something alike. The assumption that everything inside this git
repository collection container is already taken care of by the repository
servers leads to the exclusion of it from your scheduled local backup runs to
relief it a bit. However, this is quite dangerous if you have no means to make
sure that you never put anything else inside it by accident and left it there.

PINGIT warns if it encounters directories not containing git repositories every
time it scans a directory tree. Further, if it identifies files outside such a
directory that are unbeknownst to any git repositories, these files will also
be reported. If your intention is to identify such dangers of leftover files it
is advised to use `pingit status` as it will also report if you have some
repositories with dirty stage-areas, untracked files or simply unpublished
commits.

Equally dangerous is the case where you compose all of your commits but simply
forget to publish by pushing them. `pingit status` also reports this case.
However, please note that the presence of `.gitignore`-d files will not be
reported.

    nutzer@dev:~/Git/github$ pingit status
    WARNING:root:No git repositories found in ~/Git/github/foo-data
    WARNING:root:Files outside a git repository in ~/Git/github.
    WARNING:root:PINGIT <master> (1 untracked files) contains uncommited stages (dirty)
    WARNING:root:chefkoch <master>  contains uncommited stages (dirty)
    WARNING:root:fastmat <circulant-merge>  is ahead of origin by 1 commits
    WARNING:root:fastmat <circulant-merge>  contains uncommited stages (dirty)
    nutzer@dev:~/Git/github$


NOTE: Repositories that are up-to-date and require no attention do not produce
      console output unless the `--verbose` option is provided. In the above
      case the output with `--verbose` would be:

    nutzer@dev:~/Git/github$ pingit status -v
    WARNING:root:No git repositories found in ~/Git/github/foo-data
    INFO:root:EuroSciPy2018 <master>  OK.
    INFO:root:HX3 <master>  OK.
    WARNING:root:PINGIT <master> (1 untracked files) contains uncommited stages (dirty)
    WARNING:root:chefkoch <master>  contains uncommited stages (dirty)
    WARNING:root:fastmat <circulant-merge>  is ahead of origin by 1 commits
    WARNING:root:fastmat <circulant-merge>  contains uncommited stages (dirty)
    nutzer@dev:~/Git/github$


## Assisting the backup process of your git repositories

    *Backups are like insurances -- you hope you never need it, but if you do,
    you are happy if you're fully covered.*

Following that common phrase it is of good practice to automate the backup
process as much as possible, always following the other phrase: *better safe
than sorry*.

PINGIT helps by archiving every git repository inside your git collection
container directory and storing it into a single backup folder as one single
file per repository, still containing the relative path information within your
git collection container and -- of course -- the full git repository. This
allows you to selectively roll back single repositories.

By default a timestamp will be added included into the archive filename, but
you may choose to disable this behaviour with the `--no-timestamp` option.

    nutzer@dev:~/Git/github$ pingit archive -o ~/backup
    WARNING:root:No git repositories found in ~/Git/github/foo-data
    INFO:root:Archiving EuroSciPy2018 to ~/backup/2019-01-10__18-15-28__EuroSciPy2018
    INFO:root:Archiving HX3 to ~/backup/2019-01-10__18-15-28__HX3
    INFO:root:Archiving PINGIT to ~/backup/2019-01-10__18-16-04__PINGIT
    INFO:root:Archiving chefkoch to ~/backup/2019-01-10__18-16-05__chefkoch
    INFO:root:Archiving fastmat to ~/backup/2019-01-10__18-16-06__fastmat
    nutzer@dev:~/Git/github$ ls -sh1 ~/backup
    insgesamt 471M
     20K 2019-01-10__18-15-28__EuroSciPy2018.tar.gz
    355M 2019-01-10__18-15-28__HX3.tar.gz
     64K 2019-01-10__18-16-04__PINGIT.tar.gz
    280K 2019-01-10__18-16-05__chefkoch.tar.gz
    116M 2019-01-10__18-16-06__fastmat.tar.gz
    nutzer@dev:~/Git/github$


## Migrating your git collection to a new machine
Hauling git repositories is either copying your local git collection container
directory to another location or even another machine (including all build
leftovers or dirty states) or resembling the structure of your local git
collection container manually by selective cloning the required repositories.

An alternative poses the combination of `pingit export` / `pingit import`, that
exports your local git collection to a description file which can be shared,
moved or copied for rebuilding it somewhere else:

     alice@foo:~/Git/github$ pingit export -i desc.json
     alice@foo:~/Git/github$


     bob@bar:/tmp$ pingit import -i desc.json
     INFO:root:Cloning EuroSciPy2018 from https://github.com/ChristophWWagner/python-modelling to /tmp/EuroSciPy2018
     INFO:root:Cloning HX3 from https://github.com/keyboardpartner/HX3 to /tmp/HX3
     INFO:root:Cloning PINGIT from https://github.com/EMS-TU-Ilmenau/PINGIT.git to /tmp/PINGIT
     INFO:root:Cloning chefkoch from http://github.com/EMS-TU-Ilmenau/chefkoch to /tmp/chefkoch
     INFO:root:Cloning fastmat from https://github.com/EMS-TU-Ilmenau/fastmat.git to /tmp/fastmat
     bob@bar:/tmp$


With some shell-plumbing this can also be achieved in a one-liner to retrieve
a clean checkout of your git collection in one flush:

      nutzer@dev:~/Git/github$ pingit export | pingit import -o /tmp/clean

NOTE: Currently, only multiple remote specifications are preserved and not the
      full local repository configuration.


## Finding dead remotes
When your repository server moves you often end up with git remotes pointing
to unavailable locations. You may identify such situation using `pingit ping`,
can be thought of as a kind of batch-`git ls-remote`. Every remote that could
unresponsive remote will be reported and can be adjusted manually using `git`.

In cases where you can define a regular expression pattern to resolve the issue
you can migrate all your remotes at once by combining `pingit` and `sed`:

    pingit export | sed -e 's_oldserver.somewhere.xyz_newserver.somewhere.abc_g' | pingit import -o new_location

NOTE: This provides you with a clean clone into `new_location` and might
      result in the loss of special git repository configuration


## Update your complete git collection in one flush
If you work on multiple machines you might encounter the case where you sit
before a git repository collection that has not been updated in a while.
Batch-fetching or Batch-pulling can be achieved easily with PINGIT:

    nutzer@dev:~/Git/github$ pingit fetch
    INFO:root:Fetching from EuroSciPy2018:origin
    INFO:root:Fetching from HX3:origin origin/master
    INFO:root:Fetching from PINGIT:originigin/master
    INFO:root:Fetching from chefkoch:originin/master
    INFO:root:Fetching from fastmat:origin       -> origin/stable
    nutzer@dev:~/Git/github$


Alternatively, you may choose to pull or rebase-pull directly:

    nutzer@dev:~/Git/github$ pingit pull
    nutzer@dev:~/Git/github$ pingit pull --rebase


NOTE: If pulling fails this will be expressed with an error. Currently, you
      need to manually resolve the issue using git.

# Usage
PINGIT applies a subcommand architecture, quite comparable to git. Many
subcommands match those already known from git, although some exist that are
not related to any existing git functionaliy.

The common usage is:

    $ pingit <subcommand> <arguments>


For detailed description of any subcommands exact synctax please refer to the
command line help, which is available via

    $ pingit <subcommand> -h


The following general command line switches are available for most if not all
subcommands:

|    | Option    | Description                                              |
|----|-----------|----------------------------------------------------------|
| -p | --path    | Use different base path than current directory.          |
| -i | --input   | Read input from file instead of reading from STDIN.      |
| -o | --output  | Write output to file instead of writing to STDOUT.       |
| -o | --output  | Write output to a different than the current directory.  |
| -l | --list    | Instead of a recursive search for repos, take this list. |
| -v | --verbose | Increase verbosity of output. (Also report infos)        |
|    | --logging | Choose output verbosity level. (silence output a bit)    |

You may choose <subcommand> from the list composed of the following subsection
titles:

## export
**Generate a description of a directory containing nested git repositories.**
The resulting directory structure description originates at the given base path
and is formatted as json file. Use `import` to reproduce the repository
structure from this description.

Accepts the `--path` and `--output` command line options as defined above.

## import
**Clone a git repo tree from a description file (as produced by `export`).**

Accepts the `--path`, `--input` and `--verbose` command line options as defined
above.

## list
**List all git repos in the current or a given path.**
You may use the produced list (either as-is or reduced afterwards) to control
the repository selection the following commands are applied to.

Accepts the `--path` and `--output` command line options as defined above.

## ping
**Ping the remotes of all git repos and report issues.**
All urls for all remotes of the (selected) git repositories will be tried
using `git ls-remote`.

Accepts the `--path`, `--list` and `--verbose` command line options as defined
above.

## fetch
**Fetch changes in upstream from all git repos.**

Accepts the `--path`, `--list` and `--verbose` command line options as defined
above.

## status
**Show status of all git repos.**
The following conditions will be tested for all remotes of all (selected) git
repositories:
 * what is the active branch?
 * Are there untracked files?
 * Are there uncommitted changes?
 * Are there unpublished/unfetched changes? i.e. Is there a remote the local
   repository is ahead/behind of?
 * Is the repository bare or does not contain any commits?

Accepts the `--path`, `--list` and `--verbose` command line options as defined
above.

## pull
**Pull upstream of all git repos.**

Accepts the `--path`, `--list` and `--verbose` command line options as defined
above. Further, you may select to apply the rebase strategy with the `--rebase`
command line option instead of the default strategy (merge or as set in the
repository configuration).

## archive
**Archive all git repositories.**
Each of the (selected) git repositories will be packed into an archive format
of your choice and written to the current working directory or the path
specified by `--output`. The filename will by default be composed from a
timestamp (YYYY-MM-DD and HH-MM-SS) and the pathspec of the repository relative
to the selected basepath (current working directory or `--path` option).
However, you may decide to skip the timestamp if you like. Path delimiters in
the relative path portion of the filename will be replaced by the separation
character sequence given in `--sep` (defaults to `__`). The same sequence will
also be used to separate the timestamps, if activated.

Accepts the `--path`, `--list`, `--output` and `--verbose` command line options
as defined above. Also accepts the following options:

| Option         | Description                                    |
|----------------|------------------------------------------------|
| --sep          | Token separator for archive name composition.  |
| --format       | Archive output format.                         |
| --no-timestamp | Do not include timestamps in archive filename. |

## version
Report the version of the PINGIT.

# Contributing
Please feel free to fork this repository and feed back your changes via
pull-request.

## Issues
If you experience problems or missing a feature please feel free to open an
issue at our github project page: http://github.com/EMS-TU-Ilmenau/PINGIT.

## Contact the Author
Pingit was developed by Christoph Wagner at the EMS Research Group, Institute
for Information Technology, Technische Universität Ilmenau. Please check out
https://www.tu-ilmenau.de/it-ems/ or contact the author via Mail on
christoph.wagner@tu-ilmenau.de
