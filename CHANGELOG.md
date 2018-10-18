# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).


## [Unreleased][unreleased]
### Added
- Added `--quick-benchmark` for Travis can check assertions of performance tests too
- Added Python3 support


## [1.1.2] - 2018-10-18
### Changed
- Updated development dependencies
- More understandable error message when path was not specified

### Fixed
- Fixed performance test of [WSC007] rule
- Fixed "wscheck: error: paths" error


## [1.1.1] - 2017-11-02
### Fixed
- Removed unnecessary test files from the released package


## [1.1.0] - 2017-11-02
### Added
- Added rule for checking empty lines at the beginning of the files ([WSC007])
- Added PyPy support
- Added performance measurement tests
- Added small detail and example to pages of rules.

### Changed
- Improved documentation

### Fixed
- Fixed the HTML generation error of readme on GitHub and PyPi


## [1.0.1] - 2017-07-14
### Fixed
- Fixed versioning


## [1.0.0] - 2017-07-14
### Added
- Added documentation for rules

### Changed
- Renamed rule IDs from **WSW000** to **WSC000** for better fit to the name of `wscheck`
- Set version number for all components


## [0.1.6] - 2016-08-31
### Fixed
- Fixed column calculation of [WSW003][WSC003] rule


## [0.1.5] - 2016-08-31
### Added
- Added some test cases to printer

### Changed
- Always write checkstyle output in case-insensitive alphabetic order of paths

### Fixed
- Fixed arrow position on console output


## [0.1.4] - 2016-08-11
### Fixed
- KeyError: 'row' in printer.py:15 - issue #1


## [0.1.3] - 2016-08-05
### Added
- Covered code with tests

## Fixed
- Write checkstyle file when no issues
- Write issue-less paths into checkstyle output


## [0.1.2] - 2016-08-04
### Changed
- Minimized dependencies


## [0.1.1] - 2016-08-04
### Added
- PyPi release


## 0.1.0 - 2016-08-04
### Added
- `wscheck` lib with command line bin (with [WSW001][WSC001], [WSW002][WSC002], [WSW003][WSC003], [WSW004][WSC004],
  [WSW005][WSC005], [WSW006][WSC006] rules)


[unreleased]: https://github.com/andras-tim/wscheck/compare/v1.1.2...HEAD
[1.1.2]: https://github.com/andras-tim/wscheck/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/andras-tim/wscheck/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/andras-tim/wscheck/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/andras-tim/wscheck/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/andras-tim/wscheck/compare/v0.1.6...v1.0.0
[0.1.6]: https://github.com/andras-tim/wscheck/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/andras-tim/wscheck/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/andras-tim/wscheck/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/andras-tim/wscheck/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/andras-tim/wscheck/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/andras-tim/wscheck/compare/v0.1.0...v0.1.1

[WSC001]: https://wscheck.readthedocs.io/en/latest/rules/WSC001.html
[WSC002]: https://wscheck.readthedocs.io/en/latest/rules/WSC002.html
[WSC003]: https://wscheck.readthedocs.io/en/latest/rules/WSC003.html
[WSC004]: https://wscheck.readthedocs.io/en/latest/rules/WSC004.html
[WSC005]: https://wscheck.readthedocs.io/en/latest/rules/WSC005.html
[WSC006]: https://wscheck.readthedocs.io/en/latest/rules/WSC006.html
[WSC007]: https://wscheck.readthedocs.io/en/latest/rules/WSC007.html
