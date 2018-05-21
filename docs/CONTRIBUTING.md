# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/spbrien/mir/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

Mir Framework could always use more documentation, whether as part of the
official Mir Framework docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/spbrien/mir/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `mir` for local development.

---

Clone the repo and install it as a python package in development mode:

```bash
git clone https://github.com/spbrien/mir.git
pip install -e ./mir
```

* The core application (which imports/registers all project-specific code and other python modules) is in `mir/mir.py`
* The CLI tool is in `mir/cli.py`
* The source code for the Admin UI is in `admin/src`

### Working on the API core files

In a separate directory, scaffold out and run a new Mir project:

```bash
mir init test_project
cd test_project
mir dev
```

Once you have a running Mir instance, you can update core files and see your changes in the running instance. Due to the way Mir dynamically imports python modules from project-specific code, many changes require manually restarting the development server:

```bash
ctrl + c
mir dev
```

### Working on the Admin UI

In a separate testing directory, scaffold out and run a new Mir project:

```bash
mir init test_project
cd test_project
mir dev
```

In your main Mir directory, change to the admin application folder and start a dev server:

```bash
cd admin
npm run dev
```

This starts a frontend development server for the Admin Vue application at http://localhost:8081

To build your changes into the running mir instance, run `npm run build` and restart the mir dev server from the testing directory. For the Admin UI, build files should be committed to the Mir package repo.
