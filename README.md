# mups

![](mups_logo.PNG)
### Following Standards

- PEP 566, 643: RingInfo, aka Metadata for Mojo software packages is based on PEP 566
- PEP 508: Package Names. `mups` has more stricter names only with lowercases and dashes.
- PEP 440: Package Version, which is almost compatible with semantic versioning 2.0.
- Due to PEP 632, Deprecate distutils module, `mups` uses `sysconfig.get_platform()` to get platform identifier.
- Email format follows RFC 5322
- PEP 301: [Classifiers](https://www.python.org/dev/peps/pep-0301/#distutils-trove-classification)
- PEP 643: Metadata for Package Source Distributions
- PEP 685: Comparison of extra names for optional distribution dependencies

### TODO

- Follow PEP 427 Wheel Format