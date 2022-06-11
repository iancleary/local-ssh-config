# New-Component

[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![ci](https://github.com/iancleary/new-component/workflows/ci/badge.svg)](https://github.com/iancleary/new-component/actions/workflows/ci.yml)

Ian Cleary ([iancleary](https://github.com/iancleary))

## Description

**Welcome!** This is a CLI for creating [styled-components](https://styled-components.com) for React projects quickly.

> Note: I've rewrote Josh W Comeau's [new-component](https://www.npmjs.com/package/new-component) NPM package in Python 🐍 and adapted it to my preferences. It is an excellent project and you should check it out!

I didn't understand styled components at first. At the time of this writing, I'm looking to develop my understanding of CSS, upon the advice of Josh W Comeau's blog post "[The styled-components Happy Path
](https://www.joshwcomeau.com/css/styled-components/)".

After you read that article, you'll gather that this CLI aims to combine the wisdom of Josh's templates with my personal preferences.

-   Adding the `import styled from "styled-components"` in the new `component.js` file.
-   Adding a `styled.Wrapper` component definition (and making it .the parent html element in the React Component's `render` function)

## Quickstart

```sh
❯ pipx install new-component
❯ new-component --help
```

That will output the following:

```
Usage: vmsshconfig [OPTIONS] NAME

  Creates an new component directory in a React project, with opinionated
  defaults for styled-components.

  See https://styled-components.com/ for more information.

Arguments:
  NAME  Name of component to create.  [required]

Options:
  -d, --directory TEXT  The directory in which to create the component.
                        [default: src/components/]
  -e, --extension TEXT  The file extension for the created component files.
                        [default: js]
  -v, --version         Show the application's version and exit.
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.
```

## Example Usage

The first and only argument is the name of the component to create.

```bash
❯ new-component Backdrop
Created a new Backdrop Component 💅 🚀!
/Users/iancleary/Personal/new-component/src/components/Test4
```

The path printed is the absolute path to new component folder.

> It will very based upon your setup!

This command created two files:

`src/components/Backdrop/index.js`
`src/components/Backdrop/Backdrop.js`

The contents of the files will be as follows:

```js
// `src/components/Backdrop/index.js`
export { default } from "./Backdrop";
```

```js
// `src/components/Backdrop/Backdrop.js`
import React from "react";
import styled from "styled-components";

const Backdrop = ({children}) => {
  return (
    <Wrapper>
      {children}
    </Wrapper>
  )
};

const Wrapper = styled.div`
    /* CSS Goes Here */
`;

export default Backdrop;
```

## Configuration

Configuration can be done through 3 different ways:

* Creating a global `settings.json` in your home directory (`~/.config/new-component/settings.json`).
* Creating a local `.new-component-config.json` in your project's root directory.
* Command-line arguments.

The resulting values are merged, with command-line values overwriting local values, and local values overwriting global ones.

## API Reference

### Directory

Controls the desired directory for the created component. Defaults to src/components

Usage:

Command line: `--directory <value>` or `-d <value>`

JSON config: `{ "directory": <value> }`

### File Extension

Controls the file extension for the created components. Can be either js (default) or jsx.

Usage:

Command line: `--extension <value> or -e <value>`

JSON config: `{ "extension": <value> }`

## Further information

> I will likely evolve this CLI as I learn more; I'm on my way 😊

-   Add different component types
-   Promote better patterns to ensure CSS (single source of styles, Isolated CSS)

Thanks to Josh W Comeau's blog post "[The styled-components Happy Path
](https://www.joshwcomeau.com/css/styled-components/) for starting my education! Again, it puts this README in perspective.

**Enjoy quickly creating styled components 💅 🚀!**

## Contributing

I created this CLI for my opinionated uses and may not accept changes.

See [CONTRIBUTING.md](.github/CONTRIBUTING.md).
