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

## [0.2.4] - 2023-11-07

### Fixes

- Update `pydantic` to `2.x`.

## [0.2.3] - 2023-09-16

### Fixes

- Switch `settings-doc` from CI to `pre-commit` hook.
- 

## [0.2.2] - 2022-12-30

### Fixes

- Dependencies update

## [0.2.1] - 2021-11-07

### Fixes

- Improved environment variables documentation.

## [0.2.0] - 2021-11-02

### Features

- Option to define when to merge data points (`mqtt_merge_data_points_on`).
- Validation of variables in `mqtt_topic_pattern`.
- Validation of `influxdb_url`
- Options to set global bucket and measurement with `influxdb_default_bucket` and `influxdb_default_measurement`.
- Documentation of settings.

## [0.1.2] - 2021-10-31

### Features

- Change `Dockerfile` to use Python version from `pyproject.toml`.

## [0.1.1] - 2021-10-30

### Features

- Updates build process to build docker images for multiple architectures.

### Fixes

- docker-compose file not starting up the container correctly.

## [0.1.0] - 2021-10-28

- Initial release

[Unreleased]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.2.4...HEAD
[0.2.4]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.2.3...0.2.4
[0.2.3]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.2.2...0.2.3
[0.2.2]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.2.1...0.2.2
[0.2.1]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.1.2...0.2.0
[0.1.2]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/radeklat/mqtt-influxdb-gateway/compare/initial...0.1.0
