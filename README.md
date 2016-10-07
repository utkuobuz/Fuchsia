# Fuchsia

Pink + Purple == Fuchsia (a new Operating System)

Welcome to Fuchsia! This is a top-level entry point for the project. From here
we try to link to everything you need to get started, use, and develop for
Fuchsia.

## Getting the source

The Fuchsia project is in many Git repositories and we use the jiri tool to make
it easier to work with these repositories. jiri uses manifest files to know what
repositories to pull. Visit the 'manifest' project to find out how to
[check out the source](https://fuchsia.googlesource.com/manifest/+/HEAD/README.md).

## Building Fuchsia

### Build Magenta and [optional] QEMU

First, follow Magenta's
[instructions](https://fuchsia.googlesource.com/magenta/+/master/docs/getting_started.md#Preparing-the-build-environment)
from "Preparing the build environment" up through "Build Magenta". It isn't
necessary to check out the Magenta and QEMU sources, they are included in the
Fuchsia manifest. Note, building QEMU isn't strictly required if you're only
developing on actual hardware, but it is a good tool to have at the ready.

### Build a sysroot

Next, you need to build a sysroot:

```
./scripts/build-sysroot.sh -c -t x86_64
```

### Build Fuchsia

Finally, you can build Fuchsia using these commands:

```
./packages/gn/gen.py
./buildtools/ninja -C out/debug-x86-64
```

[Googlers only] If you have goma installed, use these alternative commands for faster builds:

```
./packages/gn/gen.py --goma
./buildtools/ninja -j1000 -C out/debug-x86-64
```

The gen.py script takes an optional parameter '--target\_cpu' to set the target
architecture. If not supplied, it defaults to x86-64.

```
./packages/gn/gen.py --target_cpu=aarch64
./buildtools/ninja -C out/debug-aarch64
```

You can configure the set of modules that `gen.py` uses with the `--modules`
argument. After running `gen.py` once, you can do incremental builds using
`ninja`.

### Running Fuchsia

These commands will create an `out/debug-{arch}/user.bootfs` file. To run the
system with this filesystem attached in QEMU, pass the user.bootfs path as the
value of the '-x' parameter in Magenta's start command script, for example:

```
cd magenta
./scripts/run-magenta-x86-64 -x ../out/debug-x86-64/user.bootfs
./scripts/run-magenta-arm64 -x ../out/debug-aarch64/user.bootfs
```

If you want a graphical console, add the `-g` flag.

Then, when Fuchsia has booted and started an MXCONSOLE, you can run programs!

For example, to receive deep wisdom, run:

```
fortune
```

## Additional helpful documents
If you're contributing changes, visit the 'manifest' repository
[documentation](https://fuchsia.googlesource.com/manifest/+/HEAD/README.md#Submitting-changes)
for more information about submitting changes.
