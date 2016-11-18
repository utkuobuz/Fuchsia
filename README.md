# Fuchsia

Pink + Purple == Fuchsia (a new Operating System)

Welcome to Fuchsia! This is a top-level entry point for the project. From here
we try to link to everything you need to get started, use, and develop for
Fuchsia.

## Getting the source
Get the Fuchsia source by following these two steps and then return to this document:
  * [Install prerequisites](https://fuchsia.googlesource.com/manifest/+/HEAD/README.md#Prerequisites) for Jiri, a tool for multi-repo development.
  * [Create a new checkout](https://fuchsia.googlesource.com/manifest/+/HEAD/README.md#Creating-a-new-checkout) of Fuchsia.

## Prerequisites

### Magenta Prerequisites

The Fuchsia source  includes [Magenta](https://fuchsia.googlesource.com/magenta), the core platform which underpins Fuchsia. Follow this step to install the Magenta build prerequisites and then return to this document:

* [Preparing the Magenta build environment](https://fuchsia.googlesource.com/magenta/+/master/docs/getting_started.md#Preparing-the-build-environment).

### [Googlers only] Goma

Ensure `goma` is installed on your machine for faster builds.

## Build Fuchsia
### Setup Build Environment

Source the `env.sh` script, which provides helpful shell functions for Fuchsia development. The following command also changes the command prompt and sets up for a x86-64 build.

```
source scripts/env.sh && envprompt && fset x86-64
```

Run `envhelp` to see other useful shell functions, and `envhelp <function>` for specific usage information.

[optional] You might find it useful to add a shell function `fuchsia` as a shortcut to setup the build environment. For that, add this your shell startup script (e.g. `~/.bashrc`):

```
export FUCHSIA_ROOT=/path/to/my/fuchsia/source
function fuchsia() {
  source $FUCHSIA_ROOT/scripts/env.sh && envprompt && fgo && fset x86-64 "$@"
}
```


### [optional] Customize Build Environment

By default you will get a x86-64 debug build, and you can skip this step unless you want something else.

[Googlers only: If you have `goma` installed, it will also be used by default. Prefer `goma` over `ccache`]

Run `fset-usage` to see a list of build options. Some examples:

```
fset x86-64           # x86-64 debug build, no goma, no ccache
fset arm64            # arm64 debug build, no goma, no ccache
fset x86-64 --release # x86-64 release build, no goma, no ccache
fset x86-64 --ccache  # x86-64 debug build, ccache enabled
```

Note: to use `ccache` or `goma` you must install them first.

### Build Fuchsia

Once you have setup your build environment, simply run:
```
fbuild
```

This builds Magenta, the sysroot, and the default Fuchsia build.

### Run Fuchsia in QEMU

After Fuchsia is built, you will have a Magenta (`magenta.bin`) image and a `user.bootfs` file in `out/debug-{arch}/`.

To run Magenta with `user.bootfs` attached in QEMU:


* Build and install Fuchsia's fork of [QEMU](https://fuchsia.googlesource.com/magenta/+/HEAD/docs/qemu.md#Build-QEMU):
```
cd third_party/qemu
./configure --target-list=arm-softmmu,aarch64-softmmu,x86_64-softmmu
make -j32
sudo make install
```

* Run Fuchsia in QEMU:
```
frun -g
```
To run in command-line only mode, omit the `-g` flag. The `-m` flag sets QEMU's memory size in MB. Adding `-N` will enable network, but you will need to
[configure](https://fuchsia.googlesource.com/magenta/+/master/docs/qemu.md#Enabling-Networking-under-Qemu-x86_64-only)
a virtual interface and this is only available under x86_64.

When Fuchsia has booted and started an MXCONSOLE, you can run programs!

For example, to receive deep wisdom, run:

```
fortune
```

Run [mozart](https://fuchsia.googlesource.com/mozart) applications in `/system/apps` like this:

```
@ bootstrap launch spinning_square_view
```

Some more mozart example apps are [here](https://fuchsia.googlesource.com/mozart/+/HEAD/examples/).

### Run Fuchsia on hardware

* [Acer Switch Alpha 12](https://fuchsia.googlesource.com/magenta/+/master/docs/targets/acer12.md)
* [Intel NUC](https://fuchsia.googlesource.com/magenta/+/master/docs/targets/nuc.md)
* [Raspberry Pi 3](https://fuchsia.googlesource.com/magenta/+/master/docs/targets/rpi3.md)

## Additional helpful documents


* [Fuchsia documentation](https://fuchsia.googlesource.com/docs) hub.
* [Contributing changes](https://fuchsia.googlesource.com/manifest/+/HEAD/README.md#Submitting-changes).
* More about the [build commands](https://fuchsia.googlesource.com/fuchsia/+/HEAD/BUILD_NOTES.md) called under-the-hood by `fbuild`.
