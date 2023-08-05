# mups

### Following Standards

- PEP 508: Package Names. `mups` has more stricter names only with lowercases and dashes.
- PEP 440: Package Version
- Due to PEP 632, Deprecate distutils module, `mups` uses `sysconfig.get_platform()` to get platform identifier.
- Email format follows RFC 5322