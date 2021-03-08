<!-- markdownlint-disable MD033 -->
<!-- markdownlint-disable MD034 -->
<!-- markdownlint-disable MD036 -->
# SPM-CLI

## The state of spm

Previous release:   **None**

LTS release:        **None**

Current release:    **None**

Next release:       v1.0.0-**alpha**

SPM is in development, we are yet to have a public release schedule.

Currently, the project is not able to take contributions- it is being used for a formal project.
~~Feel free to make contributions to the project!~~

## What is SPM

SPM is intended to be a unified package manager, allowing software previously unpublished on package managers, and ones already existing on other ones, to exist in one place.

No more browsing through git repositories, configuring 3rd party PPAs and installing package manager after package manager. I would happily bet half of you out there have pip and npm installed for random software you've previously installed, not even using the package managers for active development or other software.

SPM aims to bring everything into one, single, location.

## How to use SPM

### spm install

*Used to install new software*

The install command is utilised to install now software onto your machine.
The syntax is very simple.

`spm install [author/package]`

### spm remove

*Used to remove installed software*

The remove command is used to remove software installed on your machine.
It tracks installed packages via the local index<sup id="a1">[1](#f1)</sup>.

Unlike other package managers, for a proper removal of the software in the way the author wishes it to be removed, you will require an active internet connection.
SPM will connect to a package management server to pull software-specific removal instructions.

If this is not available, spm can also delete directores and files associated with the software.

`spm remove [author/package]`

### spm update (awaiting implementation)

*Used to update installed software- yet to be implemented*

The update command is used to update software installed on your machine.
It can only update software in your local index<sup id="a1">[1](#f1)</sup>.

Running this command will attempt to see if the author has specific update instructions, if not the software will simply run through the installation process again.

`spm update [author/package]`

### spm fetch

*Used to fetch package data from the remote server*

The fetch command is used to pull information about packages available on the remote server locally.

This command creates a remote index, this can be altered and restored at any time. You do not need this to be able to install packages.

You may also download the individual information for all packages on the remote server (--save), or a specific package (--save [author/package]).

`spm fetch <--save [author/package]>`

## Default remote servers

The public SPM index is available to publish at https://spm.visudo.tech', this is a moderated repository.
By default, when using spm, the configuration will default to this remote server (this server is SSL-enabled).  

### Publishing to the default servers

API documentation will be published soon.

### Package approval on the default servers

### Report a package

Contact `security@thatspretty.cool` with the following:

```email

To:         Security Ops <security@thatspretty.cool>
Subject:    Report on malicious package [author/package] version [version]
Body:
Hi there,
I wish to report [author/package], as it contains malicious code, or violates local law from the United Kingdom.

The reasoning behind my report is...

You [can/cannot] contact me for more information, and the result of this report.
Thank you.

```

### Start my own server

The backend we originally designed isn't too well optimised and implemented, a new version is being built which will be available to the public.

## Report an issue

You can enable verbose debug logging in spm by using the `-v` flag.
This flag will log verbose output to stdout, this can be used to see the actions leading up to the issue you're experiencing.

Open an Issue on the GitHub Repository site describing the issue, showing us the verbose output.

To log the output of spm to a file, and view the output, you can try the following.

```shell
spm [arguments...] 2>&1 | tee myLog
```

## Footnotes

<b id="f1">1</b> If this index is damaged, removed or rebuilt the remove command will not work on software installed prior to a new index being built. [↩](#a1)
