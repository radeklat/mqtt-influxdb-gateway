# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
Types of changes are:

- **Added** for new features.
- **Changed** for changes in existing functionality.
- **Deprecated** for soon-to-be removed features.
- **Removed** for now removed features.
- **Fixed** for any bug fixes.
- **Security** in case of vulnerabilities.

## [Unreleased]

## [0.2.0] - 2011-11-02

### Added

- Option to define when to merge data points (`mqtt_merge_data_points_on`).
- Validation of variables in `mqtt_topic_pattern`.
- Validation of `influxdb_url`
- Options to set global bucket and measurement with `influxdb_default_bucket` and `influxdb_default_measurement`.
- Documentation of settings.

## [0.1.2] - 2011-10-31

### Changed

- Change `Dockerfile` to use Python version from `pyproject.toml`.

## [0.1.1] - 2011-10-30

### Changed

- Updates build process to build docker images for multiple architectures.

### Fixed
- docker-compose file not starting up the container correctly.

## [0.1.0] - 2011-10-28

- Initial release

[Unreleased]: https://github.com/radeklat/mqtt_influxdb_gateway/compare/0.2.0...HEAD
[0.2.0]: https://github.com/radeklat/mqtt_influxdb_gateway/compare/0.1.2...0.2.0
[0.1.2]: https://github.com/radeklat/mqtt_influxdb_gateway/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/radeklat/mqtt_influxdb_gateway/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/radeklat/mqtt_influxdb_gateway/compare/initial...0.1.0