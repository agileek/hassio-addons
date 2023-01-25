# HOWTO BUILD

Thanks to https://github.com/agileek/hassio-addons/pull/47 this is now done using a github action workflow.

Just go to https://github.com/agileek/hassio-addons/actions/workflows/build-libsignal.yml and run a workflow on your branch, after modifying the LIBSIGNAL_VERSION in .github/workflows/build-libsignal.yml


# OLD

[cross](https://github.com/rust-embedded/cross) is used for cross compiling libsignal-client.

* download new release from `https://github.com/signalapp/libsignal-client/releases`
* unzip + change into directory
* run `cross build --target x86_64-unknown-linux-gnu -p libsignal-jni --release`
  run `cross build --target armv7-unknown-linux-gnueabihf -p libsignal-jni --release`
  run `cross build --target aarch64-unknown-linux-gnu -p libsignal-jni --release`
to build the library for `x86-64`, `armv7` and `arm64`
* the built library will be in the `target/<architecture>/release` folder 

## Why?

Building libsignal-client every time a new docker image gets released takes really long (especially for cross platform builds with docker/buildx and QEMU). Furthermore, due to this bug here (https://github.com/docker/buildx/issues/395) we would need to use an ugly workaround for that right now. As libsignal-client isn't released very often I guess it's okay to manually build a new version once in a while.  
