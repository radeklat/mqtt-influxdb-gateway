# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).
Types of changes are:

- **Breaking changes** for breaking changes.
- **Features** for new features or changes in existing functionality.
- **Fixes** for any bug fixes.
- **Deprecated** for soon-to-be removed features.

## [Unreleased]

## [0.2.2] - 2012-12-30

### Fixes

- Dependencies update

## [0.2.1] - 2011-11-07

### Fixes

- Improved environment variables documentation.

## [0.2.0] - 2011-11-02

### Features

- Option to define when to merge data points (`mqtt_merge_data_points_on`).
- Validation of variables in `mqtt_topic_pattern`.
- Validation of `influxdb_url`
- Options to set global bucket and measurement with `influxdb_default_bucket` and `influxdb_default_measurement`.
- Documentation of settings.

## [0.1.2] - 2011-10-31

### Features

- Change `Dockerfile` to use Python version from `pyproject.toml`.

## [0.1.1] - 2011-10-30

### Features

- Updates build process to build docker images for multiple architectures.

### Fixes

- docker-compose file not starting up the container correctly.

## [0.1.0] - 2011-10-28

- Initial release

[Unreleased]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.2.2...HEAD
[0.2.2]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.1.2...0.2.0
[0.1.2]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/initial...0.1.0
