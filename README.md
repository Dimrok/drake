# <img src="docs/static_files/drake_logotype@2x.png" alt="Logo - Drake" title="Drake logotype" width="300" style="max-width:300px;">

The well-formed build system.

[![pipeline status](https://gitlab.gruntech.org/mefyl/drake/badges/master/pipeline.svg)](https://gitlab.gruntech.org/mefyl/drake/commits/master)

## About

Drake is a build system written in Python3 that transforms a list of *source* nodes into a list of *target* nodes. Each target (or list of targets) is defined by a *builder* which takes a list of sources as its input. These targets can then be sources of other builders; resulting in a chain of dependencies. Drake resolves these chains to determine the build order and avoids rebuilding targets unnecessarily by hashing source and target files.

Its advantages include:
- Easily extensible using Python3
- Build any target without the need for rule specification
- Built in cross compiling capabilities

## Requirements

**Linux:**

If your distribution did not come with Python3 and *pip* for Python3, install them with your package manager. With a Debian based distribution (such as Ubuntu), this can be done as follows:
```bash
sudo apt-get install python3 python3-pip
```

**macOS:**

Python3 can be installed using [homebrew](http://brew.sh).
```bash
brew install python3
```

Drake requires *Python3* along with the following modules:
- [greenlet](https://pypi.python.org/pypi/greenlet) *(Micro-threads)*.
- [orderedset](https://pypi.python.org/pypi/orderedset) *(Set that remembers original insertion order)*.

Some builders require specific modules, such as:
- [mako](https://pypi.python.org/pypi/Mako) *(Templating)*.
- [mistune](https://pypi.python.org/pypi/mistune) *(Markdown parser)*.

Drake's requirements can be found in the root directory of this repository. To install them use:

```bash
pip3 install -r requirements.txt
```

## Basic structures of a drakefile and a Drake script

Consider the following hierarchy:
```bash
 .
 - build
(  - drake)
 - drakefile
```

The `drakefile`, located at **./drakefile**, contains the list of sources, targets, builders transforming sources to targets, etc.

```python3
import drake

def configure(arg1,
              arg2):
  # List sources
  # List targets
  # Declare builders
  print("got arg1: %s and arg2: %s" % (arg1, arg2))
```

If you have no special configuration, you can run Drake directly from **./build** (assuming Drake is installed at `/opt/drake`):
```
$ cd build
$ PYTHONPATH=/opt/drake/src /opt/drake/src/bin/drake .. --arg1="bob" --arg2="Hello world!"
got arg1: bob and arg2: Hello world!
...
```

Otherwise, the `Drake script`, located at **./build/drake** is the way to personalize your configuration.
```python3
#!/usr/bin/env python3
import drake

# ...

# Instantiate Drake to look for a drakefile at '../drakefile'.
path_to_the_drakefile_directory = '..'
with drake.Drake(path_to_the_drakefile_directory) as d:
  # Pass arguments to the drakefile configure function.
  d.run(
    arg1 = "example",
    arg2 = "Hello world!"
  )
```

With that structure, you can run (from `build`):
```
$ cd drake
$ ./drake --arg1="sample"
got arg1: sample and arg2: Hello world!
...
```

## Examples

### Hello World Example

This example shows how to build a simple executable from the C++ source file *hello_world.cc*.

See the [source directory](examples/hello_world).

The *drakefile* in the root describes the build process. Each platform in the *_build* directory has it's own *Drake* script which has some initial configuration.

To build the example project, we invoke the build *rule* as follows:
```bash
$> cd _build/<platform>
$> ./drake //build
./drake: Entering directory <current directory>
Compile hello_world.o
Link hello_world
./drake: Leaving directory <current directory>
```

The target could also be built by specifying its output path:
```bash
$> ./drake hello_world
...
```

The resulting executable can be found in the root of the build directory:
```bash
$> ./hello_world
Hello world
```

### User Libraries Example

In this example, a static and dynamic library are built from user sources.

See the [source directory](examples/user_libraries).

The drakefile shows how to build both a static and a dynamic library from user specified sources.

Once again, we build the example project by invoking the build rule:
```bash
$> cd _build/<platform>
$> ./drake //build
...
```

Any of the targets can be built individually by invoking Drake with their output path:
```bash
$> ./drake geometry/Shape.o
...
$> ./drake lib/libcolor.a
...
```

If you would like to see the underlying commands that Drake is launching, you can set the `DRAKE_RAW` environment variable:

```bash
$> DRAKE_RAW=1 ./drake //build
...
```

The resulting executable is in the *bin* directory and can be run as follows:
```bash
$> ./bin/colored_shape
...
```

### GNU Dependencies Example

This example is an executable that fetches the contents of *https://example.com*. To do this, we build our own cURL (which depends on zlib and OpenSSL) using Drake.

See the [source directory](examples/gnu_builder).

The drakefile shows how cURL, OpenSSL and zlib tarballs are fetched by Drake and built in the correct order so that our executable can be linked with cURL.

To build the project:
```bash
$> cd _build/<platform>
$> ./drake //build
...
```

To run the resulting executable:
```bash
$> ./bin/http_request
...
```

## Helpful Environment Variables

**DRAKE_RAW**

Setting `DRAKE_RAW=1` in your environment will cause Drake to output the raw commands that it calls to perform your build.

**DRAKE_DEBUG_BACKTRACE**

Setting `DRAKE_DEBUG_BACKTRACE=1` in your environment will cause Drake to output a backtrace if there is an issue with your build.
